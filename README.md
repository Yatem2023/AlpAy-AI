# 🤖 AlpAy AI

Bu proje, Python ile geliştirilmiş **basit ama geliştirilebilir bir yapay zekâ (AI) sohbet sistemidir**.  
Kullanıcıdan gelen mesajlara göre cevap üretir, yeni soru–cevapları öğrenebilir ve zamanla kendini geliştirebilir.

> 🎯 Amaç: AI mantığını sıfırdan anlamak, ML/kurallı sistem temellerini öğrenmek ve kişisel bir asistan altyapısı kurmak.

---

## 🚀 Özellikler

- 💬 Sohbet edebilme  
- 🧠 Öğrenilen verileri kaydetme  
- 📂 JSON tabanlı veri yapısı  
- 🔁 Sonradan yeniden eğitilebilir yapı  
- ⚙️ Kurallı cevap + veri tabanlı cevap sistemi  
- 🧩 Modüler dosya yapısı  
- 🐍 Saf Python (ekstra framework yok)

---

## 🗂️ Proje Yapısı

```
AlpAy-AI/
├── Kodlar/
│   ├── main.py
│   ├── intent_model.py
│   ├── actions.py
│   ├── learner.py
│   ├── memory.py
│   ├── knowledge.py
│   ├── rules.json
│   ├── learned_commands.json
│   └── memory.json
├── web site/
│   └── index.html
└── README.md
```

---

## 🛠️ Kurulum

```bash
git clone https://github.com/kullanici-adi/AlpAy-AI.git
cd AlpAy-AI
cd AlpAy-AI/Kodlar
pip install -r requirements.txt
python main.py
```

---

## ▶️ Çalıştırma

Başarılıysa:
```
🤖 AlpAy AI hazır.
```

---

## 🧠 Nasıl Çalışır?


- Kuralları kontrol eder (`Kodlar/rules.json`)
- Öğrenilmiş veriye ve kullanıcı hafızasına bakar (`Kodlar/learned_commands.json`, `Kodlar/memory.json`)
- Bilmediğini kullanıcıdan öğrenir
- Bir dahaki sefere hatırlar 🎉

---

## ⚠️ Notlar

- Eğitim amaçlıdır  
- Gerçek bir LLM değildir  
- Geliştirmeye açıktır  

---

## 👤 Geliştiriciler

**Yağız Alp Taykaya**  **Abdullah Bildirici**
AI • Arduino • IoT

---

⭐ Projeyi beğendiysen yıldızlamayı unutma


## 🌐 Web Arayüz + Backend

```bash
# 1) Backend
python Kodlar/backend.py

# 2) Frontend (ayrı terminal)
cd "web site"
python -m http.server 4173
```

Sonra tarayıcıdan `http://127.0.0.1:4173` adresine git.


## 💾 Otomatik Kaydet (Auto Commit)

Repodaki değişiklikleri otomatik commit almak için:

```bash
python autosave_repo.py --interval 60
```

Tek seferlik kontrol/commit için:

```bash
python autosave_repo.py --once
```