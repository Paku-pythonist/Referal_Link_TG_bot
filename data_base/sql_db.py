import time
import sqlite3 as sql


# ++++++++++++++++++++++++++++++++++ Запуск БД +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def sql_start():
    global base, cur
    base = sql.connect('super_link.db')   # Подкл. к сущ-й базе, иначе созд. нов.
    cur = base.cursor()                   # Оператор CRUD операций.
    if base:
        print('Data base connected OK!')

    base.execute('CREATE TABLE IF NOT EXISTS users(_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, '
                 'first_name TEXT, username TEXT, link_amount INT, registration_time TEXT)')
    base.commit()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# ++++++++++++++++++++++++++++++++++ Добавление нового пользователя в БД +++++++++++++++++++++++++++++++++++++++++++++++
async def add_new_user(params):
    if params['check'] == 'creator':
        new_user_id = params["creator_user_id"]
        new_user_first_name = params["creator_first_name"]
        new_user_username = params["creator_user_username"] if params["creator_user_username"] else params["creator_first_name"]
    if params['check'] == 'invited':
        new_user_id = params["invited_user_id"]
        new_user_first_name = params["invited_user_first_name"]
        new_user_username = params["invited_user_username"] if params["invited_user_username"] else params["invited_user_first_name"]

    result = cur.execute(
        f'SELECT * FROM users WHERE user_id = {new_user_id}').fetchall()   # Проверка на наличие в базе.

    if not bool(len(result)):
        data = tuple([new_user_id, new_user_first_name, new_user_username, 0, time.time()])

        cur.execute(
            'INSERT INTO users (user_id, first_name, username, link_amount, registration_time) '
            'VALUES (?, ?, ?, ?, ?)', data)   # Защита от SQL-инъекций.
        base.commit()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



async def add_point(params: dict):
    try:
        if cur.execute(f'SELECT * FROM users WHERE user_id = {params["creator_user_id"]}').fetchall() == []:
            print('Add link creator id=', params["creator_user_id"])
            params['check'] = 'creator'
            await add_new_user(params)
        else:
            print('Link creator already exists id=', params["creator_user_id"])

        if cur.execute(f'SELECT * FROM users WHERE user_id = {params["invited_user_id"]}').fetchall() != []:
            print('Этого юзера его уже приглашали, балл не засчитан.')
        else:
            link_amount = cur.execute(
                f'SELECT link_amount FROM users WHERE user_id = {params["creator_user_id"]}').fetchall()

            if type(link_amount[0][0]) == int:
                cur.execute(
                    f'UPDATE users SET link_amount = {link_amount[0][0] + 1} WHERE user_id = {params["creator_user_id"]}')
                base.commit()
                print('Add id=', params["creator_user_id"], ' + ball')
            else:
                print(f'__error.add_point.link_amount: none digit: ({link_amount}->{link_amount[0][0]})')

    except Exception as ex:
        print('__error.sql.add_point:', ex)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



async def get_info():
    return cur.execute('SELECT user_id, first_name, username, link_amount FROM users ').fetchall()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



async def get_top_200():
    return cur.execute('SELECT user_id, first_name, username, link_amount FROM users '
                       'ORDER BY link_amount desc LIMIT 200').fetchall()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++