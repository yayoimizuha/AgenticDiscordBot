# noinspection PyProtectedMember
from markitdown.converters._html_converter import HtmlConverter
import json
from bs4 import BeautifulSoup
from dataclasses import dataclass
from aiohttp import ClientSession
from scrapling.fetchers import AsyncStealthySession
from scrapling.engines.toolbelt.convertor import Response


@dataclass
class SearchResult:
    title: str
    link: str
    snippet: str


@dataclass
class WebSearchService:
    """A service for performing web searches."""

    def __init__(self):
        self.session = ClientSession(headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0"
        })
        self.html_converter = lambda html: HtmlConverter().convert_string(html_content=html).text_content

        # self.scrapling_session = AsyncStealthySession(solve_cloudflare=True, headless=False)

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        # self.scrapling_session.close()

    @staticmethod
    async def get_single_page(url: str) -> str:
        async with AsyncStealthySession(solve_cloudflare=True, headless=False) as scrapling_session:
            return (await scrapling_session.fetch(url)).html_content

    async def keyword_search(self, query: str, page: int = 0) -> list[SearchResult]:
        """Perform a keyword search and return results."""
        results: list[SearchResult] = []
        webpages: list[Response] = []
        # await self.scrapling_session.start()

        for idx in range(1):
            search_page: str = await (
                await self.session.get(
                    f"https://search.yahoo.co.jp/search?p={query.replace(' ', '+')}&b={(page + idx) * 10 + 1}"
                )).text()
            # print(search_page)
            __next_data__ = BeautifulSoup(search_page, 'lxml').find('script', {'id': '__NEXT_DATA__'}).get_text()
            search_result_json = json.loads(__next_data__)
            search_results = search_result_json['props']['pageProps']['initialProps']['pageData']['algos']
            # print(search_results)
            results.extend([SearchResult(title=self.html_converter(result['title']),
                                         link=result['url'],
                                         snippet=self.html_converter(result['description'])) for result in
                            search_results])
            async with AsyncStealthySession(solve_cloudflare=True, headless=False, max_pages=5) as scrapling_session:
                _webpages = []
                for webpage in search_results:
                    _webpages.append(scrapling_session.fetch(webpage['url']))
                webpages.extend(await asyncio.gather(*_webpages))

        return [SearchResult(title=result.title, link=result.link, snippet=self.html_converter(page.html_content))
                for result, page in zip(results, webpages)]


if __name__ == '__main__':
    import asyncio


    async def main():
        service = WebSearchService()
        results = await service.keyword_search("InfiniBand")
        for result in results:
            print(result)


    asyncio.run(main())
