import requests


def search_keyword(keyword, limit=100):
    """
    書籍または著者をキーワードで検索する関数

    Args:
        keyword (str): 検索キーワード
        search_type (str): "book" または "author"
        limit (int): 取得する結果数

    Returns:
        dict: 検索結果
    """
    if keyword != "":
        url = f"https://openlibrary.org/search.json"
        params = {"q": keyword, "limit": limit}
    else:
        return {"docs": []}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_book_cover(cover_id, size="L"):
    """
    書籍のカバー画像URLを取得する関数

    Args:
        cover_id (int or str): Open LibraryのカバーID
        size (str): 画像サイズ ("S", "M", "L")

    Returns:
        str: カバー画像のURL
    """
    if cover_id is None:
        return "./img/app/no_image.jpg"
    return f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"


def fetch_books_with_details(keyword):
    """
    キーワードを使用して書籍情報を取得し、
    カバー画像URL、タイトル、著者名、出版年、OLIDを含むJSONを返す関数

    Args:
        keyword (str): 検索キーワード

    Returns:
        list: 書籍情報のリスト (各書籍は辞書形式)
    """
    results = search_keyword(keyword, limit=50)
    books = []

    for book in results.get("docs", []):
        book_details = {
            "cover_url": get_book_cover(book.get("cover_i")),
            "title": book.get("title", "タイトルなし"),
            "author": book.get("author_name", ["著者不明"])[0],
            "publish_year": book.get("first_publish_year", "不明"),
            "olid": book.get("key", "").split("/")[-1] if book.get("key") else None
        }
        books.append(book_details)

    return books
