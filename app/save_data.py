# データ保存（CSV or Google Sheets）
import csv
import os
import gspread
from google.oauth2.service_account import Credentials

# 仮の構造化済みデータ（OCR→GPT処理後の想定形式）
dummy_data = {
    "name": "広告 太郎",
    "company": "光広告株式会社",
    "position": "営業部長",
    "address": "福岡県福岡市博多区博多駅前3-23-17",
    "postal_code": "812-0011",
    "tel": "092-409-8228",
    "mobile": "070-5698-7077",
    "email": "info@f-koukou.co.jp"
}

dummy_data_2 = {
    "name": "田中　一郎",
    "company": "IT株式会社",
    "position": "エンジニア",
    "address": "東京都品川区",
    "postal_code": "111-2211",
    "tel": "098-407-6784",
    "mobile": "070-5698-7077",
    "email": "it_tarou@f-koukou.co.jp"
}


# def save_to_csv(data, csv_path="../data/saved.csv"):
#     os.makedirs(os.path.dirname(csv_path), exist_ok=True)
#     file_exists = os.path.isfile(csv_path)

#     with open(csv_path, mode="a", newline="", encoding="utf-8") as f:  # 既存のデータの次に、新しいデータを追加する。つまり末尾に１行ずつ追加されます。
#         writer = csv.DictWriter(f, fieldnames = data.keys())
#         if not file_exists:
#             writer.writeheader()
#         writer.writerow(data)

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
        "../key/meishi-project-gspread.json", scopes=scopes
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



if __name__ == "__main__":
    #save_to_csv(dummy_dat_2)
    save_to_gsheets(dummy_data_2, spreadsheet_name="名刺登録一覧", worksheet_name="シート1")
    print("✅ 完了")
    