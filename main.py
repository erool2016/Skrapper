from bs4 import BeautifulSoup

import requests
from requests.exceptions import Timeout, ConnectionError
import db
class Astronews:
    def __init__(self, link):
        self.link = link

    def get_soup_obj(self,link=None):
        '''Получаем Soup obj по указанной ссыдке. декодируем'''
        try:
            resp = requests.get(link)
            resp.encoding = 'cp1251'
            soup = BeautifulSoup(resp.text, features='lxml')
        except Timeout as  e:
            print(e)
            self.start_program()
        except  ConnectionError as e:
            print(e)
            self.start_program()
        except :
            print('Указанная ссылка не существует')
            self.start_program()
        else:
            return soup

    def get_info(self) -> list:
        '''Получаем новости из Soup obj'''
        obj = self.get_soup_obj(self.link)
        news = obj.find_all('div', class_='col')
        return news
    def create_link(self,link:str) -> str:
        '''Создаем ссылку на статью'''
        return f'{self.link}{link.find("a", class_="name").get("href").strip("/")}/'

    def get_text(self,link:str) -> str:
        '''Получаем текст статьи по ссылке'''
        try:
            soup = self.get_soup_obj(link)
            text = soup.find('div', class_='news-page').find_all('p')[1].text
        except Timeout as  e:
            print(e)
            self.start_program()
        except  ConnectionError as e:
            print(e)
            self.start_program()
        except :
            print('Указанная ссылка не существует')

        else:
            return text


    def create_info_for_table(self, news_block :BeautifulSoup) -> dict:
        '''Создаем словарь с информацией о новости'''
        info_for_save = {
            'title_': news_block.find('a', class_='name').find('img').get('title'),
            'link': self.create_link(news_block),
            'data': news_block.find('div', class_='date').text
            }

        info_for_save["text"] = self.get_text(info_for_save['link'])

        return info_for_save


    def make_dict(self)->list:
        '''Создаем список словарей с информацией о новостях'''
        list_info=[]
        for news in self.soup_news:
            list_info.append(self.create_info_for_table(news))

        return list_info
    def send_message(message:str):
        print(message)

    def create_list_for_save_bd(self)->list:
        '''Проверяем отсутствие новости в бд и формируем список словарей с новостями'''
        list_for_save_bd_ = []
        print(self.list_info)
        for item in self.list_info:
            # print(type(item['link']))
            if db.Table.check_link(item['link']) is None:
                list_for_save_bd_.append(item)
                print(f'Ссылка {item["link"]} в бд нет')

            else:
                print(f'Ссылка {item["link"]} в бд есть')

        return list_for_save_bd_

    def send_news_for_db(self):
        '''Отправляем новости в бд'''
        print(self.list_for_save_bd)
        if self.list_for_save_bd:
            print('Отправляем новости в бд')
            for item in self.list_for_save_bd:
                db.Table.add_news(item)
        else:
            print('Новостей нет')


    def start(self):
        '''Запуск сбори информации'''
        self.soup_news = self.get_info()

        self.list_info = self.make_dict()
        self.list_for_save_bd = self.create_list_for_save_bd()
        #print(list_for_save_bd)
        self.send_news_for_db()

def start_program():
    while True:
        print('1 - https://www.astronews.ru/\n0 - exit')
        choice = int(input())
        if choice == 1:
            a = Astronews('https://www.astronews.ru/')
            a.start()
        if choice == 0:
            print('до свидания')
            break


if __name__ == '__main__':
    # db.Table.create_table()
    #db.Table.drop_table()
    # a = Astronews('https://www.astronews.ru/')
    start_program()
    # # while True:
    #     print('1 - https://www.astronews.ru/\n0 - exit')
    #     choice = int(input())
    #     if choice == 1:
    #         a = Astronews('https://www.astronews.ru/')
    #         a.start()
    #     if choice == 0:
    #         print('до свидания')
