package rwosidecar

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// GRPCServiceName and GRPCReduceMethod are deliberately versioned. They define
// the candidate-local wire route without making protobuf generation a claim.
const (
	GRPCServiceName  = "rwo.v1.EventBoundary"
	GRPCReduceMethod = "/" + GRPCServiceName + "/Reduce"
)

// JSONCodec is the explicit prototype codec for the manually described gRPC
// route. encoding/json encodes []byte as base64, so raw accepted-event bytes
// round-trip without JSON re-parsing at the sidecar boundary.
//
// This is not a protobuf schema or a general transport interchangeability
// claim. A production wire contract would need its own separately owned
// schema and compatibility evidence.
type JSONCodec struct{}

func (JSONCodec) Name() string { return "rwo-json" }

func (JSONCodec) Marshal(value any) ([]byte, error) { return json.Marshal(value) }

func (JSONCodec) Unmarshal(data []byte, value any) error { return json.Unmarshal(data, value) }

// GRPCClient invokes the one versioned sidecar route. It takes the same
// boundary envelope as any other ingress adapter, so delivery metadata remains
// visible to the observation but is excluded by Service.Reduce from the pure
// kernel request.
type GRPCClient struct {
	connection grpc.ClientConnInterface
}

func NewGRPCClient(connection grpc.ClientConnInterface) GRPCClient {
	return GRPCClient{connection: connection}
}

func (client GRPCClient) Reduce(ctx context.Context, envelope EventEnvelope) (Observation, error) {
	if client.connection == nil {
		return Observation{}, fmt.Errorf("%w: gRPC connection is required", ErrMalformedEnvelope)
	}

	var observation Observation
	if err := client.connection.Invoke(
		ctx,
		GRPCReduceMethod,
		&envelope,
		&observation,
		grpc.ForceCodec(JSONCodec{}),
	); err != nil {
		return Observation{}, err
	}
	return observation, nil
}

// NewGRPCServer returns a local gRPC server for the candidate-local sidecar.
// Its explicit codec is paired with GRPCClient's ForceCodec call so the route
// does not depend on global codec registration or generated protobuf types.
func NewGRPCServer(service Service) *grpc.Server {
	server := grpc.NewServer(grpc.ForceServerCodec(JSONCodec{}))
	RegisterGRPCEventBoundary(server, service)
	return server
}

// grpcEventBoundaryServer is a small manual equivalent of a generated unary
// server interface. Keeping it private avoids representing the prototype
// route as a public generated-protobuf API.
type grpcEventBoundaryServer interface {
	Reduce(context.Context, *EventEnvelope) (*Observation, error)
}

type grpcEventBoundaryAdapter struct {
	service Service
}

func (adapter *grpcEventBoundaryAdapter) Reduce(ctx context.Context, envelope *EventEnvelope) (*Observation, error) {
	if envelope == nil {
		return nil, status.Error(codes.InvalidArgument, "RWO event envelope is required")
	}
	observation, err := adapter.service.Reduce(ctx, *envelope)
	if err != nil {
		if errors.Is(err, ErrMalformedEnvelope) {
			return nil, status.Error(codes.InvalidArgument, err.Error())
		}
		if errors.Is(err, ErrInvalidKernelResponse) {
			return nil, status.Error(codes.FailedPrecondition, err.Error())
		}
		return nil, status.Error(codes.Internal, err.Error())
	}
	return &observation, nil
}

// RegisterGRPCEventBoundary registers the only gRPC method supported by this
// prototype. It is intentionally separate from HTTP and future adapter setup:
// all paths converge on Service.Reduce rather than sharing transport state.
func RegisterGRPCEventBoundary(server *grpc.Server, service Service) {
	if server == nil {
		panic("RWO gRPC server is required")
	}
	server.RegisterService(&grpc.ServiceDesc{
		ServiceName: GRPCServiceName,
		HandlerType: (*grpcEventBoundaryServer)(nil),
		Methods: []grpc.MethodDesc{{
			MethodName: "Reduce",
			Handler:    grpcReduceHandler,
		}},
		Metadata: "rwo.v1.json",
	}, &grpcEventBoundaryAdapter{service: service})
}

func grpcReduceHandler(
	server any,
	ctx context.Context,
	decode func(any) error,
	interceptor grpc.UnaryServerInterceptor,
) (any, error) {
	envelope := new(EventEnvelope)
	if err := decode(envelope); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return server.(grpcEventBoundaryServer).Reduce(ctx, envelope)
	}
	info := &grpc.UnaryServerInfo{Server: server, FullMethod: GRPCReduceMethod}
	handler := func(ctx context.Context, request any) (any, error) {
		return server.(grpcEventBoundaryServer).Reduce(ctx, request.(*EventEnvelope))
	}
	return interceptor(ctx, envelope, info, handler)
}
