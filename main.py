# Импорты
import requests
from bs4 import BeautifulSoup as BSoup
from tabulate import tabulate
import config
import colorama
import os
from tqdm import tqdm

colorama.init(autoreset=True)

# Создаем нашу главную функцию get_data для получения данных
def get_data(nick):
    # Проверяем существование файла poshel_naxuy.txt
    if os.path.exists('poshel_naxuy.txt'):
        # Если он существует - то мы добавляем ключ к словарю BONDAY_COOKIES
        with open('poshel_naxuy.txt') as file:
            config.BONDAY_COOKIES['poshel_nahuy'] = file.read()

    else:
        # Ничего не делаем если файла нету
        pass

    # Проверяем существование Samiy_umniy.txt
    if os.path.exists('Samiy_umniy.txt'):
        # Если он существует - то мы добавляем ключ к словарю BONDAY_COOKIES
        with open('Samiy_umniy.txt') as file:
            config.BONDAY_COOKIES['Samiy_umniy?'] = file.read()

    else:
        # Ничего не делаем если файла нету
        pass

    # Создаем переменную с параметрами GET запроса к bonday
    params = {
        'abob': '8',
        'nick': nick,
        'type': 'minecraft',
        'opt': 'false1false1false1false1false',
    }

    # Отправляем GET запрос к https://bonday.xyz, отправляем что-бы сайт подумал что скрипт это человек

    requests.get('https://bonday.xyz',
                 headers=config.BONDAY_HEADERS,
                 cookies=config.BONDAY_COOKIES)

    # Отправляем GET запрос к https://bonday.xyz/vipchecker, отправляем что-бы сайт подумал что скрипт это человек

    requests.get('https://bonday.xyz/vipchecker',
                 cookies=config.BONDAY_COOKIES,
                 headers=config.BONDAY_HEADERS)

    # Отправляем GET запрос к https://bonday.xyz/inc/ebalo, отправляем что-бы сайт подумал что скрипт это человек

    requests.get('https://bonday.xyz/inc/ebalo',
                 params={'abob': '8', 'nick': nick, 'type': 'minecraft'},
                 cookies=config.BONDAY_COOKIES,
                 headers=config.BONDAY_HEADERS)

    # Отправляем GET запрос к https://bonday.xyz/checkerajax и записывает ответ в перменнную response

    response = requests.get('https://bonday.xyz/checkerajax',
                            params=params,
                            cookies=config.BONDAY_COOKIES,
                            headers=config.BONDAY_HEADERS)

    response_bonday_cookies = response.cookies.get_dict()

    print(colorama.Fore.BLUE + '[INFO] ' + colorama.Fore.GREEN + 'Получил новые COOKIE')

    # Проверяем существование файла poshel_naxuy.txt
    if os.path.exists('poshel_naxuy.txt'):
        # Если он существует - то мы его удаляем и создаем новый с новыми печеньками(cookie), при следующем запросе будут использоваться именно они
        os.remove('poshel_naxuy.txt')
        with open('poshel_naxuy.txt', 'a+') as file:
            file.write(response_bonday_cookies['poshel_nahuy'])
            print(colorama.Fore.BLUE + '[INFO] ' + colorama.Fore.GREEN + 'Записал: poshel_nahuy')

    else:
        # Если он не существует - то мы его создаем новый с новыми печеньками(cookie), при следующем запросе будут использоваться именно они
        with open('poshel_naxuy.txt', 'a+') as file:
            file.write(response_bonday_cookies['poshel_nahuy'])
            print(colorama.Fore.BLUE + '[INFO] ' + colorama.Fore.GREEN + 'Записал: poshel_nahuy')

    # Проверяем существование Samiy_umniy.txt
    if os.path.exists('Samiy_umniy.txt'):
        # Если он существует - то мы его удаляем и создаем новый с новыми печеньками(cookie), при следующем запросе будут использоваться именно они
        os.remove('Samiy_umniy.txt')
        with open('Samiy_umniy.txt', 'a+') as file:
            file.write(response_bonday_cookies['Samiy_umniy?'])
            print(colorama.Fore.BLUE + '[INFO] ' + colorama.Fore.GREEN + 'Записал: Samiy_umniy?')

    else:
        # Если он не существует - то мы его создаем новый с новыми печеньками(cookie), при следующем запросе будут использоваться именно они
        with open('Samiy_umniy.txt', 'a+') as file:
            file.write(response_bonday_cookies['Samiy_umniy?'])
            print(colorama.Fore.BLUE + '[INFO] ' + colorama.Fore.GREEN + 'Записал: Samiy_umniy?')

    print(colorama.Fore.BLUE + '[INFO] ' + colorama.Fore.GREEN + 'Получил ответ от BonDay, начинаю искать данные')

    # Проверка на существование данных в БД bonday
    if 'Ничего не найдено.' in response.text:
        print(colorama.Fore.RED + '[ERROR] ' + colorama.Fore.GREEN + f'По нику {nick} данных не найдено!')

    # Проверка на блокировку запроса бондеем
    elif 'татары недовольны твоими действиями.' in response.text:
        print(colorama.Fore.RED + '[ERROR] ' + colorama.Fore.GREEN + 'Татары недовольны твоими действиями.(Слишком много запросов к BonDay)')

    # Если все хорошо то начинаем собирать данные
    else:
        # Объявляем переменную tabledata для составления таблицы
        tabledata = []
        # Создаем объект BeautifulSoup4
        soup = BSoup(response.text, 'lxml')
        # Ищем таблицу с никами, паролями и базами
        ready = soup.find_all('tr', class_='table-primary')
        print(colorama.Fore.BLUE + '[INFO] ' + colorama.Fore.GREEN + 'Начинаю составлять таблицу с никами, паролями и базами')
        # Пробегаемся циклом по всем никам, паролям и базам
        for i in ready and tqdm(ready):
            i = list(i)
            try:
                # Достаем из записи таблицы ник
                nick = str(i[1]).replace('<td>', '').replace('</td>', '')
                # Достаем из записи таблицы пароль
                password = str(i[2]).replace('<td>', '').replace('</td>', '')
                # Достаем из записи таблицы базу
                base = str(i[3]).replace('<td>', '').replace('</td>', '').strip()
                # Добавляем данные в переменную для составления таблицы
                tabledata.append([nick, password, base])

            except:
                pass

        # Если файл result.txt существует то мы записываем в него таблицу
        if os.path.exists('result.txt'):
            with open('result.txt', 'w') as file:
                file.write(tabulate(tabledata))

        # Если файла нету то мы его создаем и записываем таблицу
        else:
            with open('result.txt', 'a+') as file:
                file.write(tabulate(tabledata))

        print(colorama.Fore.BLUE + '[INFO] ' + colorama.Fore.GREEN + 'Результат парсинга сохранен в файл result.txt')


# Запрашиваем у пользователя ник
NICK = input(colorama.Fore.CYAN + '[QUESTION] ' + colorama.Fore.YELLOW + 'Введи ник по которому искать данные: ')

# Вызываем функцию get_data
get_data(NICK)
