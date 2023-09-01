from typing import Union

from bs4 import BeautifulSoup, NavigableString, Tag

from app.extractor.job_search_extractor import JobSearchExtractor


class JobSearchLinkedInExtractor(JobSearchExtractor):
    def extract_job_description(self) -> None:
        div_element: Union[Tag, NavigableString, None]

        soup_page = BeautifulSoup(self.content, "html.parser")
        div_element = soup_page.find(
            "div", class_="description__text description__text--rich"
        )

        if isinstance(div_element, Tag):
            self.content = div_element.get_text()
