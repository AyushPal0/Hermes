from dataclasses import dataclass


@dataclass
class SourceScore:
    score: float
    reasons: list[str]


class SourceScorer:
    """
    Scores the quality of a research source.

    The score is between 0 and 1.
    """

    def score(
        self,
        title: str,
        snippet: str,
        content: str,
        url: str,
    ) -> SourceScore:

        score = 0.0
        reasons = []

        # --------------------------------
        # 1. Content availability
        # --------------------------------

        content_length = len(content.strip())

        if content_length == 0:
            reasons.append("No content extracted")
        elif content_length < 500:
            score += 0.10
            reasons.append("Very short content")
        elif content_length < 2000:
            score += 0.20
            reasons.append("Limited content")
        elif content_length < 5000:
            score += 0.30
            reasons.append("Moderate content length")
        else:
            score += 0.40
            reasons.append("Substantial content")

        # --------------------------------
        # 2. Title quality
        # --------------------------------

        if title.strip():
            score += 0.10
            reasons.append("Has a meaningful title")

        # --------------------------------
        # 3. Search snippet
        # --------------------------------

        if snippet.strip():
            score += 0.10
            reasons.append("Has search context")

        # --------------------------------
        # 4. URL quality
        # --------------------------------

        url_lower = url.lower()

        trusted_domains = [
            ".edu",
            ".gov",
            ".org",
            ".ac.",
        ]

        if any(domain in url_lower for domain in trusted_domains):
            score += 0.20
            reasons.append("Potentially authoritative domain")
        else:
            score += 0.05

        # --------------------------------
        # 5. Content structure
        # --------------------------------

        if "\n" in content or ". " in content:
            score += 0.10
            reasons.append("Structured textual content")

        # --------------------------------
        # Normalize score
        # --------------------------------

        score = min(score, 1.0)

        return SourceScore(
            score=round(score, 3),
            reasons=reasons,
        )