package main

import (
	"encoding/json"
	"io"
	"math/rand"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/penglongli/gin-metrics/ginmetrics"
)

type status struct {
	Working  string `json:"working"`
	Language string `json:"language"`
	Time     string `json:"time"`
}

func api(c *gin.Context) {
	url := "https://mashape-community-urban-dictionary.p.rapidapi.com/define?term=soydev"

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return
	}

	req.Header.Add("X-RapidAPI-Key", "e15cce8cedmsh829310d4a331963p1ca8fdjsnd643b41e3b65")
	req.Header.Add("X-RapidAPI-Host", "mashape-community-urban-dictionary.p.rapidapi.com")

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		return
	}
	defer res.Body.Close()

	body, err := io.ReadAll(res.Body)
	if err != nil {
		return
	}
	c.JSON(http.StatusOK, gin.H{"data": json.RawMessage(body)})

}

func working(c *gin.Context) {

	ginmetrics.GetMonitor().GetMetric("test_gauge").SetGaugeValue([]string{"label_value1"}, rand.Float64())
	/* c.JSON(http.StatusOK, gin.H{
		"working": "ok",
	}) */
	var currentStatus = status{Working: "ok", Language: "golang", Time: time.Now().Format(time.UnixDate)}
	c.IndentedJSON(http.StatusOK, currentStatus)
}

func setupRouter() *gin.Engine {
	gin.SetMode(gin.ReleaseMode)
	// router := gin.Default()
	router := gin.New()
	router.LoadHTMLGlob("templates/*")

	router.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.tmpl", gin.H{})
	})
	router.GET("/working", working)
	router.GET("/api", api)

	metrics := ginmetrics.GetMonitor()
	metrics.SetMetricPath("/metrics")
	metrics.SetSlowTime(10)
	metrics.SetDuration([]float64{0.1, 0.3, 1.2, 5, 10})
	metrics.Use(router)

	gaugeMetric := &ginmetrics.Metric{
		Type:        ginmetrics.Gauge,
		Name:        "test_gauge",
		Description: "an example of gauge type metric",
		Labels:      []string{"label1"},
	}

	ginmetrics.GetMonitor().AddMetric(gaugeMetric)
	ginmetrics.GetMonitor().GetMetric("test_gauge").SetGaugeValue([]string{"label_value1"}, rand.Float64())
	return router
}

func main() {
	router := setupRouter()
	router.Run(":3000")
}
