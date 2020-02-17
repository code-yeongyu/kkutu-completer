# CREATING TABLE

#import psycopg2
import sqlite3
from db_specs import db_settings
from db_specs import table_schema

schema_text = ""
schemas_info = table_schema.schema
for COLUMN_NAME in schemas_info.keys():
    schema_info = schemas_info[COLUMN_NAME]
    TYPE = schema_info['TYPE']
    OPTIONS = schema_info['OPTIONS']
    schema_text += f"{COLUMN_NAME} {TYPE} {OPTIONS}, "
schema_text = schema_text[:schema_text.rfind(",")]

connection = sqlite3.connect(db_settings.file_name)
cursor = connection.cursor()
cursor.execute(f"CREATE TABLE hangul ({schema_text});")
cursor.close()
connection.commit()