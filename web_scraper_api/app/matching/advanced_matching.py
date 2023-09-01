import re
from thefuzz import fuzz

from app.matching.base_matching import BaseMatching


class AdvancedMatching(BaseMatching):
    def _sanitize(self, input_string: str) -> str:
        # Remove empty lines
        non_empty_lines = [
            line for line in input_string.split("\n") if line.strip()]
        filtered_lines = []

        for line in non_empty_lines:
            # Replace 2 or more spaces with a single space
            filtered_line = re.sub(r" {2,}", " ", line)
            filtered_lines.append(filtered_line)

        return "\n".join(filtered_lines)

    def match_with_sentences(self, sentences: list, keywords: list, threshold: int = 90) -> dict:
        summary: dict = {}

        try:
            for sentence in sentences:
                sanitized_token = self._sanitize(sentence)

                for keyword in keywords:
                    if len(keyword) < 3:
                        continue

                    ratio = fuzz.partial_ratio(
                        sanitized_token.lower(), keyword.lower())

                    if ratio >= threshold:
                        if keyword in summary:
                            summary[keyword].append(ratio)
                        else:
                            summary[keyword] = [ratio]

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error

        return summary
