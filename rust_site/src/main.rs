use actix_web::{web, App, HttpServer};
use rust_site::*;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Serving at http://localhost:3000");
    HttpServer::new(move || {
        App::new()
            .route("/", web::get().to(index))
            .service(api)
            .service(working)
            .app_data(web::Data::new(create_test_gauge_metric()))
            .wrap(create_prometheus_metrics().clone())
    })
    .bind(("0.0.0.0", 3000))?
    .run()
    .await
}
