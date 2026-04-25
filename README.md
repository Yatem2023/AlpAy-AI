🤖 AlpAy AI
AlpAy AI, Python dilinde sıfırdan geliştirilmiş, kural tabanlı mantık ile dinamik öğrenme yeteneğini birleştiren modüler bir yapay zekâ asistanıdır. Karmaşık kütüphanelere bağımlı kalmadan, yapay zekânın temel işleyiş mantığını (veri işleme, hafıza yönetimi ve karar verme) anlamak ve geliştirmek için tasarlanmıştır.

🎯 Amaç: AI mantığını temelden kavramak, ML prensiplerini kural tabanlı sistemlerle harmanlamak ve kişisel, geliştirilebilir bir asistan altyapısı oluşturmak.

🚀 Öne Çıkan Özellikler
💬 İnteraktif Sohbet: Kullanıcı ile doğal bir akışta iletişim kurabilir.

🧠 Dinamik Öğrenme: Bilmediği bir komutu kullanıcıdan öğrenir ve learned_commands.json üzerine kaydederek bir sonraki sefer hatırlar.

📂 Kalıcı Hafıza: Kullanıcı tercihlerini ve geçmiş etkileşimleri memory.json içinde saklar.

⚙️ Hibrit Karar Mekanizması: Hem önceden tanımlanmış kuralları (rules.json) hem de sonradan öğrenilen verileri eşzamanlı kullanır.

🌐 Web Entegrasyonu: Hem terminal üzerinden hem de modern bir web arayüzü (Backend/Frontend) üzerinden kontrol edilebilir.

💾 Otomatik Senkronizasyon: Yapılan geliştirmeleri otomatik olarak Git reposuna işleyen (Auto Commit) script desteği.

🗂️ Proje Yapısı
Plaintext
AlpAy-AI/
├── Kodlar/
│   ├── main.py              # Ana giriş noktası (Terminal Modu)
│   ├── backend.py           # Web API sunucusu
│   ├── intent_model.py      # Niyet anlama ve işleme mantığı
│   ├── actions.py           # Tetiklenen fonksiyonlar ve eylemler
│   ├── learner.py           # Yeni veri öğrenme motoru
│   ├── memory.py            # Hafıza okuma/yazma yönetimi
│   ├── knowledge.py         # Bilgi tabanı yönetim modülü
│   ├── rules.json           # Statik sistem kuralları
│   ├── learned_commands.json # AI'nın sonradan öğrendiği bilgiler
│   └── memory.json          # Kullanıcıya özel saklanan veriler
├── web site/
│   └── index.html           # Kullanıcı dostu web arayüzü
├── autosave_repo.py         # Otomatik Git commit scripti
└── README.md                # Proje dökümantasyonu
🛠️ Kurulum ve Kullanım
1. Hazırlık
Önce repoyu klonlayın ve ilgili dizine gidin:

Bash
git clone https://github.com/Yatem2023/AlpAy-AI.git
cd AlpAy-AI
2. Terminal Modunda Çalıştırma
Sadece kod mantığını test etmek için:

Bash
cd Kodlar
python main.py
3. Web Arayüzü ile Çalıştırma
Web sürümünü kullanmak için iki ayrı terminal açmanız gerekir:

Terminal 1 (Backend):

Bash
python Kodlar/backend.py
Terminal 2 (Frontend):

Bash
cd "web site"
python -m http.server 4173
Tarayıcınızdan şu adrese gidin: http://127.0.0.1:4173

💾 Geliştiriciler İçin: Otomatik Kayıt (Auto Commit)
Kod yazarken değişikliklerinizi düzenli olarak GitHub'a aktarmak için autosave_repo.py scriptini kullanabilirsiniz:

Belirli aralıklarla (örneğin 60 saniyede bir) kontrol etmek için:

Bash
python autosave_repo.py --interval 60
Tek seferlik kontrol ve commit için:

Bash
python autosave_repo.py --once
🧠 Nasıl Çalışır?
Analiz: Kullanıcıdan gelen girdi önce rules.json içindeki sabit kurallarla karşılaştırılır.

Hafıza Kontrolü: Eğer kurallarda yoksa, learned_commands.json (öğrenilenler) ve memory.json (kişisel hafıza) taranır.

Öğrenme: Eğer yanıt bulunamazsa, AlpAy kullanıcıya "Bunu nasıl cevaplamalıyım?" diye sorar.

Kalıcılık: Kullanıcının verdiği cevap anında veri tabanına işlenir ve bir sonraki sefer aynı soru sorulduğunda doğrudan yanıt verilir.

👤 Geliştiriciler
Yağız Alp Taykaya

Abdullah Bildirici

Yapay Zekâ • Arduino • IoT • Yazılım Geliştirme

⚠️ Not: Bu proje eğitim amaçlıdır. Bir Büyük Dil Modeli (LLM) değildir, mantıksal kurallar ve dinamik veri eşleşmeleri üzerine kurulmuştur.

⭐ Bu projeyi beğendiysen yıldız vermeyi unutma!
