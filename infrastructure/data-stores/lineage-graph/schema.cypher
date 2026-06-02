// Lineage Graph Schema — Neo4j / Amazon Neptune
// Records the provenance of every AI execution output
// Enables forensic traceability: AI output → model → prompt → data → governance decisions

// ── NODE LABELS ──────────────────────────────────────────────────────────────

// ArtifactNode: represents a versioned AI artifact at a specific point in time
// Properties: artifact_id, artifact_type, version, snapshot_timestamp, tenant_id
CREATE CONSTRAINT artifact_node_id FOR (n:ArtifactNode) REQUIRE n.artifact_id IS UNIQUE;

// ExecutionNode: represents a single AI execution (inference, tool call, workflow run)
// Properties: invocation_id, timestamp, tenant_id, session_id, latency_ms
CREATE CONSTRAINT execution_node_id FOR (n:ExecutionNode) REQUIRE n.invocation_id IS UNIQUE;

// DataNode: represents a dataset, document, or knowledge asset accessed during execution
// Properties: asset_id, asset_type, version, data_vintage, tenant_id
CREATE CONSTRAINT data_node_id FOR (n:DataNode) REQUIRE n.asset_id IS UNIQUE;

// UserNode: represents the user who initiated an execution
// Properties: user_id, tenant_id, authorization_snapshot (at time of execution)
CREATE CONSTRAINT user_node_id FOR (n:UserNode) REQUIRE n.user_id IS UNIQUE;

// OutputNode: represents an AI output (response, analysis, decision support)
// Properties: output_id, output_type, timestamp, tenant_id
CREATE CONSTRAINT output_node_id FOR (n:OutputNode) REQUIRE n.output_id IS UNIQUE;

// GovernanceStateNode: snapshot of governance state at a specific execution time
// Properties: snapshot_id, policy_decision_id, risk_score, compliance_status, timestamp
CREATE CONSTRAINT governance_state_id FOR (n:GovernanceStateNode) REQUIRE n.snapshot_id IS UNIQUE;

// ── RELATIONSHIP TYPES ───────────────────────────────────────────────────────

// (ExecutionNode)-[:PRODUCED]->(OutputNode)
// An execution produced an output

// (ExecutionNode)-[:USED_AGENT]->(ArtifactNode {artifact_type: "Agent"})
// The execution used this specific version of this agent

// (ExecutionNode)-[:CALLED_MODEL]->(ArtifactNode {artifact_type: "Model"})
// Properties: model_version_at_call_time

// (ExecutionNode)-[:USED_PROMPT]->(ArtifactNode {artifact_type: "Prompt"})
// Properties: prompt_version_at_call_time

// (ExecutionNode)-[:ACCESSED_DATA]->(DataNode)
// Properties: access_timestamp, documents_retrieved, relevance_scores

// (ExecutionNode)-[:CALLED_TOOL]->(ArtifactNode {artifact_type: "Tool"})
// Properties: call_timestamp, call_sequence, success, latency_ms

// (ExecutionNode)-[:INITIATED_BY]->(UserNode)
// Properties: authorization_level_at_time

// (ExecutionNode)-[:GOVERNED_BY]->(GovernanceStateNode)
// Links to the complete governance state snapshot for this execution

// (DataNode)-[:SOURCED_FROM]->(DataNode)
// Data provenance: knowledge asset sourced from dataset

// (ArtifactNode)-[:VERSION_OF]->(ArtifactNode)
// Version history: version 2 is a VERSION_OF version 1

// ── EXAMPLE LINEAGE QUERY ────────────────────────────────────────────────────

// "Explain the complete provenance of output O-123456"
//
// MATCH (output:OutputNode {output_id: 'O-123456'})
// MATCH (exec:ExecutionNode)-[:PRODUCED]->(output)
// MATCH (exec)-[:USED_AGENT]->(agent:ArtifactNode)
// MATCH (exec)-[:CALLED_MODEL]->(model:ArtifactNode)
// MATCH (exec)-[:USED_PROMPT]->(prompt:ArtifactNode)
// MATCH (exec)-[:ACCESSED_DATA]->(data:DataNode)
// MATCH (exec)-[:GOVERNED_BY]->(gov:GovernanceStateNode)
// RETURN output, exec, agent, model, prompt, COLLECT(data), gov

// "Which outputs were produced using model version X?"
//
// MATCH (exec:ExecutionNode)-[:CALLED_MODEL]->(model:ArtifactNode {
//     artifact_id: 'MODEL-ID',
//     version: '1.0.0'
// })
// MATCH (exec)-[:PRODUCED]->(output:OutputNode)
// RETURN output.output_id, exec.timestamp, exec.tenant_id
// ORDER BY exec.timestamp DESC

// "Impact analysis: which executions are affected if prompt P is changed?"
//
// MATCH (prompt:ArtifactNode {artifact_id: 'PROMPT-ID'})
// MATCH (exec:ExecutionNode)-[:USED_PROMPT]->(prompt)
// MATCH (exec)-[:USED_AGENT]->(agent:ArtifactNode)
// RETURN DISTINCT agent.artifact_id, agent.canonical_name, COUNT(exec) AS usage_count
// ORDER BY usage_count DESC
