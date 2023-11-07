import requests
import random
import collections
import re

def get_page_vacancies(vacancy, city_id, per_page=100, page=0):
    base_url = "https://api.hh.ru/vacancies"
    params = {
        "text": vacancy,
        "area": city_id,
        "per_page": per_page,
        "page": page
    }

    response = requests.get(base_url, params=params)

    if response.status_code:
        data = response.json()
        vacancies = data.get('items', [])
        return vacancies

def get_all_vacavacancies():
    vacancy = "программист"
    area = {
        'msc': 1,
        'spb': 2
    }
    per_page = 100
    all_vacancies = []

    for city_id in area.values():
        for page in range(10):
            page_vacancies = get_page_vacancies(vacancy, city_id, per_page, page)
            all_vacancies.extend(page_vacancies)

    return all_vacancies

get_vacancies = get_all_vacavacancies()

random_index = random.randint(0, 2000)
for key, value in get_vacancies[random_index].items():
    print('{}: {}'.format(key, value))

keys = [
    'id', 'name', 'salary', 'employer', 'snippet']

vacancies = list()

new_vacancies = list(map(
    lambda vacance: {
        'id': vacance['id'],
        'name': vacance['name'],
        'area': vacance['area']['name'],
        'salary_from': vacance['salary']['from'] if vacance['salary'] and vacance['salary']['from'] else None,
        'salary_to': vacance['salary']['to'] if vacance['salary'] and vacance['salary']['to'] else None,
        'currency': vacance['salary']['currency'] if vacance['salary'] and vacance['salary']['currency'] else None,
        'gross': vacance['salary']['gross'] if vacance['salary'] and  vacance['salary']['gross'] else None,
        'employer': vacance['employer']['name'],
        'requirement': vacance['snippet']['requirement'] if vacance['snippet'] and vacance['snippet']['requirement'] else None
    },
    get_vacancies
))
vacancies.extend(new_vacancies)

for key, value in vacancies[random_index].items():
    print('{}: {}'.format(key, value))

words = list()

for vacancy in vacancies:
  requirement = vacancy.get('requirement')
  if requirement:
    requirement = re.sub(r'[^\w\s]', '', requirement)
    words.extend(requirement.lower().split())


words_counter = collections.Counter(words)
delete_list = {
    'в', 'на', 'под', 'за', 'с',
    'у', 'к', 'от', 'до', 'по',
    'и', 'или', 'да', 'либо', 'то'
}
words_counter = collections.Counter({word: count for word, count in words_counter.items() if word not in delete_list})

sort_words = sorted(words_counter.items(), key=lambda x: x[1], reverse=True)
for word_counter in sort_words[:5]:
  print('{}: {}'.format(word_counter[0], word_counter[1]))

five_words_set = {word[0] for word in sort_words[:5]}
sort_vacancies = list()
words = list()

for vacancy in vacancies:
  requirement = vacancy.get('requirement')
  if requirement:
    words = set(requirement.lower().split())
    if five_words_set.intersection(set(words)):
      sort_vacancies.append(vacancy)

print(sort_vacancies[0])

for vacancy in sort_vacancies:
  print('\n')
  for key, value in vacancy.items():
   print('{}: {}'.format(key, value))