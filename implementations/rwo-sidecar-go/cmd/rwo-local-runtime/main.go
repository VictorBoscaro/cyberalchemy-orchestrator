// rwo-local-runtime starts the candidate-local RWO host on one loopback gRPC
// listener. It is a development process, not a public service, deployment
// artifact, adapter framework, or production runtime.
package main

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"net"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"

	rwosidecar "cyberalchemy-orchestrator/implementations/rwo-sidecar-go"
	"google.golang.org/grpc"
)

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "rwo-local-runtime:", err)
		os.Exit(1)
	}
}

func run() error {
	var (
		compositionPath string
		tuplePath       string
		registryPath    string
		kernelChildPath string
		storePath       string
		storeInstanceID string
		materialRoot    string
		listenAddress   string
		maxFrameBytes   uint
	)
	flags := flag.NewFlagSet("rwo-local-runtime", flag.ContinueOnError)
	flags.SetOutput(os.Stderr)
	flags.StringVar(&compositionPath, "composition", "", "raw ExplicitComposition JSON file")
	flags.StringVar(&tuplePath, "composition-tuple", "", "VersionTuple JSON file for the composition")
	flags.StringVar(&registryPath, "registry", "", "local Rust registry.json path")
	flags.StringVar(&kernelChildPath, "kernel-child", "", "local rwo_kernel_child executable")
	flags.StringVar(&storePath, "store", "", "exclusive local durable .rwolog path")
	flags.StringVar(&storeInstanceID, "store-instance-id", "", "stable identifier bound into a new store header")
	flags.StringVar(&materialRoot, "material-root", "", "allowed read-only seat-material directory")
	flags.StringVar(&listenAddress, "listen", "127.0.0.1:0", "loopback gRPC listen address")
	flags.UintVar(&maxFrameBytes, "max-frame-bytes", 1<<20, "private child frame maximum (1..4294967295)")
	if err := flags.Parse(os.Args[1:]); err != nil {
		return err
	}
	if flags.NArg() != 0 {
		return fmt.Errorf("unexpected positional arguments")
	}
	if compositionPath == "" || tuplePath == "" || registryPath == "" || kernelChildPath == "" ||
		storePath == "" || storeInstanceID == "" || materialRoot == "" || maxFrameBytes == 0 || maxFrameBytes > uint(^uint32(0)) {
		return fmt.Errorf("composition, composition-tuple, registry, kernel-child, store, store-instance-id, material-root, and a bounded max-frame-bytes are required")
	}
	if err := requireLoopback(listenAddress); err != nil {
		return err
	}
	materialInfo, err := os.Stat(filepath.Clean(materialRoot))
	if err != nil || !materialInfo.IsDir() {
		return fmt.Errorf("material-root must be an existing directory")
	}

	composition, err := os.ReadFile(filepath.Clean(compositionPath))
	if err != nil {
		return fmt.Errorf("read raw composition: %w", err)
	}
	if len(composition) == 0 {
		return fmt.Errorf("raw composition must not be empty")
	}
	tupleBytes, err := os.ReadFile(filepath.Clean(tuplePath))
	if err != nil {
		return fmt.Errorf("read composition tuple: %w", err)
	}
	var tuple rwosidecar.VersionTuple
	if err := json.Unmarshal(tupleBytes, &tuple); err != nil {
		return fmt.Errorf("decode composition tuple: %w", err)
	}

	child, err := rwosidecar.StartProcessKernel(rwosidecar.ChildKernelConfig{
		ExecutablePath: kernelChildPath,
		RegistryPath:   registryPath,
		MaxFrameBytes:  uint32(maxFrameBytes),
	})
	if err != nil {
		return err
	}
	defer child.Close()
	compiled, err := child.Compile(context.Background(), rwosidecar.CompileRequest{
		Tuple: tuple, RawComposition: composition,
	})
	if err != nil {
		return fmt.Errorf("compile composition: %w", err)
	}
	if compiled.Outcome != "Compiled" {
		return fmt.Errorf("composition rejected by semantic kernel: %v", compiled.DefectCodes)
	}
	compositionDigest := sha256.Sum256(composition)
	store, err := rwosidecar.OpenDurableStore(filepath.Clean(storePath), rwosidecar.DurableStoreHeader{
		StoreFormat:          rwosidecar.DurableStoreFormatV1,
		GraphIdentity:        compiled.GraphIdentity,
		RawCompositionSHA256: hex.EncodeToString(compositionDigest[:]),
		Tuple:                tuple,
		StoreInstanceID:      storeInstanceID,
	})
	if err != nil {
		return fmt.Errorf("open durable store: %w", err)
	}
	defer store.Close()
	runtime, err := rwosidecar.NewDurableRuntimeKernel(child, compiled, store)
	if err != nil {
		return err
	}
	defer runtime.Close()

	listener, err := net.Listen("tcp", listenAddress)
	if err != nil {
		return fmt.Errorf("listen on requested loopback address: %w", err)
	}
	defer listener.Close()
	server := rwosidecar.NewGRPCServer(rwosidecar.Service{Kernel: runtime})
	defer server.Stop()

	serveDone := make(chan error, 1)
	go func() { serveDone <- server.Serve(listener) }()
	fmt.Fprintln(os.Stdout, listener.Addr().String())

	context, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	select {
	case <-context.Done():
		server.Stop()
		if err := <-serveDone; err != nil && !errors.Is(err, grpc.ErrServerStopped) {
			return fmt.Errorf("serve local gRPC runtime: %w", err)
		}
		return nil
	case err := <-serveDone:
		if err != nil && !errors.Is(err, grpc.ErrServerStopped) {
			return fmt.Errorf("serve local gRPC runtime: %w", err)
		}
		return nil
	}
}

func requireLoopback(address string) error {
	host, _, err := net.SplitHostPort(address)
	if err != nil {
		return fmt.Errorf("listen must be a host:port loopback address: %w", err)
	}
	ip := net.ParseIP(host)
	if ip == nil || !ip.IsLoopback() {
		return fmt.Errorf("listen address must use a numeric loopback host")
	}
	return nil
}
