import scrapy


class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        "https://www.amazon.com/s?k=processors&rh=n%3A193870011&ref=nb_sb_noss"
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'test-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
