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


def fetch_book_by_olid(olid):
    """
    OLIDを使用して単一の書籍詳細を取得する関数

    Args:
        olid (str): Open Library ID

    Returns:
        dict: 書籍詳細情報 (辞書形式) またはNone
    """
    try:
        url = f"https://openlibrary.org/works/{olid}.json"
        response = requests.get(url)
        response.raise_for_status()
        book_data = response.json()
        
        # 著者情報を取得
        authors = []
        if "authors" in book_data:
            for author in book_data["authors"]:
                if "author" in author:
                    author_key = author["author"]["key"]
                    author_url = f"https://openlibrary.org{author_key}.json"
                    author_response = requests.get(author_url)
                    if author_response.status_code == 200:
                        author_data = author_response.json()
                        authors.append(author_data.get("name", "著者不明"))
        
        # カバー画像IDを取得
        cover_id = None
        if "covers" in book_data and book_data["covers"]:
            cover_id = book_data["covers"][0]
        
        book_details = {
            "cover_url": get_book_cover(cover_id),
            "title": book_data.get("title", "タイトルなし"),
            "author": authors[0] if authors else "著者不明",
            "publish_year": book_data.get("first_publish_date", "不明"),
            "olid": olid
        }
        
        return book_details
    except Exception as e:
        print(f"Error fetching book with OLID {olid}: {e}")
        return None
