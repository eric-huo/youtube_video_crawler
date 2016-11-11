import os

import mysql.connector

conn = mysql.connector.connect(user='taloscar', password='taloscar', database='taloscar', host='10.161.23.57')
cursor = conn.cursor()


def update_channel_priority():
    channel_url_with_priority = read_from_file()
    for data in channel_url_with_priority:
        channel_url = data['url']
        priority = data['priority']
        update_mysql(channel_url, priority)


def read_from_file():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(file_dir, 'channel_url_with_priority.txt')
    channel_url_with_priority = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            channel_url = line.split(',')[0]
            priority = line.split(',')[1]
            channel_url_with_priority.append({
                'url': channel_url,
                'priority': priority
            })
    return channel_url_with_priority


def update_mysql(channel_url, priority):
    cursor.execute('update youtube_channel set priority = ' + priority + ' where channel_url = "' + channel_url + '";')
    conn.commit()


if __name__ == '__main__':
    update_channel_priority()
    cursor.close()
    conn.close()
