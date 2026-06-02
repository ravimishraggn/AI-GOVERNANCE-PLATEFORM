# Governance Platform Plugin Contract

The Governance Platform supports extension via a plugin architecture.
Plugins implement well-defined interfaces and register with the Extension Registry.
The platform routes to registered plugins at defined extension points.

---

## Extension Points

| Extension Point | Interface File | Purpose |
|----------------|---------------|---------|
| PolicyRule | `interfaces/policy-rule-interface.yaml` | Custom policy rule evaluators |
| RiskScorer | `interfaces/risk-scorer-interface.yaml` | Custom risk scoring algorithms |
| ComplianceControl | `interfaces/compliance-control-interface.yaml` | Regulatory framework modules |
| EvaluationMetric | `interfaces/evaluation-metric-interface.yaml` | Custom evaluation benchmarks |
| ContentClassifier | `interfaces/content-classifier-interface.yaml` | Custom content classifiers |

---

## Plugin Requirements

Every plugin MUST:

1. Implement the interface contract for its declared extension point
2. Declare its resource requirements in the plugin manifest
3. Handle errors gracefully — platform fails safely if plugin is unavailable
4. Emit standard telemetry via the platform's observability infrastructure
5. Pass the plugin certification process before activation in production

Every plugin MUST NOT:

1. Access platform internals or other tenants' data
2. Make undeclared network calls
3. Consume unlimited compute resources
4. Modify audit records
5. Modify the governance metadata store outside of its declared scope

---

## Plugin Manifest Format

```yaml
apiVersion: governance.platform/v1
kind: PluginManifest

metadata:
  plugin_id: "my-org.my-plugin-name"
  display_name: "My Plugin"
  version: "1.0.0"
  author: "Author Name"
  contact: "contact@author.com"

extension_point: PolicyRule   # which extension point this plugin implements

capabilities:
  - name: "describe what this plugin does"

resource_limits:
  max_cpu_ms_per_call: 100    # max CPU time per invocation
  max_memory_mb: 64           # max memory per invocation
  max_timeout_ms: 500         # hard timeout

network_permissions:
  outbound_allowed: false     # declare if plugin needs network access
  allowed_domains: []         # explicit allowlist if outbound_allowed: true

data_permissions:
  can_read_artifact_metadata: true
  can_read_policy_decisions: false
  can_read_audit_events: false
  can_write_governance_data: false   # almost never true for third-party plugins

certification:
  certified_by: null          # platform team fills this on certification
  certified_at: null
  certification_scope: []     # which use cases this plugin is certified for
```

---

## First-Party Plugins

See `../first-party/` for platform-maintained plugins:

- `sec-compliance-pack/` — SEC SR 11-7 and Reg BI compliance controls
- `gdpr-compliance-pack/` — GDPR Article 22 and data minimization controls
- `private-markets-domain-pack/` — Private markets evaluation benchmarks

---

## Plugin Development

1. Read the interface specification for your target extension point
2. Implement the interface in your language of choice
3. Package as a Docker container with the governance-sdk as a dependency
4. Write the plugin manifest
5. Submit to the Governance Team for certification review
6. After certification: register via Extension Registry API
