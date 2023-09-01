from typing import Union

from bs4 import BeautifulSoup, NavigableString, Tag

from app.extractor.job_search_extractor import JobSearchExtractor


class JobSearchGlassdoorExtractor(JobSearchExtractor):
    def extract_job_description(self) -> None:
        div_element: Union[Tag, NavigableString, None]

        soup_page = BeautifulSoup(self.content, "html.parser")
        div_element = soup_page.find(
            "div", id="JobDescriptionContainer"
        )

        if isinstance(div_element, Tag):
            self.content = div_element.get_text()
