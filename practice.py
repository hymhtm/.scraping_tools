import asyncio
from crawlee import PlaywrightCrawler, PlaywrightCrawlingContext

async def main():
    crawler = PlaywrightCrawler(
        max_request_per_crawl = 50
    )
    
    @crawler.router.default_handler
    async def default_handler(context: PlaywrightCrawlingContext):
        await context.request.get("https://www.google.com")

if __name__ == "__main__":
    asyncio.run(main())
