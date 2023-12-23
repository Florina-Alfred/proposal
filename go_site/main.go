package main

import (
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
	// gin.DefaultWriter = io.Discard
	router.LoadHTMLGlob("templates/*")

	router.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.tmpl", gin.H{})
	})
	router.GET("/working", working)
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
