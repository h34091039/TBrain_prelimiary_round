# import torch
import json
# import re
import jieba
# import pandas as pd
# from tqdm import tqdm
# import re
from m3 import M3_retrieve
from bm25 import BM25_retrieve

qs_path = './questions_preliminary.json' # 設定問題檔的路徑
with open(qs_path, 'rb') as f: 
    qs_ref = json.load(f)  # 讀取問題檔案

path_to_insurance = "./processed_reference/insurance.json"
with open(path_to_insurance, 'rb') as f_s: # orig: insurance.json
    corpus_dict_insurance = json.load(f_s)
    corpus_dict_insurance = {int(key): value for key, value in corpus_dict_insurance.items()}

path_to_finance = "./processed_reference/finance.json" 
with open(path_to_finance, 'rb') as f_s: # orig: cleaned_finance.json
    corpus_dict_finance = json.load(f_s)  # 讀取參考資料文件
    corpus_dict_finance = {int(key): value for key, value in corpus_dict_finance.items()}

path_to_faq = "./processed_reference/faq.json"
with open(path_to_faq, 'rb') as f_s:
    corpus_dict_faq = json.load(f_s)  # 讀取參考資料文件
    corpus_dict_faq = {int(key): value for key, value in corpus_dict_faq.items()}

answer_dict = {"answers": []}  # 初始化字典
jieba.load_userdict('custom_dict.txt')

# 根據查詢語句和指定的來源，檢索答案
for i,q_dict in enumerate(qs_ref['questions']):
        if q_dict['category'] == 'finance':
            retrieved = BM25_retrieve(q_dict['query'], q_dict['source'], corpus_dict_finance, i) # 使用BM25處理finance類別的問題
        elif q_dict['category'] == 'insurance':
            retrieved = M3_retrieve(q_dict['query'], q_dict['source'], corpus_dict_insurance, i) # 使用M3處理insurance類別的問題
        elif q_dict['category'] == 'faq':
            retrieved = M3_retrieve(q_dict['query'], q_dict['source'], corpus_dict_faq, i) # 使用M3處理faq類別的問題
        else:
            raise ValueError("Something went wrong")  # 如果過程有問題，拋出錯誤
        answer_dict['answers'].append({"qid": q_dict['qid'], "retrieve": retrieved})

# 將答案字典保存為json文件
with open('./pred_retrieve.json', 'w', encoding='utf8') as f:
    json.dump(answer_dict, f, ensure_ascii=False, indent=4)  # 儲存檔案，確保格式和非ASCII字符

# with open('./ground_truths_example.json', 'rb') as file:
#     ground_truths = json.load(file)['ground_truths']

# with open('./pred_retrieve.json', 'rb') as file:
#     pred_retrieve = json.load(file)['answers']

# correct = 0
# wrong = []
# val = {'faq': 0, 'finance': 0, 'insurance': 0}


# for i in range(150):
#     if ground_truths[i]['qid'] != pred_retrieve[i]['qid']:
#         continue
#     if str(ground_truths[i]['retrieve']) != str(pred_retrieve[i]['retrieve']):
#         wrong.append({'qid': i+1, 'question': qs_ref['questions'][i]['query'], 'actual': ground_truths[i]['retrieve'], 'predict': pred_retrieve[i]['retrieve'], 'category': ground_truths[i]['category']})
#         val[ground_truths[i]['category']] += 1
#         continue
#     correct += 1

# print('Accuracy:', correct/150)
# print('Wrong:', len(wrong))
# print('Wrong qid:')
# for w in wrong:
#     print(w)
# print('Val:', val)
