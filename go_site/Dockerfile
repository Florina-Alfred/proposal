FROM golang:latest AS Builder

WORKDIR /go_site
COPY . .
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /go/bin/go_site
RUN chmod +x /go/bin/go_site


#FROM alpine:latest
FROM ubuntu:latest
WORKDIR /go/bin
COPY --from=Builder /go/bin/go_site /go/bin/go_site
COPY --from=Builder /go_site/templates /go/bin/templates
#USER root:root
ENV GIN_MODE=release
CMD ["/go/bin/go_site"]


