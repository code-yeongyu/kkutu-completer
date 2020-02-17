import database
from hangul_library import *
from selenium import webdriver
from time import sleep


def filter_word_to_type(words, history):
    ONE_KILL = [
        '륨', '늄', '릇', '쁨', '붏', '썽', '늬', '싕', '꾼', '슭', '즘', '썹', '쭝', '뀌',
        '휼', '념', '삯', '뇰', '믜', '뮴', '븀', '켓', '녘', '겅', '슴', '듬', '켈', '션',
        '믈', '슘', '섯', '뇨', '못', '렁', '갱', '듐', '튬', '드', '봇', '쉽', '윰', '릎',
        '듭', '쫑', '뺌', '엌', '즙', '짐', '킷', '갗', '탉', '득', '욱', '즐', '첸', '콕',
        '혀', '폭', '뢰', '죵', '샅', '램', '랖', '랒', '길', '밀', '꼍', '믄', '뭇', '슨',
        '늉', '율', '킨', '펫', '껑', '셋', '궤', '믁', '윙', '븨', '욤', '늘', '삐', '닥',
        '앗'
    ]
    suggested = []
    if len(words) == 0:
        return None
    for word in words:
        if not word[1] in history:
            suggested.append(word[1])
    suggested.sort(key=len, reverse=True)
    if len(history) != 0:
        for s in suggested:
            if s[-1:] in ONE_KILL:
                return s
    return suggested[0]


def manner_filter_word_to_type(words, history):
    ONE_KILL = [
        '륨', '늄', '릇', '쁨', '붏', '썽', '늬', '싕', '꾼', '슭', '즘', '썹', '쭝', '뀌',
        '휼', '념', '삯', '뇰', '믜', '뮴', '븀', '켓', '녘', '겅', '슴', '듬', '켈', '션',
        '믈', '슘', '섯', '뇨', '못', '렁', '갱', '듐', '튬', '드', '봇', '쉽', '윰', '릎',
        '듭', '쫑', '뺌', '엌', '즙', '짐', '킷', '갗', '탉', '득', '욱', '즐', '첸', '콕',
        '혀', '폭', '뢰', '죵', '샅', '램', '랖', '랒', '길', '밀', '꼍', '믄', '뭇', '슨',
        '늉', '율', '킨', '펫', '껑', '셋', '궤', '믁', '윙', '븨', '욤', '늘', '삐', '닥',
        '앗'
    ]
    suggested = []
    if len(words) == 0:
        return None
    for word in words:
        if not word[1] in history:
            if word[1][-1:] not in ONE_KILL:
                suggested.append(word[1])
    suggested.sort(key=len, reverse=True)

    return suggested[0]


class KkutuGame:
    def __init__(self, driver):
        self.driver = driver
        self.used_words = []
        self.current_text = ""

    def add_used_word(self, word):
        self.used_words.append(word)

    def get_used_words(self):
        return self.used_words

    def get_current_text(self):
        return driver.find_element_by_css_selector(
            "#GameBox > div > div.game-head > div.jjoriping > div > div.jjo-display.ellipse"
        ).text

    def type_word(self, word):
        try:
            self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[31]/div/input").send_keys(f"{word}\n")
        except:
            self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[30]/div/input").send_keys(f"{word}\n")

    def wait_for_turn(self):
        try:
            self.driver.find_element_by_css_selector("#game-input").click()
            return True
        except:
            pass
        return False

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
                    except:
                        pass
                self.add_used_word(word)
                self.used_words = list(set(self.used_words))
                print(self.used_words)
        except:
            pass

    def mine_words_til_my_turn(self):
        while True:
            self.update_used_words()
            if self.current_text != self.get_current_text():
                self.current_text = self.get_current_text()
            if self.wait_for_turn():
                return


driver = webdriver.Chrome(
    "/Users/yeongyu/Documents/git/kkutu-completer/chromedriver")
driver.get("https://kkutu.co.kr")
kg = KkutuGame(driver)
import pdb
pdb.set_trace()
while True:
    kg.mine_words_til_my_turn()
    text = kg.current_text
    text = extract_blanks_and_texts(text)
    suggested = []
    for t in text:
        while True:
            try:
                suggested += database.get_recommendation(text)
                break
            except:
                pass
    try:
        result = manner_filter_word_to_type(suggested, kg.get_used_words())
        f = open("logs.txt", 'a')
        f.write(f"{result}\n")
        f.close()
    except:
        pass
    if result != None:
        kg.type_word(result)
        kg.add_used_word(result)
    else:
        kg.type_word(f"{text[-1:]}| 한방단어 우웩 ㅠㅠ")
    print(kg.get_used_words())
    sleep(3)