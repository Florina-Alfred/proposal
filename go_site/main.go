package main

import (
	"math/rand"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/penglongli/gin-metrics/ginmetrics"
)

type status struct {
	Working  string    `json:"working"`
	Language string    `json:"language"`
	Time     time.Time `json:"time"`
}

func working(c *gin.Context) {

	ginmetrics.GetMonitor().GetMetric("test_gauge_metric").SetGaugeValue([]string{"label_value1"}, rand.Float64())
	/* c.JSON(http.StatusOK, gin.H{
		"working": "ok",
	}) */
	var currentStatus = status{Working: "ok", Language: "golang", Time: time.Now()}
	c.IndentedJSON(http.StatusOK, currentStatus)
}

func main() {

	router := gin.New()
	gin.SetMode(gin.ReleaseMode)
	// gin.DefaultWriter = io.Discard
	router.LoadHTMLGlob("templates/*")

	metrics := ginmetrics.GetMonitor()
	metrics.SetMetricPath("/metrics")
	metrics.SetSlowTime(10)
	metrics.SetDuration([]float64{0.1, 0.3, 1.2, 5, 10})
	metrics.Use(router)
	gaugeMetric := &ginmetrics.Metric{
		Type:        ginmetrics.Gauge,
		Name:        "test_gauge_metric",
		Description: "an example of gauge type metric",
		Labels:      []string{"label1"},
	}

	ginmetrics.GetMonitor().AddMetric(gaugeMetric)

	router.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.tmpl", gin.H{})
	})

	router.GET("/working", working)

	router.Run(":3000")

}
