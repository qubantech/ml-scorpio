import warnings

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

warnings.filterwarnings("ignore")


def run_jsonifier(df):
    df.index = df.index.map(str)
    df.columns = df.columns.map(str)

    js = str(df.to_dict())
    idx = [i for i, _ in enumerate(js) if _ == '"']
    js = js.replace("'", '"')
    for add, i in enumerate(idx):
        js = js[:i + add] + '\\' + js[i + add:]
    return js


def get_recs(goods_df):
    goods_name_list = goods_df["name"]

    tfidf_vectorizer = TfidfVectorizer(strip_accents="unicode")

    tfidf = tfidf_vectorizer.fit_transform(list(goods_df["description"]))
    tfidf_vectorizer.get_feature_names()

    dic_recommended_1 = {}
    for index in range(goods_df["description"].shape[0]):
        similarities_1 = linear_kernel(tfidf[index], tfidf).flatten()
        related_docs_indices_1 = (-similarities_1).argsort()[:10]

        dic_recommended_1.update(
            {
                goods_name_list[index]: [
                    goods_name_list[i] for i in related_docs_indices_1
                ]
            }
        )
    df_content_based_results_1 = pd.DataFrame(dic_recommended_1)
    df_content_based_results_1.reset_index(inplace=True)

    json_recs = run_jsonifier(df_content_based_results_1[1:4])
    return json_recs
