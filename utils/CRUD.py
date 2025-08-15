import csv
import os

COMMENTS_FILE = os.path.join("data", "comments.csv")

def initialize_comments_file():
    """コメントファイルが存在しない場合に初期化する"""
    if not os.path.exists(COMMENTS_FILE):
        os.makedirs(os.path.dirname(COMMENTS_FILE), exist_ok=True)
        with open(COMMENTS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "olid", "comment"])

def add_comment(olid, comment):
    """コメントを追加する"""
    initialize_comments_file()
    with open(COMMENTS_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        comment_id = sum(1 for _ in open(COMMENTS_FILE, encoding="utf-8"))  # 行数をIDとして使用
        writer.writerow([comment_id, olid, comment])

def get_comments(olid):
    """指定されたOLIDに関連するコメントを取得する"""
    initialize_comments_file()
    comments = []
    with open(COMMENTS_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["olid"] == olid:
                comments.append({"id": row["id"], "comment": row["comment"]})
    return comments

def delete_comment(comment_id):
    """コメントを削除する"""
    initialize_comments_file()
    rows = []
    with open(COMMENTS_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["id"] != comment_id:
                rows.append(row)
    with open(COMMENTS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "olid", "comment"])
        writer.writeheader()
        writer.writerows(rows)