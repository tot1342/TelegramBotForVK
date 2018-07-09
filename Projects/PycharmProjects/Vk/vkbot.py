import vk

def chats(token):
    session = vk.AuthSession(access_token = token )
    vk_api = vk.API(session)

    data = vk_api.messages.getConversations(count = 15,  v = 5.80)
    Name = {}

    for a in range(0,14):
        if data['items'][a]['conversation']['peer']['type'] == 'chat':
            Name[data['items'][a]['conversation']['chat_settings']['title']] =  data['items'][a]['conversation']['peer']['id']
        else:
            name_users = vk_api.users.get(user_ids=data['items'][a]['conversation']['peer']['id'], fields='first_name,last_name',
                         v=5.80)[0]
            Name[(name_users['first_name'] + ' ' + name_users['last_name'])]= data['items'][a]['conversation']['peer']['id']
    return Name

def token(id_chat):
    import sqlite3
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    sql = "SELECT token, chat FROM users WHERE id_in_telegram=?"
    cursor.execute(sql, [(str(id_chat))])
    rew = cursor.fetchall()
    for d in rew:
        return (d)
    conn.commit()

