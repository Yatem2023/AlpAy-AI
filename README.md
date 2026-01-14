# 🤖 AlpAy AI

**AlpAy AI**, Python ile geliştirilmiş, kullanıcıyla etkileşime girerek yeni bilgiler öğrenebilen ve bu bilgileri hafızasında tutabilen modüler bir yapay zeka asistanı prototipidir.

> 🎯 **Amaç:** Yapay zekanın temel mantığını anlamak, kural tabanlı sistemler ile veri tabanlı öğrenme süreçlerini birleştirmek.

---

## 🚀 Özellikler

- 💬 **Dinamik Sohbet:** Kullanıcı mesajlarına anlık yanıtlar.
- 🧠 **Öğrenme Kabiliyeti:** Bilmediği soruları kullanıcıdan öğrenir ve hafızasına ekler.
- 💾 **Kalıcı Hafıza:** Öğrenilen bilgiler JSON formatında güvenli bir şekilde saklanır.
- ⚙️ **Hibrit Sistem:** Sabit kurallar (`rules.py`) ve esnek veri yapısının (`ml_data.json`) birleşimi.
- 🐍 **Saf Python:** Herhangi bir ağır kütüphane bağımlılığı olmadan hafif çalışma.

---

## 🗂️ Proje Yapısı

```text
AlpAy-AI/
│
├── main.py           # Uygulamanın giriş noktası
├── ai_engine.py      # Mantık ve karar mekanizması
├── trainer.py        # Veri işleme ve öğrenme modülü
├── rules.py          # Önceden tanımlanmış kurallar
├── data/
│   └── ml_data.json  # Yapay zekanın öğrenmiş olduğu veriler
│
├── requirements.txt  # Gerekli bağımlılıklar
└── README.md         # Proje dökümantasyonu
🛠️ Kurulum ve Çalıştırma
1. Projeyi İndirin
Bash

git clone [https://github.com/kullanici-adi/AlpAy-AI.git](https://github.com/kullanici-adi/AlpAy-AI.git)
cd AlpAy-AI
2. Bağımlılıkları Yükleyin
Bash

pip install -r requirements.txt
3. Uygulamayı Başlatın
Bash

python main.py
🧠 AlpAy AI Nasıl Çalışır?
Sorgu: Kullanıcı bir mesaj yazar.

Kural Kontrolü: Önce rules.py içindeki sabit komutlar taranır.

Veri Kontrolü: Kural bulunamazsa ml_data.json içindeki kayıtlı bilgiler taranır.

Öğrenme Modu: Yanıt bulunamazsa, AlpAy AI kullanıcıya "Bunu bilmiyorum, nasıl cevap vermeliyim?" diye sorar.

Kayıt: Kullanıcının verdiği cevap hafızaya alınır ve bir sonraki seferde otomatik kullanılır. 🎉

⚠️ Önemli Not
Bu proje eğitim ve prototipleme amaçlıdır. Karmaşık bir Dil Modeli (LLM) değil, temel AI mantığını kavramaya yönelik bir mantıksal asistan altyapısıdır.

👤 Geliştirici
Yağız Alp Taykaya Yazılım & Abdullah Bildirici

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
