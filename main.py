import requests
import csv
from bs4 import BeautifulSoup
from time import sleep
from random import randint

pages = {'page': 1}
file = open('buyers.csv', 'w', encoding='utf-8', newline='\n')
file_obj = csv.writer(file)
file_obj.writerow(['brand', 'title', 'price'])
url = 'https://buyers.ge/category/lifestyle/914'

while pages['page'] < 6:
    content = requests.get(url, params=pages).text
    soup = BeautifulSoup(content, 'html.parser')
    block = soup.find('div', class_='products_list')
    items = block.find_all('div', class_='product_list_item')

    for each in items:
        brand = each.find('a', class_='brand').text
        title = each.find('a', class_='title').text

        # საიტზე ზოგიერთ ნივთზე იყო ფასდაკლება და ფასები რომ მომქონდა,
        # პროგრამას ორივე, ანუ ძველი და ახალი ფასი გადმოჰქონდა, ამიტომ
        # დავაფორმატე ისე რომ მხოლოდ ამჟამინდელი ფასი გამოჩენილიყო string-ის მეთოდებით
        price = each.find_all('div', class_='price')[0].text.replace(' ', '').replace('\n', '')

        file_obj.writerow([brand, title, price[:price.find('₾')+1]])
    pages['page'] += 1
    sleep(randint(15, 20))
file.close()
