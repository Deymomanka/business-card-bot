from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage, TextSendMessage
import os
from dotenv import load_dotenv
from app.ocr import extract_text_from_image, extract_info_by_regex, save_to_gsheets

app = Flask(__name__)

load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

json_path = "key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path

@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    # まず即レス
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="名刺を処理中です。少しお待ちください！")
    )

    message_id = event.message.id
    image_path = f"images/{message_id}.jpg"
    content = line_bot_api.get_message_content(message_id)

    with open(image_path, "wb") as f:
        for chunk in content.iter_content():
            f.write(chunk)

    #print(f"✅ 画像を保存しました: {image_path}")

    # OCRと正規表現による構造化
    text = extract_text_from_image(image_path)
    structured_data = extract_info_by_regex(text, message_id)

    print("📦 構造化結果：")
    print(structured_data)

    save_to_gsheets(structured_data, spreadsheet_name="名刺登録一覧", worksheet_name="シート1")

    # LINEへ結果を返信
    user_id = event.source.user_id
    line_bot_api.push_message(
        user_id,
        TextSendMessage(
            text=f"名刺情報:\nDate: {structured_data['date']}\nEmail: {structured_data['email']}\nPhone: {structured_data['tel']}\nMobile: {structured_data['mobile']}")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
