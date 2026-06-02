"""
Evaluation SDK module for CI/CD integration.

Provides EvaluationRunner for running governance evaluations as part of
automated pipelines and deployment gates.
"""


class EvaluationRunner:
    """
    Run governance evaluations from CI/CD pipelines.

    Example:
        runner = EvaluationRunner(client)
        result = await runner.run(
            artifact_id="my-agent-id",
            benchmark_ids=["safety-v1", "factual-accuracy-v2"],
            fail_on_regression=True,
        )
        if not result.passed:
            sys.exit(1)
    """

    def __init__(self, client: "GovernanceClient") -> None:  # noqa: F821
        self._client = client

    async def run(
        self,
        artifact_id: str,
        benchmark_ids: list[str] | None = None,
        fail_on_regression: bool = True,
    ) -> "EvaluationRunResult":  # noqa: F821
        """Submit evaluation job and wait for completion."""
        job = await self._client.http.post(
            "/v1/evaluations/run",
            json={
                "artifact_id": artifact_id,
                "benchmark_ids": benchmark_ids,
            },
        )
        return await self._poll_job(job["job_id"])

    async def _poll_job(self, job_id: str) -> "EvaluationRunResult":  # noqa: F821
        import asyncio
        while True:
            status = await self._client.http.get(f"/v1/evaluations/{job_id}")
            if status["state"] in ("completed", "failed"):
                return status
            await asyncio.sleep(5)
