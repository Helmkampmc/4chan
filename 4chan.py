import requests
from bs4 import BeautifulSoup  # Correctly using BeautifulSoup from beautifulsoup4
import streamlit as st

def search_4chan(key_terms):
    boards = ['g', 'pol', 'b', 'v', 'a']  # Specify the most popular 4chan boards you want to search
    results = []

    for board in boards:
        url = f'https://a.4cdn.org/{board}/catalog.json'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            for page in data:
                threads = page['threads']
                for thread in threads:
                    if 'com' in thread:
                        post_text = thread['com']
                        if any(term.lower() in post_text.lower() for term in key_terms):
                            result = f"Thread ID: {thread['no']}\n"
                            if 'sub' in thread:
                                result += f"Subject: {thread['sub']}\n"
                            result += f"Comment: {post_text}\n"
                            result += '-' * 50 + '\n'
                            results.append(result)

    if len(results) > 0:
        return results
    else:
        return "No results found on 4chan."

def search_reddit(key_terms):
    subreddit = 'popular'  # Specify the Reddit subreddit you want to search
    url = f'https://www.reddit.com/r/{subreddit}/.json'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']

        results = []
        for post in posts:
            post_data = post['data']
            title = post_data['title']
            if any(term.lower() in title.lower() for term in key_terms):
                result = f"Title: {title}\n"
                result += '-' * 50 + '\n'
                results.append(result)

        if len(results) > 0:
            return results
        else:
            return "No results found on Reddit."
    else:
        return "Unable to retrieve data from Reddit."

# Streamlit app
def main():
    st.title("4chan and Reddit Search")

    # Get user search terms
    search_terms = st.text_input("Enter search terms separated by commas")

    if search_terms:
        # Split search terms
        search_terms_list = search_terms.split(",")
        search_terms_list = [term.strip() for term in search_terms_list]

        # Search 4chan
        st.subheader("4chan Results")
        chan_results = search_4chan(search_terms_list)
        if isinstance(chan_results, list):
            for result in chan_results:
                st.text(result)
        else:
            st.text(chan_results)

        # Search Reddit
        st.subheader("Reddit Results")
        reddit_results = search_reddit(search_terms_list)
        if isinstance(reddit_results, list):
            for result in reddit_results:
                st.text(result)
        else:
            st.text(reddit_results)

if __name__ == '__main__':
    main()
