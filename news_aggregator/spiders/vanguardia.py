import scrapy

class LaVanguardiaSpider(scrapy.Spider):
    name = "vanguardia"
    allowed_domains = ["lavanguardia.com"]
    start_urls = ["https://www.lavanguardia.com/"]

    def clean(self, text):
        return text.strip() if text else ""

    def parse(self, response):
        for article in response.css("article h2 a")[:15]:
            title = self.clean(article.css("::text").get())
            url = article.attrib.get("href")

            if url and not url.startswith("http"):
                url = response.urljoin(url)

            yield scrapy.Request(url, callback=self.parse_article, meta={"title": title})

    def parse_article(self, response):
        title = response.meta["title"]
        date = self.clean(response.css("time::attr(datetime)").get())
        author = self.clean(response.css("span.author-name::text").get())
        source = "La Vanguardia"

        yield {
            "title": title,
            "date": date or "",
            "author": author or "",
            "source": source
        }
