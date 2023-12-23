use actix_files::NamedFile;
use actix_web::{get, web, App, HttpServer, Responder, Result};
use actix_web_prom::PrometheusMetricsBuilder;
use prometheus::Gauge;
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
    Ok(web::Json(obj))
}

async fn index() -> Result<NamedFile> {
    Ok(NamedFile::open("./src/static/index.html")?)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
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

    HttpServer::new(move || {
        App::new()
            .route("/", web::get().to(index))
            .service(working)
            .app_data(web::Data::new(test_guage.clone()))
            .wrap(prometheus.clone())
    })
    .bind(("0.0.0.0", 9090))?
    .run()
    .await
}
