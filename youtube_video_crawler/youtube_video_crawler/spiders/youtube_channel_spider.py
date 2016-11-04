import os
import json
import scrapy
from lxml import etree


class YoutubeChannelSpider(scrapy.Spider):
    name = 'youtube_channel_spider'
    youtube_url = 'https://www.youtube.com'

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
        channel_url = response.url
        return self.extract_video_url(response, channel_url, False)

    def parse_more_json(self, response):
        channel_url = response.meta['channel_url']
        return self.extract_video_url(response, channel_url, True)

    def extract_video_url(self, response, channel_url, is_parsing_html):
        if is_parsing_html:
            json_data = json.loads(response.body)
            content_html = json_data['content_html']
            response = etree.HTML(content_html)
            more_button_html = json_data['load_more_widget_html']
            if more_button_html:
                more_button_tree = etree.HTML(more_button_html)

        html_lis = response.xpath('//li[contains(@class, "channels-content-item yt-shelf-grid-item")]')
        for html_li in html_lis:
            if is_parsing_html:
                video_url = html_li.xpath('div/div/div[contains(@class, "yt-lockup-content")]/h3/a/@href')[0]
            else:
                video_url = html_li.xpath('div/div/div[contains(@class, "yt-lockup-content")]/h3/a/@href').extract()[0]
            yield {
                'video_url': YoutubeChannelSpider.youtube_url + video_url,
                'channel_url': channel_url
            }
            if is_parsing_html and more_button_html:
                more_button = more_button_tree.xpath('//button[boolean(@data-uix-load-more-href)]')
                if more_button:
                    more_button_url = more_button_tree.xpath('//button/@data-uix-load-more-href')[0]
                    more_button_url = YoutubeChannelSpider.youtube_url + more_button_url
                    request = scrapy.Request(url=more_button_url, callback=self.parse_more_json)
                    request.meta['channel_url'] = channel_url
                    yield request
            else:
                more_button = response.xpath('//button[boolean(@data-uix-load-more-href)]')
                if more_button:
                    more_button_url = response.xpath('//button/@data-uix-load-more-href').extract()[0]
                    more_button_url = YoutubeChannelSpider.youtube_url + more_button_url
                    request = scrapy.Request(url=more_button_url, callback=self.parse_more_json)
                    request.meta['channel_url'] = channel_url
                    yield request
