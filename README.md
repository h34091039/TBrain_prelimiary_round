# 預處理程式碼說明

主程式為 `PDF_text_with_OCR.py`  
在預處理的程式中，針對讀取 PDF 檔案的部分，採用了兩種支援讀檔的方式：

1. **使用 `pdfplumber` 讀取 PDF**：
   - 程式首先嘗試使用 **主辦單位所提供的 `pdfplumber`** 來讀取 PDF 檔案的文字內容。
   - **限制**： `pdfplumber` 無法讀取影像類型的 PDF 檔案（如掃描版 PDF），如果檔案為影像類型，則 `pdfplumber` 會回傳空字串。

2. **使用 Tesseract OCR 讀取影像類型 PDF**：
   - 當 `pdfplumber` 回傳空字串時，程式會自動切換讀檔方式，改用 **Tesseract OCR** 進行文字識別。
   - 這種方式可以處理掃描版或含有影像的 PDF 檔案，提取其中的文字。

## 輸出說明

- 程式會根據程式碼內的 `output_folder` 變數所指定的路徑，自動建立一個資料夾。
- 程式會遍歷 `folder_path` 變數所指定的資料夾內所有 PDF 檔案，將讀取出的文字內容儲存為 `.txt` 檔，並存放於 `output_folder` 底下。

## Tesseract OCR 概述

Tesseract OCR 是一款開源的光學字符識別（OCR，Optical Character Recognition）引擎，用於將印刷或手寫的文本從圖像或掃描文件中提取為可編輯的文本格式。

## 環境建立

### 安裝 Poppler

`pdf2image` 需要 **Poppler** 來將 PDF 轉換為圖像，請依照以下步驟進行安裝：

### **Windows**

1. 下載 Poppler for Windows：[Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
2. 解壓縮下載的文件，找到 `bin` 資料夾。
3. 將 `bin` 資料夾的路徑（例如 `C:\path\to\poppler\bin`）添加到系統的 **環境變數** 中：
   - 在 Windows 搜索欄中輸入 **「環境變數」** 並打開 **「編輯系統環境變數」**。
   - 點擊 **「環境變數」** 按鈕。
   - 在 **「系統變數」** 中找到 **Path**，點擊 **「編輯」**。
   - 點擊 **「新增」** 並輸入 Poppler 的 `bin` 路徑（例如 `C:\poppler-23.08.0\Library\bin`）。
   - 點擊 **「確定」** 保存設置。

### **macOS**

1. 使用 **Homebrew** 安裝 Poppler：
   ```bash
   brew install poppler
   ```

### **Linux**

1. 使用 **sudo apt install** 安裝 Poppler：
   ```bash
   sudo apt install poppler-utils
   ```

### PDF_extract_text_with_OCR.py 使用方法

以主辦單位所提供的 `./reference/finance` 資料夾為例（路徑請自行更換）：

請在程式碼內修改以下變數：

```python
# 設定檔案資料夾路徑 (以下 finance 可替換成 insurance)
folder_path = './reference/finance'
output_folder = './output/finance'  # 產⽣的文字檔將被儲存在這個資料夾底下。
```

## 安裝指令

```bash
pip install -r requirements.txt
```

# retrieve模型程式碼說明

主程式為  main.py  包含了兩種模型 M3 與 BM25，此程式利用了兩種不同的模型針對不同類型的問題，來優化整體 retrieve 的表現。  

- faq 類型 以 M3 處理
- finance 類型 以 BM25 處理
- insurance 類型 以 M3 處理

此程式需要從外部引入三個 Python 程式: 
1. tools.py # 裡面包含處理正則表示的函數
2. bm25.py
3. m3.py

其中，
- tools.py
  1. 正則表示統一函數  align_expression(input_text, csv_path) 
     此函數需用到  TW_comp_list.csv  檔案，讀取台灣所有公司名稱的相關資訊
  2. 此函數會在  bm25.py  與  m3.py  中被使用到

-  bm25.py 
   - 四個前處理方法:
      1. 正則表達統一
         正則表達式將不一致的表達式統一，如: 公司全名/縮寫/英文名、民國/西元、台/臺、中文數字/阿拉伯數字等。
      2. 客製化切詞
         將財經、保險相關用語加入 jieba 的客製化辭典中，使切詞更為精確。
      3. 動態調整切詞
         根據問句的切詞結果，來動態影響文本的切詞方式。實作方法為: 將問句切詞後的所有切詞結果以最高的權重，加入 jieba 客製化的切詞辭典中，再以強化後的 jieba 對文本做切詞。
      4. 過濾非關鍵字
         將語句中非關鍵詞移除，例如: ['在', '的', '非', '及', '中', '要', '仍', '後', '並', '或', '於', '是', '嗎']，使模型能更著重在關鍵字上。
   - 模型:
      1. 相似度模型計算並無改變，與 baseline 一樣

-  m3.py 
   - 前處理 (部分與 BM25 的前處理重疊):
      1. 正則表達統一
      2. 客製化切詞
   - 模型:
      1. 把文檔以句子為單位切詞 (切句)，並將文檔中與問題最相關的句子作為該文檔的代表，以此計算所有選項文檔與問句的相似度。
      2. 選擇性過濾掉文檔中不含 **與問句相關關鍵字** 的句子，目的為降低模型大小，與提升處理效率。

## 輸入說明

- 程式會根據程式碼內的 `qs_path = './questions_preliminary.json'` 變數所指定的路徑，讀取問題。
- 程式會根據程式碼中的以下變數：
  - `path_to_insurance = "./processed_reference/insurance.json"`
  - `path_to_faq = "./processed_reference/faq.json"`
  - `path_to_finance = "./processed_reference/finance.json"`
  
  讀取預處理過後的 JSON 檔案，並將讀取出的內容用於後續的模型處理。


**注意**  
本模型所使用的輸入 JSON 檔是經過人工處理後的結果，所以此結果無法完全從上述前處理的程式碼中重現。  
人工處理包含：
1. 人工查看讀取品質不佳的檔案（大約 12 個），並利用 Google 網站上的 OCR 工具或 Line 支援的 OCR 工具將這些檔案重新讀取成文字檔。
2. 人工查看文件中的關鍵字，並將關鍵字加入切詞的詞典中。

## 輸出說明

- 程式會將結果檔 `pred_retrieve.json` 輸出至當前資料夾。

## 必要的附加檔案

1. **`costum_comp.txt`**  
   所有公司的縮寫名稱，在 `m3.py` 中會用到。
   
2. **`costum_dict.txt`**  
   客製化的切詞辭典，在 `bm25.py` 與 `m3.py` 中會用到。
   
3. **`requirements.txt`**  
   所有需要用到的 package 列表。
4. **`TW_comp_list.csv`**  
   讀取台灣所有公司名稱的相關資訊
