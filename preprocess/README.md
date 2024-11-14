# 預處理程式碼說明

主程式為 `PDF_text_with_OCR.py`  
在預處理的程式中，針對讀取 PDF 檔案的部分，採用了兩種支援讀檔的方式：

1. **使用 `pdfplumber` 讀取 PDF**：
   - 程式首先嘗試使用 **主辦單位所提供的 `pdfplumber`** 來讀取 PDF 檔案的文字內容。
   - **限制**： `pdfplumber` 無法讀取影像類型的 PDF 檔案（如掃描版 PDF），如果檔案為影像類型，則 `pdfplumber` 會回傳空字串。

2. **使用 Tesseract OCR 讀取影像類型 PDF**：
   - 當 `pdfplumber` 回傳空字串時，程式會自動切換讀檔方式，改用 **Tesseract OCR** 進行文字識別。
   - 這種方式可以處理掃描版或含有影像的 PDF 檔案，提取其中的文字。

## Tesseract OCR 概述

Tesseract OCR 是一款開源的光學字符識別（OCR，Optical Character Recognition）引擎，用於將印刷或手寫的文本從圖像或掃描文件中提取為可編輯的文本格式。

## 環境建立

### 安裝指令

```bash
pip install -r requirements.txt
```
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
## PDF_extract_text_with_OCR.py 使用方法

以主辦單位所提供的 `./reference/finance` 資料夾為例（路徑請自行更換）：

請在程式碼內修改以下變數：

```python
# 設定檔案資料夾路徑 (以下 finance 可替換成 insurance)
folder_path = './reference/finance'
output_folder = './output/finance'  # 產⽣的文字檔將被儲存在這個資料夾底下。
```
## 輸出說明

- 程式會根據程式碼內的 `output_folder` 變數所指定的路徑，自動建立一個資料夾。
- 程式會遍歷 `folder_path` 變數所指定的資料夾內所有 PDF 檔案，將讀取出的文字內容儲存為 `.txt` 檔，並存放於 `output_folder` 底下。