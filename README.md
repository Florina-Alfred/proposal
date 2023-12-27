# proposal

Site builder written in mutliple languages. This is coded to have the following features:

[x] Python
[x] Go
[x] Rust

| End-point | Descriptions                                             |
| --------- | -------------------------------------------------------- |
| /         | HTML page with HTMX form data and buttons                |
| /metrics  | Prometheus metrics (test_gauge with random float number) |
| /working  | JSON with health, language and time                      |
|           |                                                          |

Example of JSON from _/working_ end-point:

```json
{
  "working": "ok",
  "language": "python",
  "time": "xxxxxxxxxxxxx"
}
```
