from stack.items import StackItem
from scrapy import Spider, selector


class StackSpider(Spider):
    # name defines the name of spider
    name = "stack"
    # for baseurl for allowed-domains for spider to crawl
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest", ]
    # start-urls for list of urls for spider to start crawling from
    # All subsequent URLs will start from the data that the spider downloads from the
    # URLS in start_urls.

    def parse(self, response):
        #print("I am in parse function")
        questions = response.xpath('//div[@class="summary"]/h3')
        print("Checking whether xpath is valid or not")

        for question in questions:
            #print("I am in for loop of parse function")
            item = StackItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item
