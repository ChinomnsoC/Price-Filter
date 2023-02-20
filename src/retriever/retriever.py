from bs4 import BeautifulSoup
import requests


response = requests.get('https://www.currys.co.uk/products/lg-oled55cs6la-55-smart-4k-ultra-hd-hdr-oled-tv-with-google-assistant-and-amazon-alexa-10242981.html')
response.status_code

url = 'https://www.currys.co.uk/products/lg-oled55cs6la-55-smart-4k-ultra-hd-hdr-oled-tv-with-google-assistant-and-amazon-alexa-10242981.html'
prod_page = BeautifulSoup(url)    
print(prod_page.prettify())
