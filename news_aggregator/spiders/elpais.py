import scrapy

class ElPaisSpider(scrapy.Spider):
    name = "elpais"
    allowed_domains = ["elpais.com"]
    start_urls = ["https://elpais.com/"]

    def clean(self, texto):
        return texto.strip() if texto else ''

    def parse(self, response):
        # Recorremos artículos de portada
        for article in response.css("article h2 a"):
            title = self.clean(article.css("::text").get())
            url = article.attrib.get("href")
            if not url.startswith("http"):
                url = response.urljoin(url)

            # Pasamos al artículo individual para sacar fecha y autor
            yield scrapy.Request(url, callback=self.parse_article, meta={"title": title})

    def parse_article(self, response):
        title = response.meta["title"]
        date = self.clean(response.css("time::attr(datetime)").get())
        author = self.clean(response.css("span[class*='author']::text").get())
        source = "El País"

        yield {
            "title": title,
            "date": date or "",
            "author": author or "",
            "source": source
        }
