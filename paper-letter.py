import datetime as dt
import arxiv

# テンプレートを用意
QUERY_TEMPLATE = '%28 ti:%22{}%22 OR abs:%22{}%22 %29 AND submittedDate: [{} TO {}]'
# 検索期間 N_DAYS 日前までの論文を検索
N_DAYS = 7
# 検索のkeyword
keyword = "software development"
# 検索結果の上限
MAX_RESULT = 1

# arXivの更新頻度を加味して，1週間前の論文を検索
today = dt.datetime.today() - dt.timedelta(days=7)
base_date = today - dt.timedelta(days=N_DAYS)
query = QUERY_TEMPLATE.format(keyword, keyword, base_date.strftime("%Y%m%d%H%M%S"), today.strftime("%Y%m%d%H%M%S"))

search = arxiv.Search(
    query=query,  # 検索クエリ
    max_results=MAX_RESULT * 3,  # 取得する論文数の上限
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

print(result_list)