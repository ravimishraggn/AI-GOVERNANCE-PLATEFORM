# ADR-005: Build vs. Buy Decisions

**Status:** Accepted
**Date:** 2026-05-31

## Decision Matrix

| Component | Decision | Rationale |
|-----------|---------|-----------|
| Policy Engine | **BUILD** | Must reflect firm-specific risk tolerance and regulations. Too much customization required. Strategic differentiator. |
| Audit Infrastructure | **BUILD** | Must meet firm-specific regulatory requirements. Third-party creates data sovereignty risk. |
| Metadata Registry | **BUILD** | Core to governance identity; must integrate tightly with all services. |
| Risk Scoring Engine | **BUILD** | Risk models are proprietary IP; customization need is extreme. |
| LLM Evaluation Framework | **INTEGRATE** | Open-source (RAGAS, LangSmith, Promptfoo) are mature. Build domain-specific benchmarks on top. |
| Enterprise SIEM | **BUY + INTEGRATE** | Splunk/Sentinel are mature; build the integration layer, not the SIEM. |
| GRC Platform | **BUY + INTEGRATE** | ServiceNow/Archer are investments in place; build connectors. |
| AI Observability (basic) | **INTEGRATE** | Arize AI, W&B provide technical monitoring. Build governance-specific signals on top. |
| Identity and Access | **BUY + INTEGRATE** | Enterprise SSO/directory is always in-place. Integrate; never replace. |
| Private Markets Benchmarks | **BUILD** | No vendor offers domain-specific PE/VC/Credit evaluation benchmarks. |

## Key Principles

1. **Build what is strategic**: Policy engines, audit trails, risk models, and compliance
   controls are governance's core value. These cannot be commoditized or outsourced.

2. **Integrate what is commodity**: SIEM, GRC, identity, APM are solved problems with
   mature solutions. Build integrations; do not rebuild.

3. **Buy time to build**: In Phase 1–2, use pragmatic solutions (even manual processes)
   for capabilities that will be built properly later. Do not let perfect governance
   infrastructure block initial governance coverage.

4. **Evaluate open-source before SaaS**: For evaluation infrastructure, open-source
   frameworks provide more flexibility and avoid vendor lock-in for a critical capability.
