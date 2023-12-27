# proposal

Site builder written in the following mutliple languages:

- [x] Python
- [x] Go
- [x] Rust

Site has the following end-points:

| End-point  | Descriptions                                             |
| ---------- | -------------------------------------------------------- |
| `/`        | HTML page with HTMX form data and buttons                |
| `/metrics` | Prometheus metrics (test_gauge with random float number) |
| `/working` | JSON with health, language and time                      |
|            |                                                          |

Example of JSON from `/working` end-point:

```json
{
  "working": "ok",
  "language": "python",
  "time": "xxxxxxxxxxxxx"
}
```
