import mysql.connector

conn = mysql.connector.connect(user='taloscar', password='taloscar', database='taloscar', host='10.161.23.57')
cursor = conn.cursor()


def insert_video_table_foreign_key():
    channel_url_with_ids = get_channel_url_id_dict()
    sql = 'select id, channel_url from youtube_video'
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        id = row[0]
        channel_url = row[1]
        channel_id = get_channel_id_from_url(channel_url, channel_url_with_ids)
        if channel_id:
            insert_channel_id_to_video(channel_id, id)


def get_channel_url_id_dict():
    sql = 'select * from youtube_channel'
    cursor.execute(sql)
    rows = cursor.fetchall()
    channel_url_with_ids = [(row[0], row[1]) for row in rows]
    return channel_url_with_ids


def get_channel_id_from_url(channel_url, channel_url_with_ids):
    for channel_url_with_id in channel_url_with_ids:
        url = channel_url_with_id[1]
        id = channel_url_with_id[0]
        if url == channel_url or url == channel_url[0: len(channel_url) - 3]:
            return id
    return None


def insert_channel_id_to_video(channel_id, id):
    sql = 'update youtube_video set channel_id = ' + str(channel_id) + ' where id = ' + str(id)
    cursor.execute(sql)
    conn.commit()


if __name__ == '__main__':
    insert_video_table_foreign_key()
    cursor.close()
    conn.close()

