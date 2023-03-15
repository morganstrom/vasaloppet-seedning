from selenium import webdriver
from selenium.webdriver.common.by import By


class Client(object):
    def __init__(self):
        self.driver = webdriver.Firefox()

    def goto_page(self, url: str):
        self.driver.get(url)

    def click_link(self, link_text: str):
        link = self.driver.find_element(By.LINK_TEXT, link_text)
        link.click()

    def get_page_source(self) -> str:
        return self.driver.page_source

    def close(self):
        self.driver.close()
