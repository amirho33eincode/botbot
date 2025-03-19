import requests
from bs4 import BeautifulSoup

base_url = "https://arzdigital.com/coins/"
name = []
price = []

response = requests.get(base_url)
soup = BeautifulSoup(response.text,'html.parser')
 
table = soup.find("table",{"class":"arz-table"})

for row in table.find('tbody').find_all('tr'):
  name.append(row.find('a',{"class":'arz-tw-grow'}).find('span').text)
  price.append(row.find('td',{"class":"arz-coin-table__price-td"}).find('span').text)
  