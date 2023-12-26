use actix_files::NamedFile;
use actix_web::{get, web, Responder, Result};
use actix_web_prom::PrometheusMetrics;
use actix_web_prom::PrometheusMetricsBuilder;
use prometheus::{
    core::{AtomicF64, GenericGauge},
    Gauge,
};
use rand::Rng;
use serde::Serialize;

#[derive(Serialize)]
struct Status {
    working: String,
}

#[get("/working")]
async fn working(test_gauge: web::Data<Gauge>) -> Result<impl Responder> {
    let obj = Status {
        working: "ok".to_string(),
    };
    test_gauge.set(rand::thread_rng().gen::<f64>());
    return Ok(web::Json(obj));
    // Ok(HttpResponse::Ok())
}

pub async fn index() -> Result<NamedFile> {
    Ok(NamedFile::open("./src/static/index.html")?)
}

pub fn add_prom_metric() -> PrometheusMetrics {
    let prometheus = PrometheusMetricsBuilder::new("api")
        .endpoint("/metrics")
        .build()
        .unwrap();

    let test_guage = Gauge::new("test_guage", "example of guage").unwrap();
    test_guage.set(rand::thread_rng().gen::<f64>());
    prometheus
        .registry
        .register(Box::new(test_guage.clone()))
        .unwrap();

    return prometheus;
}

pub fn create_test_gauge_metric() -> GenericGauge<AtomicF64> {
    let test_guage = Gauge::new("test_guage", "example of guage").unwrap();
    test_guage.set(rand::thread_rng().gen::<f64>());

    return test_guage;
}

pub fn create_prometheus_metrics() -> PrometheusMetrics {
    let prometheus = PrometheusMetricsBuilder::new("api")
        .endpoint("/metrics")
        .build()
        .unwrap();
    /*     let test_guage = Gauge::new("test_guage", "example of guage").unwrap();
    test_guage.set(rand::thread_rng().gen::<f64>()) */
    prometheus
        .registry
        .register(Box::new(create_test_gauge_metric()))
        .unwrap();

    return prometheus;
}
