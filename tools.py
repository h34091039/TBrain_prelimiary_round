import re
import pandas as pd

def align_expression(text, csv_path): 
    '''
    This function is for regex substitution (pipeline substution)
    '''

    # This section is for 臺 to 台-------------------------------------------------
    T_to_t = {'臺': '台'}
    for pattern, replacement in T_to_t.items():
        # Perform the replacement for each pattern in the dictionary
        text = re.sub(pattern, replacement, text)
    #-------------------------------------------------------------------------------

    # This section is for Chinese numbers to arabic numbers-------------------------------------------------
    Chinese_to_arabic = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '零': '0', '○': '0'}
    for pattern, replacement in Chinese_to_arabic.items():
        # Perform the replacement for each pattern in the dictionary
        text = re.sub(pattern, replacement, text)
    #-------------------------------------------------------------------------------

    # This section is for 民國轉西元--------------------------------
    def replace(match):
        # 獲取捕獲到的年分
        year = int(match.group(2))  # 改為 group(2)，因為第二組捕獲是數字部分
        
        # 如果匹配的是民國年份，將其轉換為西元年份
        gregorian_year = year + 1911
        return f"{gregorian_year}年"
    
    # Regex pattern to match "民國" followed by a number and "年"
    pattern = r"(民國)?(\d{3})年" 
    # Perform the substitution using the replace function
    text = re.sub(pattern, replace, text)
    #---------------------------------------------------------------

    # This section is for convert the company name to simplified form
    df = pd.read_csv(csv_path) # convert csv to dataframe

    company_lst_simp = df[:][['公司名稱', '公司簡稱']].values.tolist()  
    fullTosimp_dict = {c[0]: c[1] for c in company_lst_simp} # create the map dictionary for full name to simplified name

    semiTosimp_dict = {c[0].replace("股份有限公司", ""): c[1] for c in company_lst_simp} # create the map dictionary for full name to simplified name

    company_lst_Eng = df[:][['英文簡稱', '公司簡稱']].values.tolist()  
    EngTosimp_dict = {c[0]: c[1] for c in company_lst_Eng} # create the map dictionary for English name to simplified name

    for pattern, replacement in fullTosimp_dict.items():
        # Perform the replacement for each pattern in the dictionary
        text = re.sub(pattern, replacement, text)
    
    for pattern, replacement in semiTosimp_dict.items():
        # Perform the replacement for each pattern in the dictionary
        text = re.sub(pattern, replacement, text)

    for pattern, replacement in EngTosimp_dict.items():
        # Perform the replacement for each pattern in the dictionary
        text = re.sub(pattern, replacement, text)
    #-----------------------------------------------------------------

    # This section is for insurance term substituition 
    insurance_map_dict = {'保險單': '保單', '保險額': '保額'}
    for pattern, replacement in insurance_map_dict.items():
        # Perform the replacement for each pattern in the dictionary
        text = re.sub(pattern, replacement, text)
    #-----------------------------------------------------------------
    return text