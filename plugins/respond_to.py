from slackbot.bot import respond_to
import re

from .controller import (
    get_code_from_name,
    get_info_from_code,
    get_stock_from_user,
    stock_from_user_code_count,
    delete_from_user_code,
)


@respond_to('search (.*)', re.IGNORECASE)
@respond_to('search　(.*)', re.IGNORECASE)
def search_from_name(message, name):
    sentence = ""
    companies = get_code_from_name(name)
    if companies != []:
        for company in companies:
            sentence += "企業名： {}, 銘柄コード： {}\n".format(company["company"], company["code"])
    else:
        sentence += "該当する銘柄は見つかりませんでした。"

    message.reply("```{}```".format(sentence))


@respond_to('get (.*)', re.IGNORECASE)
@respond_to('get　(.*)', re.IGNORECASE)
def check_from_code(message, code):
    try:
        info = get_info_from_code(code)
        if len(info) == 6 and info["difference"] != "":
            if float(info["difference"]) > 0:
                info["difference"] = "+{}".format(info["difference"])
                info["percent"] = "+{}".format(info["percent"])
            sentence = "【{}】\n現在価格： {}\n前日終値： {}\n\v\v\v前日比： {} ({})\n{}\n({})".format(
                    info["name"],
                    info["now"],
                    info["last_close"],
                    info["difference"],
                    info["percent"],
                    "-----" * 5,
                    info["real"],
                )
        elif len(info) == 6 and info["difference"] == "":
            sentence = "市場が開く前です。9時までお待ちください。"
    except:
        sentence = "銘柄コードに一致する株価情報が見つかりませんでした。"

    message.reply("```{}```".format(sentence))


@respond_to('check', re.IGNORECASE)
def check_from_user(message):
    user = message.body["user"]
    sentence = get_stock_from_user(user)

    if sentence == "":
        sentence = "あなたが登録している銘柄は存在しません。"

    message.reply("```{}```".format(sentence))


@respond_to('register (.*) (.*) (.*)', re.IGNORECASE)
def register_stock(message, code, count, price):
    user = message.body["user"]
    stock = stock_from_user_code_count(user, code, count, price)
    message.reply("```{}```".format(stock))


@respond_to('delete (.*)', re.IGNORECASE)
def delete_stock(message, code):
    user = message.body["user"]
    stock = delete_from_user_code(user, code)
    message.reply("```{}```".format(stock))


@respond_to('help', re.IGNORECASE)
def help(message):
    sentence = "*・銘柄コードを聞く*\n```search [銘柄名(部分一致可)]```\n"\
        + "*・銘柄の現在価格等を聞く*\n```get [銘柄コード]```\n"\
        + "*・銘柄の登録、登録銘柄の更新*\n```register [銘柄コード] [株式数] [取得価格]```\n"\
        + "*・登録銘柄の消去*\n```delete [銘柄コード] ```\n"\
        + "*・登録銘柄の現在価格等を聞く*\n```check```"
    message.reply(sentence)
