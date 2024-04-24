import datetime as dt
import arxiv
from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

# テンプレートを用意
QUERY_TEMPLATE = '%28 ti:%22{}%22 OR abs:%22{}%22 %29 AND submittedDate: [{} TO {}]'
# 検索期間 N_DAYS 日前までの論文を検索
N_DAYS = 7
# 検索のkeyword
keyword = "software development"
# 検索結果の上限
MAX_RESULT = 3

# arXivの更新頻度を加味して，1週間前の論文を検索
today = dt.datetime.today() - dt.timedelta(days=7)
base_date = today - dt.timedelta(days=N_DAYS)
query = QUERY_TEMPLATE.format(keyword, keyword, base_date.strftime("%Y%m%d%H%M%S"), today.strftime("%Y%m%d%H%M%S"))

search = arxiv.Search(
    query=query,  # 検索クエリ
    max_results=MAX_RESULT,  # 取得する論文数の上限
    sort_by=arxiv.SortCriterion.SubmittedDate,  # 論文を投稿された日付でソートする
    sort_order=arxiv.SortOrder.Descending,  # 新しい論文から順に取得する
)

# 興味があるカテゴリー群
CATEGORIES = {
    "cs.AI",    # Artificial Intelligence
    "cs.GT",    # Computer Science and Game Theory
    "cs.PL",    # Programming Languages
    "cs.SE"    # Software Engineering
}

# searchの結果をリストに格納
result_list = []
for result in search.results():
    # カテゴリーに含まれない論文は除く
    if len((set(result.categories) & CATEGORIES)) == 0:
      continue
    result_list.append(result)

# LINE Botのチャンネルアクセストークン
LINE_CHANNEL_ACCESS_TOKEN = "T8isp2SiJ3Cpdlw+A67FYbLVebZyL5E0o/DdPOVXPvNJJpSdSjikxMfMUe+1nYyBgX7X2eTH2Cm+94J+IvxUsBirfxthD4bslLIb0sMllKEQX2pSVKLHCm38f3kVLs/e7MHmAwpBdcZpmPIC0rw4TQdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# LINEに送信するメッセージを作成
message = f"最新の論文をお知らせします。（{len(result_list)}件）\n\n"

for result in result_list:
    links = [f"{link}" for link in result.links if "abs" in f"{link}"]
    message += f"{links[0]}\n"
    message += f"{result.title}\n"

# print(message)

# LINEにメッセージを送信
line_bot_api.broadcast(TextSendMessage(text=message))