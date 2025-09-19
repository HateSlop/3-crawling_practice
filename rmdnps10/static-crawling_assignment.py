from bs4 import BeautifulSoup
import requests
import csv

url = 'https://www.aladin.co.kr/shop/wbrowse.aspx?CID=34582'
reponse = requests.get(url)
html = reponse.text
soup = BeautifulSoup(html, 'html.parser')

books_container = soup.select_one('.b-bestseller .BrowseBestSeller') 
books = books_container.select('li')
book_data = []

for book in books:
    title = book.select_one('h4>a').get_text(strip=True)
    author = book.select_one('.b-author').get_text(strip=True)
    price = book.select_one('.b-price>strong').get_text(strip=True)
    book_data.append([title, author, price])

with open('books.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Author', 'Price'])
    writer.writerows(book_data)




