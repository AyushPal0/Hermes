import json

from app.services.llm.ollama_client import OllamaClient


class ResearchPlanner:

    def __init__(self):
        self.llm = OllamaClient()

    async def create_plan(
        self,
        question: str,
        depth: str = "deep",
    ) -> list[str]:

        if depth == "quick":
            max_sub_questions = 3

        elif depth == "academic":
            max_sub_questions = 7

        else:
            max_sub_questions = 5

        prompt = f"""
You are a research planning agent.

Your job is to break a complex research question
into smaller, independent research questions.

Original research question:
{question}

Research depth:
{depth}

Create up to {max_sub_questions} focused
sub-questions.

The sub-questions should:

1. Cover different important aspects of the topic.
2. Be specific enough to search on the web.
3. Avoid unnecessary overlap.
4. Help produce a comprehensive research answer.
5. Be written as complete questions.

Return ONLY valid JSON.

Use exactly this format:

[
    "sub-question 1",
    "sub-question 2",
    "sub-question 3"
]
"""

        response = await self.llm.generate(prompt)

        try:
            plan = json.loads(response)

        except json.JSONDecodeError:
            return [
                line.strip("- ").strip()
                for line in response.splitlines()
                if line.strip()
            ][:max_sub_questions]

        if not isinstance(plan, list):
            raise ValueError(
                "Research planner returned invalid format."
            )

        return [
            str(item).strip()
            for item in plan
            if str(item).strip()
        ][:max_sub_questions]