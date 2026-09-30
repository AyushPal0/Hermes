import pytest

from app.services.agent.planner import ResearchPlanner


@pytest.mark.asyncio
async def test_agent_planner():

    planner = ResearchPlanner()

    plan = await planner.create_plan(
        question=(
            "How is generative AI "
            "transforming software development?"
        ),
        depth="deep",
    )

    assert plan
    assert len(plan) <= 5

    for question in plan:

        assert isinstance(
            question,
            str,
        )

        assert len(question) > 10