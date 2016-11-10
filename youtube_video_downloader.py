# Eric 2016/11/09
from __future__ import unicode_literals
import youtube_dl
import mysql.connector

conn = mysql.connector.connect(user='taloscar', password='taloscar', database='taloscar', host='10.161.23.57')
cursor = conn.cursor()


def get_to_download_video_urls():
    urls_with_ids = query_from_mysql()
    for url_with_id in urls_with_ids:
        download_video(url_with_id[0], url_with_id[1])


def download_video(video_url, video_id):
    ydl_opts = {
        'verbose': True,
        'ignoreerrors': True,
        'noplaylist': True,
        'sleep_interval': 10,
        'max_sleep_interval': 20,
        'outtmpl': '/home/youtube_videos/' + str(video_id) + '.mp4',
        'progress_hooks': [output_log]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print 'start to download: ' + str(video_id)
        ydl.download([video_url])


def query_from_mysql():
    try:
        cursor.execute('select video_url, id from youtube_video where is_downloaded = 0')
        rows = cursor.fetchall()
        urls_with_ids = [(row[0], row[1]) for row in rows]
        return urls_with_ids

    except Exception as e:
        print 'Exception when query from mysql: ' + e.message
        return []


def output_log(d):
    if d['status'] == 'finished':
        print('Done downloading: ' + d['filename'])
        log_mysql_for_finished_video(d['filename'])
    elif d['status'] == 'error':
        print('Error downloading: ' + d['filename'])


def log_mysql_for_finished_video(video_name):
    dot_position = video_name.rfind('.')
    slash_position = video_name.rfind('/')
    if dot_position != -1 and slash_position != -1:
        video_id = video_name[slash_position + 1: dot_position]
        if video_id and video_id != '':
            modify_downloaded_field_mysql(video_id)


def modify_downloaded_field_mysql(video_id):
    try:
        cursor.execute('update youtube_video set is_downloaded = 1 where id = %(video_id)s', {'video_id': int(video_id)})
        conn.commit()

    except Exception as e:
        print 'Exception when modify downloaded filed mysql: ' + e.message
        return []


def close_mysql():
    cursor.close()
    conn.close()

if __name__ == '__main__':
    get_to_download_video_urls()
    close_mysql()

