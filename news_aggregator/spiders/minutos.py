import scrapy

class VeinteMinutosSpider(scrapy.Spider):
    name = "minutos"
    allowed_domains = ["20minutos.es"]
    start_urls = ["https://www.20minutos.es/"]

    def clean(self, text):
        return text.strip() if text else ""

    def parse(self, response):
        for article in response.css("article h2 a"):
            title = self.clean(" ".join(article.css("::text").getall()))
            url = article.attrib.get("href")

            if url and not url.startswith("http"):
                url = response.urljoin(url)

            yield scrapy.Request(url, callback=self.parse_article, meta={"title": title})

    def parse_article(self, response):
        title = response.meta["title"]
        date = self.clean(response.css("time::attr(datetime)").get())
        author = self.clean(response.css("span.author-name::text").get())
        source = "20 Minutos"

        yield {
            "title": title,
            "date": date or "",
            "author": author or "",
            "source": source
        }
