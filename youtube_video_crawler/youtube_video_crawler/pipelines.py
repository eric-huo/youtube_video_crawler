# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class YoutubeVideoCrawlerPipeline(object):
    video_url_num = 0

    def close_spider(self, spider):
        print YoutubeVideoCrawlerPipeline.video_url_num

    def process_item(self, item, spider):
        YoutubeVideoCrawlerPipeline.video_url_num += 1
        return item