# LineBot × Google OCR × Python 名刺情報登録ツール
## プロジェクト概要

PoC（概念実証）レベル開発したLineBotにより、ユーザーが送信した名刺画像から情報を抽出し、Google Spreadsheetに自動登録するPythonツール。

#### 登録する情報：
  - 名前（省略）  
  - 会社名（省略）
  - 役職（省略）
  - 住所（省略）
  - 郵便番号（省略）
  - 登録時刻
  - 電話番号
  - 携帯番号
  - 電子メール

## 使用技術・ライブラリ

- **開発環境**: VSCode  
- **コア言語**: Python3
- **その他技術**:  
  - `LINE Messaging API`（ユーザーとのチャットインターフェイス）  
  - `Flask`（Webhookサーバ）  
  - `OpenAI API`（データの構造化）
  - `Google Vision API`（OCR）
  - `Render`（クラウド環境）


## 試していただくには

#### １）以下のLine BotのQRコードのスキャン

![image](https://github.com/user-attachments/assets/00d0b0c5-f8cb-4c6b-94fb-802fbdf687c5)

#### ２）　名刺画像のアップロード

LineBotに文字が鮮明な名刺画像を送信してください。

##### ✳︎なお、3)スプレッドシートは一般に公開されているため、アップロードした名刺情報が他の方からも閲覧可能です。
##### そのため、本ツールの動作確認を目的とする場合は、以下のサンプル名刺画像や、インターネット上で公開されている名刺画像などのご利用をお勧めします。

【名刺画像の例】

#### ３）　以下のSpreadsheetでご確認ください

現在、スプレッドシートURLは準備中です。


## 注意事項

#### 1）GPT Chat API の利用について
現在、無料枠の上限を超える可能性があるため、名刺から抽出したテキストを Chat GPT API に渡す処理は停止しています。ご希望があれば、この機能を導入することも可能です。

#### 2）構造化について
上記理由により、現在は名刺情報の完全な構造化を行っておらず、登録内容はDate、Email、Phone、Mobile のみとなっています。

#### 3）ツールの拡張について
本Pythonツールには、さらに改善・拡張できる余地があります。ご要望に応じて、以下のような対応が可能です。
  - コードのカスタマイズ
  - ChatGPT APIの有効化
  - サーバー環境（RenderからHerokuなど）への移行
  - データベースの導入（名刺情報はSpreadsheetではなく、データベースに保存）
  - その他ご要望に応じたカスタマイズ

## ご相談・お問い合わせ

##### このツールの拡張やカスタマイズについてのご相談はお気軽にどうぞ。

[![Twitter](https://img.shields.io/badge/Twitter-@yourhandle-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://twitter.com/yourhandle)






