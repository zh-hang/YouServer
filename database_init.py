import sqlite3

conn = sqlite3.connect('./instance/you.db')

print("Opened database successfully")
c = conn.cursor()
c.execute('''CREATE TABLE chatroom (chatroom_id int primary key not null,chatroom_name text not null);''')
c.execute('''INSERT INTO chatroom (chatroom_id,chatroom_name) VALUES (0,'TEST')''')
c.execute('''INSERT INTO chatroom (chatroom_id,chatroom_name) VALUES (1,'YOU')''')
print("table chatroom create successfully")
c.execute(
    '''CREATE TABLE user
    (user_tel int primary key not null,
    user_name text not null,
    user_password text not null,
    user_avatar_url text not null);''')
print("table user create successfully")
conn.commit()
conn.close()
