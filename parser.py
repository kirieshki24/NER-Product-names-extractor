from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import main

def body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.body
    if body:
        return str(body)
    else: 
        return ''
    
def cleaned_content(body):
    soup = BeautifulSoup(body, 'html.parser')

    for script_style in soup(["script", "style"]):
        script_style.extract()
    
    cleaned_content = soup.get_text(separator = '\n')
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [ 
        dom_content[i : i+max_length] for i in range(0, len(dom_content), max_length)
    ]


def csv_opener(csv_file):
    data_list = []

    # Открываем файл и читаем его содержимое
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        # Создаем объект reader для чтения CSV
        csv_reader = csv.reader(file)
        
        # Пропускаем заголовок (если он есть)
        header = next(csv_reader)
        
        # Читаем данные построчно и добавляем их в список
        for row in csv_reader:
            data_list.append(row[0])
    return data_list

def URL_parser(url: str) -> str:

    # Set up the Chrome driver
    driver = main.get_driver()

    try:
        driver.get(url)
        time.sleep(2)  # Wait for the initial content to load

            # Scroll down the page with a limit to prevent infinite scrolling
        max_scroll_attempts = 5  # Limit scrolling attempts to avoid endless scrolling
        scroll_attempt = 0

        while scroll_attempt < max_scroll_attempts:
            driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down by 500 pixels
            time.sleep(0.3)  # Wait for new content to load

                # Check if we're at the bottom of the page
            new_height = driver.execute_script("return window.pageYOffset + window.innerHeight;")
            total_height = driver.execute_script("return document.body.scrollHeight")

                # Break if we have reached the end of the page
            if new_height >= total_height:
                print("Reached the end of the page.")
                break

            scroll_attempt += 1

        html = driver.page_source
            
    except Exception as e:
        html = 'NO RESPONSE\n'
        print(f"Error fetching {url}: {e}")
    
    driver.quit()
    return html
