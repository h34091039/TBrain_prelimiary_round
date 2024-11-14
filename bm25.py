import jieba
import re
from rank_bm25 import BM25Okapi
from tools import align_expression

words_to_remove = ['在', '的', '非', '及', '中', '要', '仍', '後', '並', '或', '於', '是', '嗎']

def BM25_retrieve(qs, source, corpus_dict, cat):
    jieba.load_userdict('custom_dict.txt')

    qs = re.sub(r'[^\w\s]', '', qs)

    csv_path = r"TW_comp_list.csv"
    qs = align_expression(qs, csv_path)


    tokenized_query = set(jieba.lcut(qs))

    for query in tokenized_query:
        jieba.suggest_freq((query, '1000'), tune=True) # add the qs segmentations in temporily dictionary to enhance the segmentation  
    
    filtered_corpus = [corpus_dict[int(file)] for file in source]  # 多選題的選項

    tokenized_corpus = [set(jieba.lcut(txt)) for txt in filtered_corpus]

    for word in words_to_remove:
        tokenized_corpus = [[s.replace(word, '') if s == word else s for s in sublist] for sublist in tokenized_corpus]

    tokenized_corpus = [[s for s in sublist if s != ''] for sublist in tokenized_corpus]

    bm25 = BM25Okapi(tokenized_corpus)  # 使用BM25演算法建立檢索模型

    ans = bm25.get_top_n(tokenized_query, list(filtered_corpus), n=1)  # 根據查詢語句檢索，返回最相關的文檔，其中n為可調整項

    a = ans[0]

    res = [key for key, value in corpus_dict.items() if value == a]

    return res[0]  # 回傳檔案名

