from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os

load_dotenv()

FLAG = os.getenv('FLAG')

def visit(id):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get('http://127.0.0.1:5000/signin')
        driver.add_cookie({"name" : "flag", "value": FLAG})
        print("Added cookie")
    except:
        print("Failed to add cookie")

    link = "http://127.0.0.1:5000/product/"+id
    try:
        driver.get(link)
        print("Visiting: " + link)
        driver.close()
        return True
    except:
        driver.close()
        print("Failed to visit: " + link)
        return False