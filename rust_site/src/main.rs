use actix_web::{web, App, HttpServer};
use rust_site::*;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(move || {
        App::new()
            .route("/", web::get().to(index))
            .service(working)
            .app_data(web::Data::new(create_test_gauge_metric()))
            .wrap(create_prometheus_metrics().clone())
    })
    .bind(("0.0.0.0", 9090))?
    .run()
    .await
}
