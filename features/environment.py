"""Configure headless Selenium for the product-catalog UI scenarios."""
from os import getenv

from selenium import webdriver


def before_all(context):
    context.base_url = getenv("BASE_URL", "http://127.0.0.1:5000")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(int(getenv("WAIT_SECONDS", "10")))


def after_all(context):
    context.driver.quit()
