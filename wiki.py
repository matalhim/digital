import requests
import mwparserfromhell

# URL страницы с предлогами на Wiktionary
url = 'https://ru.wiktionary.org/wiki/Категория:Русские_предлоги'

# Отправка GET-запроса на страницу
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    # Извлечение текста из HTML-кода
    text = response.text

    # Используйте mwparserfromhell для парсинга вики-текста
    wikicode = mwparserfromhell.parse(text)

    # Извлечение заголовков страниц (предлогов)
    prepositions = []
    for section in wikicode.get_sections(matches="^= Русские предлоги ="):
        for link in section.filter_links():
            preposition = link.title.strip_code()
            prepositions.append(preposition)

    # В переменной prepositions будут предлоги
    print(prepositions)
else:
    print(f"Ошибка при запросе данных: {response.status_code}")
