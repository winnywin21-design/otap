# -*- coding: utf-8 -*-
"""배포된 GitHub Pages 주소로 학생용/교사용 QR 코드 생성.
- qr/ 폴더에 단원별 PNG 8장
- qr/_시트.png 인쇄용 모음 1장 (단원별 2개 QR + 라벨)
"""
import qrcode, pathlib, sys, io
from PIL import Image, ImageDraw, ImageFont
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = "https://winnywin21-design.github.io/otap"
UNITS = [
    ("unit1", "Ⅰ. 다항식"),
    ("unit2", "Ⅱ. 방정식과 부등식"),
    ("unit3", "Ⅲ. 경우의 수"),
    ("unit4", "Ⅳ. 행렬"),
]
HERE = pathlib.Path(__file__).parent
QDIR = HERE / "qr"
QDIR.mkdir(exist_ok=True)

def make_qr(url, box=10):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=box, border=2)
    q.add_data(url); q.make(fit=True)
    return q.make_image(fill_color="black", back_color="white").convert("RGB")

def load_font(size):
    for name in ["malgun.ttf", "malgunbd.ttf", "C:/Windows/Fonts/malgun.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()

# 개별 QR 저장
saved = []
for slug, title in UNITS:
    for role, kor in [("student", "학생용"), ("teacher", "교사용")]:
        url = f"{BASE}/{slug}/{role}.html"
        img = make_qr(url)
        fn = QDIR / f"{slug}_{role}.png"
        img.save(fn)
        saved.append((title, kor, url, fn.name))
        print("저장:", fn.name, "->", url)

# 인쇄용 모음 시트
qr_px = 220
pad = 28
col_w = qr_px + pad
title_f = load_font(34)
label_f = load_font(22)
url_f = load_font(13)
row_h = 60 + qr_px + 60
sheet_w = col_w * 2 + pad * 3
sheet_h = 70 + row_h * len(UNITS) + pad
sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
d = ImageDraw.Draw(sheet)
d.text((pad, 24), "미래엔 공통수학1 오답 노트 — 단원별 QR", font=title_f, fill="black")

for ui, (slug, title) in enumerate(UNITS):
    y0 = 80 + ui * row_h
    d.text((pad, y0), title, font=label_f, fill=(31, 59, 110))
    for ci, (role, kor) in enumerate([("student", "학생용"), ("teacher", "교사용")]):
        x0 = pad + ci * (col_w + pad)
        qimg = make_qr(f"{BASE}/{slug}/{role}.html", box=6).resize((qr_px, qr_px))
        sheet.paste(qimg, (x0, y0 + 36))
        d.text((x0, y0 + 36 + qr_px + 6), kor, font=label_f, fill="black")
        d.text((x0, y0 + 36 + qr_px + 34), f"{slug}/{role}.html", font=url_f, fill=(120, 120, 120))

sheet_path = QDIR / "_QR시트_인쇄용.png"
sheet.save(sheet_path)
print("\n인쇄용 시트:", sheet_path)
print("총", len(saved), "개 QR 생성 완료")
