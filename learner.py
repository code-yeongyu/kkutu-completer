import database
from hangul_library import *
from selenium import webdriver
from time import sleep


def filter_word_to_type(words, history):
    for word in words:
        if not word[1] in history:
            return word[1]


class KkutuGame:
    def __init__(self, driver):
        self.driver = driver
        self.used_words = []

    def add_used_word(self, word):
        self.used_words.append(word)
        database.save_word(word)

    def get_used_words(self):
        return self.used_words

    def get_current_text(self):
        return driver.find_element_by_css_selector(
            "#GameBox > div > div.game-head > div.jjoriping > div > div.jjo-display.ellipse"
        ).text

    def type_word(self, word):
        self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[31]/div/input").send_keys(f"{word}\n")

    def wait_for_turn(self):
        try:
            self.driver.find_element_by_css_selector("#game-input").click()
            return True
        except:
            pass
        return False

    def update_used_words(self):
        try:
            word = driver.find_element_by_css_selector(
                "#GameBox > div > div.game-head > div.history-holder > div > div:nth-child(1)"
            ).get_attribute("innerHTML")
            word = word[:word.find("<")]
            if word not in self.used_words:
                self.add_used_word(word)
                self.used_words = list(set(self.used_words))
                print(self.used_words)
                sleep(3)
        except:
            pass

    def mine_words_til_my_turn(self):
        while True:
            self.update_used_words()
            if self.wait_for_turn():
                return


driver = webdriver.Chrome(
    "/Users/yeongyu/Documents/git/kkutu-completer/chromedriver")
driver.get("https://kkutu.co.kr")
kg = KkutuGame(driver)
while True:
    import pdb
    pdb.set_trace()
