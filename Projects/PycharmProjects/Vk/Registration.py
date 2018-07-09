import json
import urllib
from urllib.request import urlopen
import sqlite3
def start(message):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    sql = "SELECT token FROM users WHERE id_in_telegram=?"
    cursor.execute(sql, [(str(message.chat.id))])

    rew = cursor.fetchall()
    conn.commit()
    if len(rew[:]) != 0:
        for d in rew:
            return d[0]
       
    else:

        return "0"


def start1(message):

        c = message.text.split('=')
        res = urllib.request.urlopen(
            'https://oauth.vk.com/access_token?client_id=6618701&client_secret=xi4JsMlSbAmADaZt31zn&redirect_uri=https://oauth.vk.com/blank.html&code=' +
            c[-1])
        data = json.load(res)

        token = data['access_token']
        idT = str(message.chat.id)
        conn = sqlite3.connect("vk.db")
        cursor = conn.cursor()

        a = [(idT,token)]
        cursor.executemany("INSERT INTO users VALUES (?,?)", a)

        conn.commit()


