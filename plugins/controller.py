import sqlite3
import urllib.request
from bs4 import BeautifulSoup

DATA_BASE_PATH = "./db/database.db"


def get_split_number(number):
    for n in range(number.count(",")):
        number = number.replace(",", "")
    return number


def get_code_from_name(name):
    connector = sqlite3.connect(DATA_BASE_PATH)
    cursor = connector.cursor()
    try:
        name = int(name)
        rows = cursor.execute("SELECT * FROM companies WHERE code LIKE '%{}%'".format(name))
    except:
        rows = cursor.execute("SELECT * FROM companies WHERE name LIKE '%{}%'".format(name))
    return [dict(company=row[0], code=row[1]) for row in rows]


def get_info_from_code(code):
    html = urllib.request.urlopen("http://stocks.finance.yahoo.co.jp/stocks/detail/?code={}".format(str(code)))
    soup = BeautifulSoup(html, "html.parser")
    name = soup.h1.string.replace("(株)", "")
    real = soup.find(class_="real").text
    real = "{} {}".format(real[: 5], real[5: ])
    now = get_split_number(soup.find_all(class_="stoksPrice")[-1].string)
    last_close = float(get_split_number(soup.find(class_="ymuiEditLink" and "mar0").strong.string))

    if now == "---":
        difference = ""
        percent = ""
    else:
        now = float(now)
        difference = round(now - last_close, 1)
        percent = "{}%".format(round((difference / last_close) * 100, 2))

    return dict(
        name=name,
        real=real,
        now=str(now),
        last_close=str(last_close),
        difference=difference,
        percent=percent,
    )


def get_stock_from_user(user):
    connector = sqlite3.connect("./db/database.db")
    cursor = connector.cursor()

    sentence = ""
    rows = cursor.execute(
        "SELECT co.name, st.count, co.code, st.price FROM stocks AS st, companies AS co WHERE st.code = co.code AND st.user='{}'"
        .format(user)
    )
    for row in rows:
        sentence += "\n\t【{}: {}】\n\t株式数： {}\n\t取得価格： {}".format(row[0], row[2], row[1], row[3])

        info = get_info_from_code(row[2])
        if len(info) == 6 and info["difference"] != "":
            difference_y = info["difference"]
            difference = int(float(info["now"])) -  int(row[3])

            sentence += "\n\t現在価格： {}".format(int(float(info["now"])))
            sentence += "\n\n\t評価損益： {}".format(difference * int(row[1]))
            sentence += "\n\t(前日比較： {}, {})\n".format(int(int(row[1]) * difference_y), info["percent"])
            sentence += "\n\t({})".format(info["real"])
        sentence += "\n\t{}".format("-----" * 5)

    return sentence


def stock_from_user_code_count(user, code, count, price):
    connector = sqlite3.connect(DATA_BASE_PATH)
    cursor = connector.cursor()

    sql = "SELECT * FROM stocks WHERE user='{}' and code='{}' and count='{}'".format(user, code, count)
    rows = cursor.execute(sql)
    if [row for row in rows] != []:
        sentence = "この銘柄は既に登録されています。\n"
    else:
        sql = "SELECT * FROM stocks WHERE user='{}' and code='{}'".format(user, code)
        rows = cursor.execute(sql)
        if [row for row in rows] != []:
            sql = "UPDATE stocks SET count='{}' WHERE user='{}' and code='{}'".format(count, user, code)
            connector.execute(sql)
            connector.commit()
            sentence = "株式数の 【更新】 が完了しました。\n"

        else:
            sql = "INSERT INTO stocks VALUES('{}', '{}', '{}', '{}')".format(user, code, count, price)
            connector.execute(sql)
            connector.commit()
            sentence = "銘柄の 【登録】 が完了しました。\n"

    sentence += "現在あなたが登録している銘柄はこちらです。\n"
    sentence += get_stock_from_user(user)

    connector.close()
    return sentence


def delete_from_user_code(user, code):
    connector = sqlite3.connect(DATA_BASE_PATH)
    cursor = connector.cursor()

    sql = "DELETE FROM stocks WHERE user='{}' and code='{}'".format(user, code)
    cursor.execute(sql)
    connector.commit()
    connector.close()

    sentence = "銘柄の 【消去】 が完了しました。\n"
    sentence += "現在あなたが登録している銘柄はこちらです。\n"
    sentence += get_stock_from_user(user)

    return sentence
