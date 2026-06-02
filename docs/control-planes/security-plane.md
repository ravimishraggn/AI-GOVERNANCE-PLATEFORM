# Security Plane

## Purpose

The Security Plane enforces AI-specific security controls that are distinct from general IT
security: prompt injection prevention, data exfiltration detection, model abuse monitoring,
and adversarial input handling.

---

## Responsibilities

- Detect and block prompt injection attempts before they reach LLMs
- Monitor for indirect prompt injection in retrieved content (RAG poisoning)
- Detect patterns consistent with data exfiltration via model outputs
- Identify and log jailbreak attempts and their outcomes
- Monitor for model abuse: credential harvesting, PII extraction, social engineering
- Enforce data classification controls at the prompt and response boundary
- Manage AI-specific secrets: API keys, model credentials, dataset access tokens
- Integrate AI security signals with enterprise SIEM

---

## Threat Model

```
EXTERNAL THREATS
├── Direct Prompt Injection
│     Attacker submits crafted user input that overrides system prompt instructions
│     Mitigation: injection detection classifier, sandboxed execution context
│
├── Indirect Prompt Injection (RAG Poisoning)
│     Malicious content embedded in documents retrieved for RAG context
│     Mitigation: retrieved content scanning before context injection
│
├── Jailbreak Attacks
│     Adversarial prompts bypassing safety constraints
│     Mitigation: jailbreak pattern detection, safety evaluation at response time
│
└── Model Extraction
      Systematic querying to reconstruct proprietary model behavior or data
      Mitigation: rate limiting, query pattern detection, anomaly alerting

INTERNAL THREATS
├── Data Exfiltration via AI
│     Authorized user using AI to extract and exfiltrate sensitive data at scale
│     Mitigation: output content classification, unusual volume detection
│
├── Privilege Escalation via AI
│     User asking AI to act beyond their authorized scope
│     Mitigation: scope enforcement in tool permissions, action authorization
│
└── Shadow AI
      AI use outside platform visibility (personal API keys, local models)
      Mitigation: network egress controls, license monitoring
```

---

## Data Model

```yaml
SecurityEvent:
  id: UUID
  event_type: enum[PromptInjection, IndirectInjection, DataExfiltration,
                   JailbreakAttempt, AbusePattern, UnauthorizedAccess,
                   AnomalousBehavior, PolicyViolation]
  severity: enum[Informational, Low, Medium, High, Critical]
  artifact_id: ArtifactRef
  tenant_id: TenantRef
  user_id: UserRef
  timestamp: datetime
  raw_content: encrypted_blob   # for forensics, never logged in plaintext
  detection_rule: SecurityRuleRef
  confidence_score: float
  disposition: enum[Blocked, Allowed, Flagged, Quarantined, Escalated]
  investigation_status: enum[New, InProgress, Resolved, FalsePositive]
  siem_event_id: string         # cross-reference to enterprise SIEM

SecurityProfile:
  artifact_id: ArtifactRef
  security_classification: enum[Public, Internal, Confidential, Restricted, TopSecret]
  access_controls: AccessControlList
  security_controls_applied: SecurityControl[]
  threat_model: ThreatModelRef
  last_security_review: datetime
  security_incidents: SecurityEventRef[]
  injection_risk_score: float   # 0.0 – 10.0 from security assessment
```

---

## Detection Capabilities

| Threat | Detection Method | Action |
|--------|----------------|--------|
| Prompt injection | ML classifier + rule matching | Block + audit + alert |
| RAG poisoning | Content scanning at retrieval | Strip + audit + alert |
| Jailbreak attempt | Pattern library + semantic matching | Block + audit |
| Data exfiltration | Output volume + content classification | Flag + audit + alert |
| Model abuse | Rate pattern + query sequence analysis | Throttle + alert |
| Anomalous tool calls | Baseline deviation detection | Flag + alert |

---

## Services Exposed

| Method | Signature | SLA |
|--------|-----------|-----|
| EvaluateSecurityContext | `(request) → SecurityDecision` | P99 < 5ms (inline) |
| LogSecurityEvent | `(event) → EventRecord` | Fire-and-forget |
| GetSecurityProfile | `(artifact) → SecurityProfile` | P99 < 200ms |
| ClassifyContent | `(content) → ContentClassification` | P99 < 50ms |
| GetSecurityIncidents | `(scope, period) → SecurityIncident[]` | P99 < 500ms |
| UpdateThreatModel | `(artifact, threat_model) → ThreatModelVersion` | Async |
| RunSecurityAssessment | `(artifact) → SecurityAssessmentReport` | Async |

---

## SIEM Integration

All security events are forwarded to the enterprise SIEM in real-time:
- Event schema conforms to CEF (Common Event Format) and OCSF (Open Cybersecurity Schema)
- Critical and High severity events trigger automated SIEM alerting
- Security Operations Center receives AI-specific event context (prompt context, not content)

---

## Extension Points

- Custom detection rules for industry-specific threat patterns
- External threat intelligence feed integration
- Custom content classifiers for proprietary data types (e.g., deal room documents)
- Custom disposition logic for MNPI detection
