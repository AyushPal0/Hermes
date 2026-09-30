import pytest

from app.services.agent.planner import ResearchPlanner


@pytest.mark.asyncio
async def test_research_planner():

    planner = ResearchPlanner()

    questions = await planner.create_plan(
        "How is generative AI transforming software development?"
    )

    assert questions
    assert len(questions) <= 5

    for question in questions:
        assert isinstance(question, str)
        assert question.strip()

    print("\nRESEARCH PLAN:")

    for index, question in enumerate(
        questions,
        start=1,
    ):
        print(f"{index}. {question}")