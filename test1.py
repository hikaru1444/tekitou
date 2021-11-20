from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import psycopg2
import random
import math
import openpyxl

connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=")
cur = connection.cursor()

ttf_file = './IPAexfont00401/ipaexg.ttf'
pdfmetrics.registerFont(TTFont('IPAexGothic', ttf_file))

w, h = portrait(A4)
print("縦幅:w=",w,"\n横幅:h=",h)
rnd = str(math.floor(random.random() * 10000))
print(rnd,"を出力します")
cv = canvas.Canvas('./PDF出力/' + rnd + '.pdf', pagesize=landscape(A4))

font_size = 12
cv.setFont('IPAexGothic', font_size)

cur.execute("select sityoson as 住所（所在地）,komon_mei,sinkoku_kubun,kanyo_kaishibi,kanyo_keitai from komon_list where bunrui=%s AND kankatsu=%s",('1','2'))
p = cur.fetchall()
cur.execute("select count(komon_mei) from komon_list where bunrui=%s AND kankatsu=%s",('1','2',))
p_count = cur.fetchall()
print("p_count=",p_count)
cur.close()
connection.close()

#ヘッダー部分
#第１引数がx軸、第二引数がy軸,ページの左下が(0,0)となる
cv.drawCentredString(420, w - 20, "名簿")
cv.drawRightString(h - 20, w-40, "所在地　　")
cv.drawRightString(h - 20, w-60, "名　　　　印")
cv.drawRightString(h - 20, w-80, "電話　    ")
cv.drawString(20, w-40, "令和3年　4月1日")
cv.drawString(20, w-60, "    管轄内")
cv.drawString(20, w-140, "住所（所在地）")
cv.drawRightString(h - 40, w-140, "氏名（名称）　申告区分　関与開始  　関与形態　消費税　電子申告の有無")
#cv.drawString(20, w-160, "ああああいああああいああああいああああいああああいあああい")

#メイン部分
#55行出したい場合は2ぺーに20行ずつ出力し余りの5行を3ページ目に出力
#p[][]にテーブルから取り出したデータが入っている
#座標やif文内の20は書類に応じて変更してください
if p_count[0][0] >= 20:
    syo = p_count[0][0] // 20
    amari = p_count[0][0] % 20
else:
    syo = 0
    amari = p_count[0][0]

j_count = 0
for i in range(syo):
    for j in range(20):
        cv.drawString(20, w-180 - j * 20, p[j_count][0])
        cv.drawString(400, w-180- j * 20, p[j_count][1])
        cv.drawString(500, w-180- j * 20, p[j_count][2])
        cv.drawString(550, w-180- j * 20, p[j_count][3])
        cv.drawString(640, w-180- j * 20, p[j_count][4])
        j_count+=1
    cv.showPage()
    cv.setFont('IPAexGothic', font_size)

for j in range(amari):
    cv.drawString(20, w-180 - j * 20, p[j_count][0])
    cv.drawString(400, w-180- j * 20, p[j_count][1])
    cv.drawString(500, w-180- j * 20, p[j_count][2])
    cv.drawString(550, w-180- j * 20, p[j_count][3])
    cv.drawString(640, w-180- j * 20, p[j_count][4])
    j_count+=1

cv.save()