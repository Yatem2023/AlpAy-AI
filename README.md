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
│
├── main.py
├── ai_engine.py
├── trainer.py
├── rules.py
├── data/
│   └── ml_data.json
│
├── requirements.txt
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
git clone https://github.com/yatem2023/AlpAy-AI.git
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

- Kuralları kontrol eder (`rules.py`)
- Öğrenilmiş veriye bakar (`ml_data.json`)
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
