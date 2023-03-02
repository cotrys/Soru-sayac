from flask import Flask, render_template, request
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ders = request.form['ders']
        soru_sayisi = int(request.form['soru_sayisi'])
        kaydet(ders, soru_sayisi)
    return render_template('index.html', dersler=['Türkçe', 'Fen Bilgisi', 'İngilizce', 'Matematik', 'Tarih', 'Din Kültürü'])

@app.route('/sonuclar')
def sonuclar():
    dersler = ['Türkçe', 'Fen Bilgisi', 'İngilizce', 'Matematik', 'Tarih', 'Din Kültürü']
    toplam_sorular = {ders: 0 for ders in dersler}
    gunluk_sorular = {ders: 0 for ders in dersler}
    gunluk_ortalama = {ders: 0 for ders in dersler}
    sonuc = {}
    try:
        with open('sonuclar.json', 'r') as f:
            veriler = json.load(f)
            for ders in dersler:
                for tarih, soru_sayisi in veriler.get(ders, {}).items():
                    tarih = datetime.strptime(tarih, '%Y-%m-%d')
                    toplam_sorular[ders] += soru_sayisi
                    if tarih >= datetime.now() - timedelta(days=30):
                        gunluk_sorular[ders] += soru_sayisi
                gunluk_ortalama[ders] = gunluk_sorular[ders] // 30
            sonuc = {
                'toplam_sorular': toplam_sorular,
                'gunluk_sorular': gunluk_sorular,
                'gunluk_ortalama': gunluk_ortalama
            }
    except FileNotFoundError:
        pass
    return render_template('sonuclar.html', sonuc=sonuc)

def kaydet(ders, soru_sayisi):
    try:
        with open('sonuclar.json', 'r') as f:
            veriler = json.load(f)
    except FileNotFoundError:
        veriler = {}
    tarih = datetime.now().strftime('%Y-%m-%d')
    veriler.setdefault(ders, {}).setdefault(tarih, 0)
    veriler[ders][tarih] += soru_sayisi
    with open('sonuclar.json', 'w') as f:
        json.dump(veriler, f)

if __name__ == '__main__':
    app.run(debug=True)
