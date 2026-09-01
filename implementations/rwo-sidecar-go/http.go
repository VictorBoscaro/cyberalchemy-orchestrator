package rwosidecar

import (
	"encoding/json"
	"net/http"
)

// NewHTTPHandler exposes one local reference adapter. It exists to exercise
// the lossless envelope seam without claiming that HTTP is the preferred or
// production transport; a future gRPC adapter should preserve this contract.
func NewHTTPHandler(service Service) http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("POST /v1/reduce", func(writer http.ResponseWriter, request *http.Request) {
		defer request.Body.Close()
		var envelope EventEnvelope
		decoder := json.NewDecoder(http.MaxBytesReader(writer, request.Body, 1<<20))
		if err := decoder.Decode(&envelope); err != nil {
			writeJSONError(writer, http.StatusBadRequest, "INVALID_ENVELOPE")
			return
		}
		observation, err := service.Reduce(request.Context(), envelope)
		if err != nil {
			writeJSONError(writer, http.StatusBadRequest, "INVALID_ENVELOPE")
			return
		}
		writer.Header().Set("Content-Type", "application/json")
		writer.WriteHeader(http.StatusOK)
		_ = json.NewEncoder(writer).Encode(observation)
	})
	return mux
}

func writeJSONError(writer http.ResponseWriter, status int, code string) {
	writer.Header().Set("Content-Type", "application/json")
	writer.WriteHeader(status)
	_ = json.NewEncoder(writer).Encode(map[string]string{"code": code})
}
