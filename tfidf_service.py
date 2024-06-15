import requests
from bs4 import BeautifulSoup

from pythainlp import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import urljoin
from nomalizing import normalize


class TfidfService:
    TDIDFVECTORIZER = TfidfVectorizer()
    TDIDFVECTOR = None
    DOCS = {'doc-token': [], 'web-link': []}

    @staticmethod
    def setup_doc(doc_token):
        TfidfService.TDIDFVECTOR = TfidfService.TDIDFVECTORIZER.fit_transform(doc_token)

    @staticmethod
    def set_doc_list(docs):
        TfidfService.DOCS = docs

    @staticmethod
    def query_result(query):
        return TfidfService.TDIDFVECTORIZER.transform([query])

    @staticmethod
    def getPageInfo(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.title.string.strip() if soup.title else None
            if title:
                title_words = title.split()[:2]
                title = ' '.join(title_words)

            icon_url = None
            for tag in soup.find_all('link', rel=lambda value: value and value.lower() in ['icon', 'shortcut icon']):
                icon_url = urljoin(url, tag['href'])
                break

            description = None
            for tag in soup.find_all('p'):
                text = tag.get_text().strip()
                if len(text) > 0:
                    description = text[:200]
                    break

            return title, icon_url, description

        except Exception as e:
            print(f"Error fetching information from {url}: {e}")
            return None, None, None

    @staticmethod
    def search(query, result_quantity, docs):
        clear_words = []
        query_word_seg = word_tokenize(query, keep_whitespace=False)

        for i, q_word in enumerate(query_word_seg):
            clear = normalize(q_word)
            clear_words.append(clear)
        query_str = ' '.join(clear_words)

        query_vector = TfidfService.query_result(query_str)
        similarity_scores = list(enumerate(cosine_similarity(query_vector, TfidfService.TDIDFVECTOR)[0]))
        sorted_similar_docs = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        sorted_similar_docs[0], sorted_similar_docs[2] = sorted_similar_docs[2], sorted_similar_docs[0]
        # ranking_ids = []
        # web_lists = []
        query_result = []
        for i, (doc_idx, similarity_score) in enumerate(sorted_similar_docs[:result_quantity]):
            link = docs['web-link'][doc_idx]
            print(f"{i + 1}. {link} (Similarity score: {similarity_score:.4f})")
            title, icon, description = TfidfService.getPageInfo(link)
            json_data = {
                'title': title,
                'icon': icon,
                'link': link,
                'description': description,
            }
            query_result.append(json_data)

        return query_result
