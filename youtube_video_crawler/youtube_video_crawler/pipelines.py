import mysql.connector
import time

from insert_channel_table import get_channel_url_id_dict, get_channel_id_from_url


class YoutubeVideoCrawlerPipeline(object):

    def __init__(self):
        self.conn = mysql.connector.connect(user='taloscar', password='taloscar', database='taloscar', host='10.161.23.57')
        self.cursor = self.conn.cursor()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        video_url = item['video_url']
        channel_url = item['channel_url']
        channel_url_with_id = get_channel_url_id_dict()
        channel_id = get_channel_id_from_url(channel_url, channel_url_with_id)

        if channel_id:
            update_time = int(round(time.time() * 1000))
            print update_time
            try:
                self.cursor.execute('select * from youtube_video where channel_id = "' + str(channel_id) +
                                    '" and video_url = "' + video_url + '";')
                row = self.cursor.fetchone()
                if row:
                    print 'record existed'
                else:
                    sql = 'insert into youtube_video (channel_id, video_url, update_time) values (%s, %s, %s)'
                    self.cursor.execute(sql, (channel_id, video_url, update_time))
                    self.conn.commit()
                    print 'record inserted'

            except Exception as e:
                print 'exception when mysql operation'
                print e
        return item

