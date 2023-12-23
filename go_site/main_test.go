package main

import (
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestWorking(t *testing.T) {
	router := setupRouter()
	var mockResponse = status{Working: "ok", Language: "golang", Time: time.Now().Format(time.UnixDate)}

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/working", nil)
	router.ServeHTTP(w, req)

	responseData, _ := io.ReadAll(w.Body)
	responseDataStruct := status{}
	json.Unmarshal([]byte(responseData), &responseDataStruct)

	assert.Equal(t, 200, w.Code)
	assert.Equal(t, mockResponse, responseDataStruct)
}

func TestMetric(t *testing.T) {
	router := setupRouter()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/metrics", nil)
	router.ServeHTTP(w, req)

	responseData := w.Body.String()

	assert.Equal(t, 200, w.Code)
	assert.Contains(t, responseData, "test_gauge")
}
