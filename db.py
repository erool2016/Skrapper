import psycopg2

conn = psycopg2.connect(database='db1', user='postgres', password='qwr1d')

class Table:

    def create_table():
        with conn.cursor() as cur:
            cur.execute('''
                create table if not exists astronews(
                    id serial primary key,
                    title varchar(255),
                    link varchar(100),
                    data varchar(30),
                    text text
                );
                ''')
            conn.commit()
        print('создана таблица astronews')

    def drop_table():
        with conn.cursor() as cur:
            cur.execute('''
                                drop table astronews;

                            '''
                        )
        conn.commit()
        print('удалена таблица astronews')

    def check_link(link:str):
        print(link)
        with conn.cursor() as cur:
            cur.execute('''
                    select id from astronews where link = %s;
                ''', (link,))
            a = cur.fetchone()

            return a
    def add_news(dict):
        with conn.cursor() as cur:
            cur.execute('''
                    insert into astronews(title, link, data, text) values (%s, %s, %s, %s);
                ''', (dict['title_'], dict['link'], dict['data'], dict['text']))
        conn.commit()
        print(f'добавлена новость - {dict["title_"]}')