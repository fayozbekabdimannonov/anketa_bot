#1)ism,familya,tug"ilgan yili,rasm, [id]
import sqlite3
connection = sqlite3.connect("anketa.db")
def create_anketa():
    command = """
    CREATE TABLE IF NOT EXISTS anketa (
    ism VARCHAR(50),
    familya VARCHAR(50),
    tel_raqam NUMBER,
    jinsi VARCHAR,
    t_yil NUMBER,
    t_oy NUMBER,
    t_kun NUMBER,
    rasmi VARCHAR(50),
    telegram_id NUMBER UNIQUE
    );
    """

    cursor = connection.cursor()

    cursor.execute(command)

    connection.commit()
def anketa_qushish(ism,familya,tel_raqam,jinsi,t_yil,t_oy,t_kun,rasm,telegram_id):
    command = f"""
INSERT INTO anketa VALUES("{ism}","{familya}","{tel_raqam}","{jinsi}","{t_yil}","{t_oy}","{t_kun}","{rasm}","{telegram_id}");

"""
    cursor = connection.cursor()

    cursor.execute(command)

    connection.commit()

def users_id():
    command = f"""
SELECT telegram_id FROM anketa;
"""
    cursor = connection.cursor()

    cursor.execute(command)

    return cursor.fetchall()