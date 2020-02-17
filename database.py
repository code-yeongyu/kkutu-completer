import sqlite3
from db_specs import db_settings
from db_specs import table_schema


def save_word(word):
    connection = sqlite3.connect(db_settings.file_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM hangul WHERE word='{word}';")
    if len(cursor.fetchall()) == 0:
        cursor.execute(
            f"INSERT INTO hangul(word, start, length) VALUES('{word}', '{word[:1]}', {len(word)});"
        )
        connection.commit()
    cursor.close()


def delete_word(word):
    connection = sqlite3.connect(db_settings.file_name)
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM hangul WHERE word='{word}';")
    connection.commit()
    cursor.close()


def get_recommendation(start):
    start = start[-1:]
    connection = sqlite3.connect(db_settings.file_name)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM hangul WHERE start='{start}' ORDER BY length DESC;")
    result = cursor.fetchall()
    cursor.close()
    return result
