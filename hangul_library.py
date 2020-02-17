def extract_blanks_and_texts(text):
    result = ""
    for letter in text:
        if (ord('가') <= ord(letter) <= ord('힣')) or letter == ' ':
            result += letter
    return result.replace(" ", "")


def get_chosung(word):
    word = extract_blanks_and_texts(word)
    CHOSUNG = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
        'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]
    HANGUL_START = 44032
    CHOSUNG_WEIGHT = 588
    result = ""
    for letter in word:
        if letter == ' ':
            result += ' '
            continue
        CODE = ord(letter) - HANGUL_START
        CHAR_INDEX = int(CODE / CHOSUNG_WEIGHT)
        result += CHOSUNG[CHAR_INDEX]
    return result