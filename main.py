import database
from hangul_library import *
from selenium import webdriver
from threading import Thread
from time import sleep
import random
import sqlite3
from db_specs import db_settings
from db_specs import table_schema


def manner_filter_word_to_type(words, history):
    # 맨 뒷자리 '하다' 있으면 제거
    ONE_KILL = [
        '륨', '늄', '릇', '쁨', '붏', '썽', '늬', '싕', '꾼', '슭', '즘', '썹', '쭝', '뀌',
        '휼', '념', '삯', '뇰', '뮴', '븀', '켓', '녘', '겅', '슴', '듬', '켈', '션', '믈',
        '슘', '섯', '뇨', '못', '렁', '갱', '듐', '튬', '드', '봇', '쉽', '윰', '릎', '듭',
        '쫑', '뺌', '엌', '즙', '짐', '킷', '갗', '탉', '득', '욱', '즐', '첸', '콕', '혀',
        '뢰', '죵', '샅', '램', '랖', '랒', '길', '밀', '꼍', '믄', '뭇', '슨', '늉', '율',
        '킨', '펫', '껑', '궤', '믁', '윙', '욤', '늘', '삐', '닥'
    ]
    TWO_KILL = [
        '늣', '븨', '뀌', '훠', '샷', "얏", "츰", "랏", "쳔", "즘", "륄", "옳", "믜", '셋',
        "쳥", "욘", '숍', '랙', '츈', '렛', '텬', '딍', '싀'
    ]
    suggested = []
    if len(words) == 0:
        return None

    for word in words:
        if not word[1] in history:
            if word[1][-1:] not in ONE_KILL:
                suggested.append(word[1])
    suggested.sort(key=len, reverse=True)

    # two_kill
    if len(suggested[0]) < 15:
        for s in suggested:
            if s[-1:] in TWO_KILL:
                print("ATTACK!")
                return s

    return suggested[0]


def load_words():
    words_raw = database.get_all()
    words = []
    for word in words_raw:
        words.append([word[1], word[2]])
    del words_raw

    words.sort(key=lambda x: (x[0][0], -len(x[0])))
    return words


def search_word(words, letter):
    for word in words:
        if word[1] == letter:
            return word


class KkutuGame:
    def __init__(self, driver):
        self.driver = driver
        self.used_words = []
        self.current_text = ""
        connection = sqlite3.connect(db_settings.file_name)
        self.cursor = connection.cursor()

    def get_remain_time(self):
        text = driver.find_element_by_css_selector(
            "#GameBox > div > div.game-head > div.jjoriping > div > div.graph.jjo-turn-time > div"
        ).text
        return float(text.replace("초", ""))

    def is_fail(self):
        if "game-fail-text" in driver.page_source:
            try:
                text = self.driver.find_element_by_xpath(
                    '//*[@id="GameBox"]/div/div[1]/div[6]/div/div[1]/label'
                ).text
                if "한방 단어" in text or not "이미 쓰인 단어" in text:
                    return True
            except Exception as e:
                pass

    def add_used_word(self, word):
        self.used_words.append(word)

    def get_used_words(self):
        return self.used_words

    def get_current_text(self):
        return driver.find_element_by_css_selector(
            "#GameBox > div > div.game-head > div.jjoriping > div > div.jjo-display.ellipse"
        ).text

    def update_current_text(self):
        try:
            if not self.is_fail():
                self.current_text = self.get_current_text()
        except Exception as e:
            pass

    def type_word(self, word):
        try:
            self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[31]/div/input").send_keys(f"{word}\n")
        except:
            self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[30]/div/input").send_keys(f"{word}\n")

    def send_word(self, word):
        js = f"document.getElementById('{self.get_chat_element()}').value = '{word}';"
        js += "document.getElementById('ChatBtn').click();"
        self.driver.execute_script(js)

    def get_chat_element(self):
        source = driver.page_source
        source = source[source.find("UserMessage"):]
        source = source[:source.find("\"")]
        return source

    def is_my_turn(self):
        return self.driver.find_element_by_css_selector(
            "#game-input").is_displayed()
        return True

    def update_used_words(self):
        if len(driver.find_elements_by_css_selector(".history-item")) == 0:
            self.used_words = []
        try:
            word = driver.find_element_by_css_selector(
                "#GameBox > div > div.game-head > div.history-holder > div > div:nth-child(1)"
            ).get_attribute("innerHTML")
            word = word[:word.find("<")]
            if word not in self.used_words:
                while True:
                    try:
                        database.save_word(word)
                        break
                    except Exception as e:
                        print(e)
                self.add_used_word(word)
                self.used_words = list(set(self.used_words))
        except Exception as e:
            pass

    def mine_words_til_my_turn(self):
        while True:
            self.update_used_words()
            kg.update_current_text()
            if self.is_my_turn():
                return


def thread_wrapper(kg):
    text = extract_blanks_and_texts(kg.current_text)
    used = []
    while kg.is_my_turn():
        suggested = []

        for t in text:
            while True:
                try:
                    suggested += database.get_recommendation_quick(
                        text, kg.cursor)
                    break
                except:
                    pass

        result = manner_filter_word_to_type(suggested,
                                            kg.get_used_words() + used)
        if result != None:
            remaining_time = kg.get_remain_time()
            sleep_time = random.uniform(0, remaining_time - 1)
            sleep(sleep_time)
            kg.send_word(result)
            sleep(0.5)
            if kg.is_fail():
                f = open("fails.txt", 'a')
                f.write(f"{used}\n")
                f.close()
            used.append(result)
            print(f"{text[-1:]}| {result}")
            kg.add_used_word(result)
        else:
            f = open("logs.txt", 'a')
            f.write(f"{text[-1:]}\n")
            f.close()


driver = webdriver.Chrome(
    "/Users/yeongyu/Documents/git/kkutu-completer/chromedriver")
driver.get("https://kkutu.co.kr")
kg = KkutuGame(driver)
input("엔터")
while True:
    try:
        kg.mine_words_til_my_turn()
        thread_wrapper(kg)
    except Exception as e:
        print(e)