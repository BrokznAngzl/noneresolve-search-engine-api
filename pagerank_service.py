import networkx as nx
from django.db import connection


def find_out_link(link_id, ref_links, link_nodes):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT  mylinks.link, myoutlinks.out_link FROM `myoutlinks`, `mylinks` WHERE myoutlinks.doc_id = mylinks.id AND mylinks.id =" + str(
            link_id)
    )
    out_links = cursor.fetchall()
    cursor.close()

    for link in out_links:
        target_link = link[0]
        out_link = link[1]

        if target_link != out_link and out_link in ref_links:
            node = (target_link, out_link)
            if node not in link_nodes:
                link_nodes.append(node)


def cal_node(link_nodes):
    G = nx.DiGraph()
    for ege in link_nodes:
        G.add_edge(*ege)

    pagerank = nx.pagerank(G, alpha=0.85)  # 15%
    popular_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)

    return popular_nodes


def combine_pagerank(docs, popular_links, similarity_tuple, trash_word):
    popularity_tuple = {item[0]: idx + 1 for idx, item in enumerate(popular_links)}

    weight_cosine = 0.7
    weight_popularity = 0.3
    combined_scores = {}
    for url, data in similarity_tuple.items():
        cosine_score = data['score']
        tfidf_id = data['tfidf_id']
        popularity_score = popularity_tuple.get(url, 1)
        combined_score = (weight_cosine * cosine_score) + (weight_popularity * (1 / popularity_score))

        combined_scores[url] = {
            "score": combined_score,
            "title": docs['doc-title'][tfidf_id],
            "icon": docs['doc-icon'][tfidf_id],
            "link": docs['doc-link'][tfidf_id],
            "description": docs['doc-body'][tfidf_id].replace(trash_word, '')[:200]
        }

    return sorted(combined_scores.items(), key=lambda item: item[1]['score'], reverse=True)
