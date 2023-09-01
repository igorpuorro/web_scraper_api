import pandas as pd

from app.presenter.base_presenter import BasePresenter


class KeywordPresenter(BasePresenter):
    def format_summary(self, summary: dict) -> dict:
        df_result: pd.DataFrame
        result_data: list = []

        try:
            for key, values in summary.items():
                count = len(values)
                min_value = min(values)
                max_value = max(values)
                average = sum(values) / count

                result_data.append(
                    {
                        "keyword": key,
                        "count": count,
                        "min": min_value,
                        "max": max_value,
                        "average": average,
                    }
                )

            df_result = pd.DataFrame(result_data)

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error

        return df_result.to_dict()
