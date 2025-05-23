# Fuzzy Öğrenci Notlandırma Sistemi

Bu proje, bulanık mantık (fuzzy logic) teknikleri kullanarak öğrencilerin **Final Notu** ve **Destek (Rehberlik) İhtiyacı** düzeylerini hesaplayan bir Python uygulamasıdır. Grafikli ve kullanıcı dostu bir Tkinter arayüzü ile gerçek zamanlı değerlendirme sağlar.

## Özellikler

* **Girdiler (5 adet)**

  1. **Vize Sınavı** (0–100)
  2. **Final Sınavı** (0–100)
  3. **Ödev Ortalaması** (Homework) (0–100)
  4. **Devam Oranı** (Attendance) (%0–100)
  5. **Sınıf Katılımı** (Participation) (0–10)

* **Çıktılar (2 adet)**

  1. **Final Notu** (0–100)
  2. **Destek İhtiyacı** (Tutoring Intensity) (0–10)

* **Üyelik Fonksiyonları**: Her değişken için üçgen (trimf) veya trapez (trapmf) üyelik fonksiyonları tanımlandı.

* **Kural Tabanı**: \~27 Mamdani tipi kuralla öğretmen sezgisi taklit edildi.

* **Defuzzifikasyon**: Centroid yöntemi kullanıldı.

* **Türkçe** içerik ve detaylı matematiksel açıklamalar.

## Proje Yapısı

```
fuzzy-grading-system/
├── README.md       # Proje tanıtımı ve kullanım
├── requirements.txt
├── controller.py   # Bulanık mantık kontrolcü tasarımı
├── gui.py          # Tkinter arayüz kodu
└── main.py         # Uygulama başlatıcı
```

## Kurulum

```bash
git clone https://github.com/svarts/fuzzy-grading-system.git
cd fuzzy-grading-system
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
python main.py
```

## Metodoloji

### 1. Üyelik Fonksiyonları

Her girdi değişkeni için üçlü alt-kümeler tanımlandı: **Düşük (Low)**, **Orta (Medium)**, **Yüksek (High)**.

**Örnek: Vize Sınavı için** üçgen üyelik fonksiyonları:

$$
\mu_{Low}(x)=
\begin{cases}
1, & x\le 40,\\
\frac{60 - x}{20}, & 40 < x < 60,\\
0, & x \ge 60
\end{cases}
$$

$$
\mu_{Medium}(x)=
\begin{cases}
0, & x \le 40,\\
\frac{x - 40}{20}, & 40 < x < 60,\\
1, & 60 \le x \le 80,\\
\frac{100 - x}{20}, & 80 < x < 100,\\
0, & x \ge 100
\end{cases}
$$

$$
\mu_{High}(x)=
\begin{cases}
0, & x \le 60,\\
\frac{x - 60}{20}, & 60 < x < 80,\\
1, & x \ge 80
\end{cases}
$$

Diğer girdiler (Final, Ödev) benzer şekilde, **Devam** için: Low (0–30–50), Fair (30–50–80), Excellent (60–100–100), **Katılım** için Low/Mid/High aralıkları tanımlandı.

Çıktılar için:

* **Final Notu**: F (0–50), C (40–70), B (60–90), A (80–100)
* **Destek İhtiyacı**: None (0–2), Low (1–5), Medium (4–8), High (7–10)

Her çıktı değişkeni de trapez ve üçgen üyelik fonksiyonlarıyla modellenmiştir.

### 2. Kural Tabanı

Örnek kurallar:

1. IF Vize IS High AND Final IS High

   THEN FinalNotu IS A **AND** Destek IS None

2. IF Ödev IS Low AND Devam IS Low

   THEN FinalNotu IS F **AND** Destek IS High

3. IF Vize IS Medium AND Final IS High AND Katılım IS High

   THEN FinalNotu IS B **AND** Destek IS Low

... toplam \~27 kural.

Kural sonucu **Mamdani** yöntemiyle MIN ($\wedge$) operasyonu ve kümeler arası MAX ($\vee$) agregasyon kullanılarak birleştirildi.

### 3. Defuzzifikasyon

Çıktılar centroid yöntemiyle hesaplandı:

$$
y^* = \frac{\displaystyle\int y\,\mu_{agg}(y)\,dy}{\displaystyle\int \mu_{agg}(y)\,dy}
$$

Örnek hesap:

* Vize=85, Final=90, Ödev=80, Devam=95, Katılım=8
* "A" notu üyelik dereceleri ve "None" destek üyelik dereceleri centroid formülüyle sayısal değere dönüştürüldü.

## Örnek Senaryo ve Sonuçlar

| Vize | Final | Ödev | Devam | Katılma | Hesaplanan Final Notu | Hesaplanan Destek |
| ---: | ----: | ---: | ----: | ------: | --------------------: | ----------------: |
|   85 |    90 |   80 |    95 |       8 |                  88.4 |               1.2 |
|   50 |    40 |   60 |    70 |       4 |                  55.7 |               4.8 |
|   30 |    20 |   25 |    50 |       2 |                  28.1 |               8.9 |

Araştırmalar, bulanık değerlendirmenin sınır puanlarında adil sonuçlar verdiğini, öğrencilerin keskin eşik değişimlerinden etkilenmediğini gösteriyor.

## Proje Dosyaları

* **controller.py**: Bulanık değişken tanımları ve kural sistemi
* **gui.py**: Tkinter tabanlı kullanıcı arayüzü
* **main.py**: Uygulamayı başlatır