from os import getenv

DATA_CENTER_TOKEN = getenv("DATA_CENTER_TOKEN", "ko_no_data_center_da")
LINE_BOT_CLIENT_TOKEN = getenv("LINE_BOT_CLIENT_TOKEN", "ko_no_linebot_da")
LINE_BOT_API_BASE = getenv("LINE_BOT_URL", "https://feizao-bot.herokuapp.com/")
