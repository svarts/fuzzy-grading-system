# Fuzzy Öğrenci Notlandırma Sistemi

Bu proje, bulanık mantık (fuzzy logic) teknikleri kullanarak öğrencilerin **Final Notu** ve **Destek (Rehberlik) İhtiyacı** düzeylerini hesaplayan bir Python uygulamasıdır. Grafiksel ve kullanıcı dostu bir arayüz sağlamak için **Dear PyGui** kütüphanesi kullanılmıştır.

## Özellikler

- **Girdiler (5 adet)**
  1. **Vize Sınavı** (0–100)
  2. **Final Sınavı** (0–100)
  3. **Ödev Ortalaması** (0–100)
  4. **Devam Oranı** (%0–100)
  5. **Sınıf Katılımı** (0–10)

- **Çıktılar (2 adet)**
  1. **Final Notu** (0–100)
  2. **Destek İhtiyacı** (0–10)

- **Üyelik Fonksiyonları**: Her değişken için üçgen (trimf) veya trapez (trapmf) üyelik fonksiyonları tanımlandı.
- **Kural Tabanı**: Yaklaşık 27 adet Mamdani tipi kural ile öğretmen sezgisi taklit edildi.
- **Defuzzifikasyon**: Centroid (ağırlıklı ortalama) yöntemi kullanıldı.
- **Arayüz**: Dear PyGui ile modern, renkli ve interaktif bileşenler.

## Teknolojiler

- Python 3.8+
- NumPy
- SciPy
- scikit-fuzzy
- networkx, packaging
- Dear PyGui

## Proje Yapısı

```
fuzzy-grading-system/
├── README.md         # Proje tanıtımı ve kullanım
├── requirements.txt  # Bağımlılıklar
├── controller.py     # Bulanık mantık kontrolcü tasarımı
├── gui.py            # Dear PyGui arayüz kodu
└── main.py           # Uygulamayı başlatır
```

## Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/svarts/fuzzy-grading-system.git
   cd fuzzy-grading-system
   ```
2. Sanal ortam oluşturun ve aktive edin:
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   ```
3. Gerekli paketleri yükleyin:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Çalıştırma

```bash
python main.py
```

Uygulama, **Dear PyGui** penceresinde beş adet slider ile girdileri ve iki adet metin ile çıktı değerlerini gerçek zamanlı olarak gösterir.

## Metodoloji

### 1. Üyelik Fonksiyonları
Her girdi değişkeni için aşağıdaki alt-kümeler tanımlandı: **Düşük**, **Orta**, **Yüksek**.

**Örnek: Vize Sınavı** için üçgen üyelik fonksiyonları:

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

Diğer girdiler (Final, Ödev Ortalaması) benzer şekilde; **Devam Oranı** için Low (0–30–50), Fair (30–50–80), Excellent (60–100–100); **Katılım** için Low/Mid/High aralıkları tanımlandı.

### 2. Kural Tabanı

Örnek kurallar:
1. IF Vize IS High AND Final IS High
   THEN FinalNotu IS A **AND** Destek IS None
2. IF Ödev IS Low AND Devam IS Low
   THEN FinalNotu IS F **AND** Destek IS High
3. IF Vize IS Medium AND Final IS High AND Katılım IS High
   THEN FinalNotu IS B **AND** Destek IS Low

Tüm kurallar **Mamdani** yöntemiyle MIN (\(\wedge\)) ve MAX (\(\vee\)) işlemleriyle birleştirildi.

### 3. Defuzzifikasyon

Çıktılar centroid metodu ile hesaplandı:

$$
y^* = \frac{\int y\,\mu_{agg}(y)\,dy}{\int \mu_{agg}(y)\,dy}
$$

Örnek hesap:
- Vize=85, Final=90, Ödev=80, Devam=95, Katılım=8
- "A" notu ve "None" destek üyelik dereceleri centroid formülü ile sayısal değerler olarak elde edildi.

## Örnek Senaryo

| Vize | Final | Ödev | Devam | Katılım | Final Notu | Destek |
|-----:|------:|-----:|------:|--------:|-----------:|-------:|
|   85 |    90 |   80 |    95 |       8 |       88.4 |    1.2 |
|   50 |    40 |   60 |    70 |       4 |       55.7 |    4.8 |
|   30 |    20 |   25 |    50 |       2 |       28.1 |    8.9 |