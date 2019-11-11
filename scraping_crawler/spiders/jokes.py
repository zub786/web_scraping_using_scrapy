import scrapy
from scrapy.loader import ItemLoader
from scraping_crawler.items import JokeItem

class JokesSpider(scrapy.Spider):


    name="jokes"
    start_urls=[
    "http://www.laughfactory.com/jokes/family-jokes"
    ]


    def parse(self, response):

        for joke in response.xpath("//div[@class='jokes']"):
            l=ItemLoader(JokeItem(), selector=joke)
            l.add_xpath('joke_text', "//div[@class='joke-text']/p")
            l.add_xpath('likes', "//div[@class='likes-dislikes-count']/a/span")


            # Manual way to load item
            # yield {
            # 'joke_text': joke.xpath("//div[@class='joke-text']/p/text()").extract_first(),
            # 'likes': joke.xpath("//div[@class='likes-dislikes-count']/a/span/text()").extract_first()
            # }

            # Scrapy way to load item
            yield l.load_item()
        next_page=response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_page is not None:
            next_page_link=response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
