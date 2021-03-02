import scrapy

from scrapy.loader import ItemLoader
from ..items import RbinternationalplItem
from itemloaders.processors import TakeFirst


class RbinternationalplSpider(scrapy.Spider):
	name = 'rbinternationalpl'
	start_urls = ['https://www.rbinternational.com.pl/aktualnosci/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="col-sm-12 news-bottom-line"]')
		for post in post_links:
			url = post.xpath('.//a[@class="fxf-btn fxf-subpage-btn-more"]/@href').get()
			date = post.xpath('./div[@class="news-date"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

		next_page = response.xpath('//a[@class="pagination-next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response, date):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="col-12 news"]//text()[normalize-space() and not(ancestor::h2 | ancestor::a[@class="fxf-btn fxf-subpage-btn-more"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=RbinternationalplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
