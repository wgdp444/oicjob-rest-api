from database import db
from models.models import JobOffer, Industry, Subject
from app import app


with app.app_context():
    # industrys
    insert_datas = ["IT", "医療", "銀行・証券", "官公庁", "機械・プラント", "不動産"]
    for insert_data in insert_datas:
        db.session.add(Industry(insert_data))
    db.session.commit()

    # job_offers
    insert_datas = [
        ["システムバックスペースプライス", 1, "システムエンジニア", 10, 180000, "test"],
        ["ORARA", 1, "フルスタックエンジニア", 10, 230000, "test"],
        ["百菱地所", 6, "正社員", 10, 500000, "test"],
        ["マクロナルド", 5, "オペレーター", 10, 330000, "test"],
        ["クラシッキ中央病院", 2, "看護師", 10, 100000, "test"],
    ]
    for insert_data in insert_datas:
        db.session.add(JobOffer(*insert_data))
    
    insert_datas = ["情報システム学科", "医療福祉事務学科", "診療情報管理士学科", 
                    "ホテル・ブライダル学科", "経営アシスト学科", "公務員学科・公務員速習学科",
                    "保育学科", "情報スペシャリスト学科", "ゲームクリエイター・ゲームプログラマー学科", 
                    "データマーケター学科", "ネット・動画クリエイター学科", "CGデザイン学科"]
    for insert_data in insert_datas:
        db.session.add(Subject(insert_data))

    db.session.commit()
    

