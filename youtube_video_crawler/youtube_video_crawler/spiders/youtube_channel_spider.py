import os
import scrapy


class YoutubeChannelSpider(scrapy.Spider):
    name = 'youtube_channel_spider'

    @staticmethod
    def read_channel_urls_from_file():
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_dir, 'channel_urls.txt')
        print file_path
        with open(file_path, 'r') as f:
            urls = f.readlines()
        return urls

    def start_requests(self):
        channel_urls = YoutubeChannelSpider.read_channel_urls_from_file()
        for url in channel_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print response.url
