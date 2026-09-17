# OTLP/HTTP Mapping

v3.9 implements a minimal JSON metrics mapping suitable for controlled integration tests and collector gateways.

Supported shape:

```text
resourceMetrics
  -> resource.attributes
  -> scopeMetrics
  -> metrics
      -> gauge | sum | histogram | exponentialHistogram
          -> dataPoints
```

Resource/service attributes are merged with data-point attributes for component selection and labels.

This is not a claim of complete OpenTelemetry protocol compliance. For broad interoperability, place an OpenTelemetry Collector in front of the runtime and emit the bounded JSON subset expected by this release.
