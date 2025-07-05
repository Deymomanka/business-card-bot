import pytesseract
from dotenv import load_dotenv
from PIL import Image
import os
import re
# from openai import OpenAI
import csv
import gspread
from google.oauth2.service_account import Credentials
import datetime

# MacやLinuxではこの設定は不要（Windowsのみパスが必要な場合あり）
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# .envからAPIキーを読み込む
# load_dotenv("../.env")
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# api_key = os.getenv("OPENAI_API_KEY")
# print(api_key)


def extract_text_from_image(image_path):

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"画像が見つかりません: {image_path}")
    image = Image.open(image_path)
    image.thumbnail((1024, 1024))
    text = pytesseract.image_to_string(image, lang='jpn')
    return text

# def parse_business_card(raw_text):
#     system_prompt = """
# あなたはOCRで読み取った名刺情報を正しく項目ごとに分けるアシスタントです。
# 以下のテキストから、次のJSON形式で出力してください：

# {
#   "name": "",
#   "company": "",
#   "position": "",
#   "address": "",
#   "postal_code": "",
#   "tel": "",
#   "mobile": "",
#   "email": ""
# }

# 不明な項目は空欄 "" にしてください。値の後に説明や記号は不要です。
# """

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": raw_text}
#     ],
#     #temperature=0.2
# )

#     return response.choices[0].message.content


def extract_info_by_regex(text):
    # result = {
    #     "name": "",
    #     "company": "",
    #     "position": "",
    #     "address": "",
    #     "postal_code": "",
    #     "tel": "",
    #     "mobile": "",
    #     "email": ""
    # }

    result = {
    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "tel": "",
    "mobile": "",
    "email": ""
}

    # メールアドレス
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    if email_match:
        result["email"] = email_match.group()

    # 携帯を先に探す
    mobile_match = re.search(r"(携帯|Mobile|Mob)[:：]?\s?(\d{2,4}-\d{2,4}-\d{3,4}|\d{10,11})", text)
    if mobile_match:
        result["mobile"] = mobile_match.group(2)
        #text = text.replace(mobile_match.group(), "")
    
    # 電話番号
    tel_match = re.search(r"(TEL|Tel|tel|電話)?[:：]?\s?(\d{2,4}-\d{2,4}-\d{3,4}|\d{10,11})", text)
    if tel_match:
        result["tel"] = tel_match.group(2)

    # # 郵便番号
    # postal_match = re.search(r"〒\d{3}-\d{4}", text)
    # if postal_match:
    #     result["postal_code"] = postal_match.group()

    # # 住所（都道府県を含む行を対象に）
    # address_match = re.search(r"(東京都|北海道|大阪府|京都府|.{2,3}県).+", text)
    # if address_match:
    #     result["address"] = address_match.group()

    # # 会社名（大文字やカタカナ含む行を推定）
    # company_lines = [line for line in text.splitlines() if re.search(r"[A-Z]{2,}|株式会社|有限会社", line)]
    # if company_lines:
    #     result["company"] = company_lines[0].strip()

    return result


def is_duplicate_entry(worksheet, data):
    existing_records = worksheet.get_all_records()
    for record in existing_records:
         if (record.get("email") and record["email"] == data.get("email")) or \
           (record.get("tel") and record["tel"] == data.get("tel")):
            return True
    return False


def save_to_gsheets(data: dict, spreadsheet_name: str, worksheet_name: str):

    scopes = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(
        "key/meishi-project-gspread.json", scopes=scopes
    )
    client = gspread.authorize(creds)

    sheet = client.open(spreadsheet_name)
    worksheet = sheet.worksheet(worksheet_name)

    if not is_duplicate_entry(worksheet, data):

        #  必要に応じて、Spreadsheetに列名を用意する（以下のコード）
        # fields = ["name", "company", "position", "address", "postal_code", "tel", "mobile", "email"]
        # worksheet.append_row([data.get(field, "") for field in fields])
        worksheet.append_row(list(data.values()))
        print("✅ データを追加しました")
    else:
        print("⚠️ すでに登録済みのデータです（スキップ）")


def process_all_images(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(folder_path, filename)
            print(f"\n📷 処理中：{filename}")
            raw_text = extract_text_from_image(full_path)
            #print(raw_text)
            #structured = parse_business_card(raw_text)
            structured = extract_info_by_regex(raw_text)
            print("📦 構造化結果：")
            print(structured)
            save_to_gsheets(structured, spreadsheet_name="名刺登録一覧", worksheet_name="シート1")


if __name__ == "__main__":
    process_all_images("images/")

