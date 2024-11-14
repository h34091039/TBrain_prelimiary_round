from FlagEmbedding import BGEM3FlagModel
import jieba
import re
from tools import align_expression


comp_set = set() # 建立公司名的set
with open("./custom_comp.txt", 'r', encoding='utf-8') as f:
    for line in f:
        comp_set.add(line.strip())

model = BGEM3FlagModel('BAAI/bge-m3',  
                       use_fp16=True)

def M3_retrieve(qs, source, corpus_dict, num):
        '''
        retrieve the best match document by M3 code
        qs: the query (string)
        source: the choices (list)
        corpus_dict: (dict)
        num: the number of question (for print, int)
        '''
        csv_path = "./TW_comp_list.csv"
        qs = align_expression(qs, csv_path)

        # -----------------------------------
        embedding_query = model.encode(qs)['dense_vecs'] # query's embedding
        tokenized_query = list(jieba.cut(qs)) # jieba's segmentation (for reducing # of embeddings)
        
        filtered_corpus = [corpus_dict[int(file)] for file in source]  # 多選題的選項

        best_doc = '' # the file retrieved
        best_similarity = 0 # the best file's similarity

        pattern = ['「','」','？','?','，','\'',',']

        if '「' in qs:
            index1 = qs.find('「')
            index2 = qs.find('」')
            tokenized_query.append(qs[index1+1:index2])

        # remove the element if it's in comp_set or patrern 
        refined_data = [ws for ws in tokenized_query if ws not in comp_set and ws not in pattern]
        print(f"refined Q{num+1}: "+str(refined_data))

        for doc in filtered_corpus:
            for sentence in re.split(r'[。；?？ ]',doc): # sentence segmentation

                #check if the sentence contain the segmented term in query, if not, ignore it
                ctr=0
                for q in refined_data:
                     if q in sentence:
                        ctr+=1
                if ctr:
                    embedding_sentence = model.encode(sentence, 
                                            batch_size=12, 
                                            max_length=256, #adjustable
                                            )['dense_vecs']
                    
                    similarity = embedding_sentence @ embedding_query.T 

                    if similarity > best_similarity: #update the best doc
                        best_similarity = similarity
                        best_doc = doc
        
        # 找回與最佳匹配文本相對應的檔案名
        res = [key for key, value in corpus_dict.items() if value == best_doc]
        return res[0]  # 回傳檔案名