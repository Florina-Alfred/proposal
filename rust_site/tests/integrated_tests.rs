use actix_service::Service;
use actix_web::{http::StatusCode, test, web, App};
use rust_site::*;

#[actix_web::test]
async fn test_api_service() {
    let app = test::init_service(App::new().service(api)).await;

    let req = test::TestRequest::with_uri("/api").to_request();

    let res = app.call(req).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
}

#[actix_web::test]
async fn test_working_service() {
    let app = test::init_service(
        App::new()
            .app_data(web::Data::new(create_test_gauge_metric()))
            .service(working),
    )
    .await;

    let req = test::TestRequest::with_uri("/working").to_request();

    let res = app.call(req).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
}

/* #[cfg(test)]
mod tests {
    use actix_web::{http::header::ContentType, test, web, App};

    // use super::*;
    use rust_site::{create_test_gauge_metric, working};

    #[actix_web::test]
    async fn test_index_get() {
        let app = test::init_service(
            App::new()
                .app_data(web::Data::new(create_test_gauge_metric()))
                .service(working),
        )
        .await;
        let req = test::TestRequest::default()
            // .insert_header(ContentType::plaintext())
            .uri("/working")
            .to_request();
        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
    }
} */

/* use actix_web::{get, test, web, App, Error, HttpResponse, Responder};
use rust_site::*;

#[actix_rt::test]
async fn test_example() {
    let srv = actix_test::start(|| {
        App::new()
            .app_data(web::Data::new(create_test_gauge_metric()))
            .service(working)
    });

    let req = srv.get("/working");
    let res = req.send().await.unwrap();

    assert!(res.status().is_success());
} */
