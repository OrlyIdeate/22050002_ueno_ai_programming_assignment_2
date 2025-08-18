import streamlit as st
import math
from utils.openlibrary import fetch_books_with_details, fetch_book_by_olid
from utils.CRUD import add_comment, get_comments, delete_comment, get_books_with_comments


st.title("📚️Books Comment")
st.subheader("書籍情報を取得＆コメントを記録するアプリ")

# タブを作成
tab1, tab2 = st.tabs(["書籍検索", "コメント付き書籍一覧"])

with tab1:
    query = st.text_input("書籍名や著者名を入力してください:")
    col1, col2 = st.columns([9, 1])
    with col1:
        st.write("日本語だと検索結果が少ない場合があります。英語での検索もお試しください。")
    with col2:
        search_button = st.button("検索")

    if search_button or query:
        # 検索結果をキャッシュ
        if "search_results" not in st.session_state or st.session_state["last_query"] != query:
            st.session_state["search_results"] = fetch_books_with_details(query)
            st.session_state["last_query"] = query

        results = st.session_state["search_results"]

        if results:
            st.write("検索結果一覧:")

            # ページネーション設定
            items_per_page = 5  # 1ページあたりのアイテム数
            total_items = len(results)
            total_pages = math.ceil(total_items / items_per_page)

            # 現在のページを選択
            current_page = st.number_input(
                "ページ番号：", min_value=1, max_value=total_pages, value=1, step=1)

            st.write(f"全{total_pages}ページ中 {current_page}ページ目を表示しています。")

            # 表示するデータの範囲を計算
            start_idx = (current_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_data = results[start_idx:end_idx]

            for book in page_data:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(book["cover_url"], width=200)
                with col2:
                    st.write(f"**タイトル:** {book['title']}")
                    st.write(f"**著者:** {book['author']}")
                    st.write(f"**初版発行年:** {book['publish_year']}")
                    st.write(f"**OLID:** {book['olid']}")

                # コメントを見るセクション
                with st.expander(f"コメントを見る: {book['title']}"):
                    # コメント表示
                    comments = get_comments(book['olid'])
                    for comment in comments:
                        col1, col2 = st.columns([9, 1])
                        with col1:
                            st.write(f"{comment['comment']}")
                        with col2:
                            if st.button(f"削除", key=f"delete_{comment['id']}"):
                                delete_comment(comment['id'])
                                st.rerun()

                    # コメント追加
                    new_comment = st.chat_input("コメントを入力してください", key=f"new_comment_{book['olid']}")
                    if new_comment:
                        add_comment(book['olid'], new_comment)
                        st.rerun()

                st.write("---")
        else:
            st.write("該当する書籍が見つかりませんでした。")

with tab2:
    st.write("### コメントが付いている書籍一覧")
    
    # コメントが付いている書籍のOLIDを取得
    commented_olids = get_books_with_comments()
    
    if commented_olids:
        # 各OLIDから書籍詳細を取得
        books_with_comments = []
        for olid in commented_olids:
            book_details = fetch_book_by_olid(olid)
            if book_details:
                books_with_comments.append(book_details)
        
        if books_with_comments:
            # ページネーション設定
            items_per_page = 5  # 1ページあたりのアイテム数
            total_items = len(books_with_comments)
            total_pages = math.ceil(total_items / items_per_page)

            # 現在のページを選択
            if total_pages > 1:
                current_page_comments = st.number_input(
                    "ページ番号：", min_value=1, max_value=total_pages, value=1, step=1, key="comment_page")
            else:
                current_page_comments = 1

            if total_pages > 1:
                st.write(f"全{total_pages}ページ中 {current_page_comments}ページ目を表示しています。")

            # 表示するデータの範囲を計算
            start_idx = (current_page_comments - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_data = books_with_comments[start_idx:end_idx]

            for book in page_data:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(book["cover_url"], width=200)
                with col2:
                    st.write(f"**タイトル:** {book['title']}")
                    st.write(f"**著者:** {book['author']}")
                    st.write(f"**初版発行年:** {book['publish_year']}")
                    st.write(f"**OLID:** {book['olid']}")

                # コメントを見るセクション
                with st.expander(f"コメントを見る: {book['title']}"):
                    # コメント表示
                    comments = get_comments(book['olid'])
                    for comment in comments:
                        col1, col2 = st.columns([9, 1])
                        with col1:
                            st.write(f"{comment['comment']}")
                        with col2:
                            if st.button(f"削除", key=f"delete_tab2_{comment['id']}"):
                                delete_comment(comment['id'])
                                st.rerun()

                    # コメント追加
                    new_comment = st.chat_input("コメントを入力してください", key=f"new_comment_tab2_{book['olid']}")
                    if new_comment:
                        add_comment(book['olid'], new_comment)
                        st.rerun()

                st.write("---")
        else:
            st.write("書籍情報の取得に失敗しました。")
    else:
        st.write("まだコメントが付いている書籍がありません。")
        st.write("「書籍検索」タブで書籍を検索し、コメントを追加してください。")
