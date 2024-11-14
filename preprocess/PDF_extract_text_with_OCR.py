import os
import pdfplumber
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  #需要事先下載並調整成你檔案的路徑
from pdf2image import convert_from_path
import cv2  # 引入OpenCV進行圖片預處理
import numpy as np

def read_pdf(pdf_loc, page_infos: list = None):
    '''
    從PDF檔案中提取文字內容。

    參數:
        pdf_loc (str): PDF檔案的路徑
        page_infos (list, optional): 包含起始和結束頁碼的列表，格式為 [起始頁碼, 結束頁碼]
                                   若為None，則處理所有頁面

    返回:
        str: 提取出的文字內容。若無法提取則返回空字串

    使用方式:
        text = read_pdf("example.pdf", [0, 5])  # 提取前5頁的內容
        text = read_pdf("example.pdf")  # 提取所有頁面的內容
    '''
    pdf = pdfplumber.open(pdf_loc)  # 打開指定的PDF文件
    pages = pdf.pages[page_infos[0]:page_infos[1]] if page_infos else pdf.pages
    pdf_text = ''
    for _, page in enumerate(pages):
        text = page.extract_text()  # 提取頁面的文本內容
        if text:
            pdf_text += text
    pdf.close()  # 關閉PDF文件
    return pdf_text  # 返回萃取出的文本

def read_pdf_with_ocr(pdf_loc):
    '''
    使用OCR技術從PDF檔案中提取文字內容。
    適用於無法直接提取文字的掃描版PDF文件。

    參數:
        pdf_loc (str): PDF檔案的路徑

    返回:
        str: 使用OCR識別出的文字內容

    處理步驟:
        1. 將PDF轉換為圖片
        2. 對圖片進行預處理（灰階化、二值化、去噪）
        3. 使用Tesseract OCR進行文字識別
        4. 合併所有頁面的識別結果

    注意事項:
        - 需要安裝Tesseract OCR引擎
        - 需要安裝poppler並設定正確的路徑
        - 預設使用繁體中文進行識別
    '''
    images = convert_from_path(pdf_loc, poppler_path='C:/poppler-24.08.0/Library/bin')  # 將PDF頁面轉換為圖片  #poppler 需要事先下載並調整成你檔案的路徑
    ocr_text = ''
    for image in images:
        # 將PIL圖片轉換為OpenCV格式
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # 圖片預處理：灰階化、二值化、去噪
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        denoised = cv2.medianBlur(binary, 3)  # 使用中值濾波去噪點
        
        # 使用OCR提取圖片中的文字
        text = pytesseract.image_to_string(denoised, lang='chi_tra')  # 使用繁體中文OCR
        ocr_text += text
    return ocr_text

if __name__ == "__main__":
    '''
    主程式進入點：
    1. 檢查指定的資料夾是否存在
    2. 遍歷資料夾中所有PDF檔案
    3. 對每個PDF檔案：
       - 嘗試直接提取PDF文字內容
       - 若無法直接提取，則使用OCR技術進行識別
    4. 將每個PDF的提取內容保存到對應的文件中
    
    輸出文件:
        對每個處理的PDF檔案會產生一個對應的輸出文件：
        - {pdf檔名}.txt: 原始提取的文字內容
    '''
    folder_path = 'reference/finance'  # 設定要讀取的資料夾路徑
    
    if not os.path.exists(folder_path):
        print(f"指定的資料夾 {folder_path} 不存在。")
        exit()
        
    # 取得資料夾中所有的PDF檔案
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"在 {folder_path} 中未找到任何PDF檔案。")
        exit()
        
    print(f"找到 {len(pdf_files)} 個PDF檔案，開始處理...")
    
    # 建立輸出資料夾
    output_folder = 'output'    # 設定成你要放入輸出txt file 的資料夾路徑
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 處理每個PDF檔案
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        pdf_name = os.path.splitext(pdf_file)[0]
        print(f"\n處理檔案: {pdf_file}")
        
        # 提取文字
        extracted_text = read_pdf(pdf_path)
        if not extracted_text:
            print(f"PDF {pdf_file} 無法提取出任何文字內容，嘗試使用OCR進行處理。")
            extracted_text = read_pdf_with_ocr(pdf_path)
            
        if extracted_text:
            # 儲存提取的文字
            output_path = os.path.join(output_folder, f"{pdf_name}.txt")
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(extracted_text)
                
            print(f"成功處理 {pdf_file}:")
            print(f"- 文字內容已保存至: {output_path}")
        else:
            print(f"無法從 {pdf_file} 提取出任何文字內容，即使用了OCR技術。")
    
    print("\n所有PDF檔案處理完成。")

    