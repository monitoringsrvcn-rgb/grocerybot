# 🤖 Telegram Product Bot

Bot ឆ្លើយតបស្វ័យប្រវត្តិអំពីផលិតផល និងតម្លៃ ដោយប្រើ AI Claude។

---

## 📁 រចនាសម្ព័ន្ធឯកសារ

```
telegram-product-bot/
├── bot.py            ← កូដ Bot ចម្បង
├── products.json     ← ទិន្នន័យផលិតផល (កែតាមចិត្ត)
├── requirements.txt  ← Python packages
└── README.md         ← ឯកសារនេះ
```

---

## ⚙️ ជំហានទី 1 – បង្កើត Telegram Bot

1. បើក Telegram → ស្វែងរក **@BotFather**
2. វាយ `/newbot`
3. ដាក់ឈ្មោះ Bot (ឧ. `MyShop Bot`)
4. ដាក់ username (ត្រូវបញ្ចប់ដោយ `bot` ឧ. `myshop_bot`)
5. Copy **Token** ដែលបានផ្តល់ → រក្សាទុក

---

## ⚙️ ជំហានទី 2 – យក Anthropic API Key

1. ចូល [https://console.anthropic.com](https://console.anthropic.com)
2. ចុច **API Keys** → **Create Key**
3. Copy key → រក្សាទុក

---

## 🚀 ជំហានទី 3 – Deploy លើ Railway (ដោយឥតគិតថ្លៃ)

### 3.1 Upload ឯកសារទៅ GitHub

```bash
git init
git add .
git commit -m "Initial bot"
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git
git push -u origin main
```

### 3.2 Deploy លើ Railway

1. ចូល [https://railway.app](https://railway.app) → Login ដោយ GitHub
2. ចុច **New Project** → **Deploy from GitHub repo**
3. ជ្រើស repo ដែល upload
4. ចុច **Variables** → បន្ថែម:

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | token ពី BotFather |
| `ANTHROPIC_API_KEY` | key ពី Anthropic |
| `SHOP_NAME` | ឈ្មោះហាងអ្នក |
| `CONTACT_INFO` | ព័ត៌មានទំនាក់ទំនង |

5. Railway deploy ដោយស្វ័យប្រវត្តិ ✅

---

## 🚀 Deploy លើ Render (ជម្រើសផ្សេង)

1. ចូល [https://render.com](https://render.com)
2. ចុច **New** → **Web Service**
3. Connect GitHub repo
4. កំណត់:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
5. បន្ថែម Environment Variables ដូច Railway ខាងលើ

---

## 🧪  សាកល្បង Local (Computer ផ្ទាល់)

```bash
# Install packages
pip install -r requirements.txt

# Set environment variables (Windows)
set TELEGRAM_BOT_TOKEN=your_token_here
set ANTHROPIC_API_KEY=your_key_here
set SHOP_NAME=ហាងរបស់ខ្ញុំ
set CONTACT_INFO=Tel: 012 345 678

# Run bot
python bot.py
```

---

## 📦 កែប្រែផលិតផល

កែឯកសារ `products.json`:

```json
{
  "categories": {
    "ឈ្មោះប្រភេទ": [
      {
        "name": "ឈ្មោះផលិតផល",
        "price": 99,
        "description": "ការពិពណ៌នា",
        "stock": 10
      }
    ]
  }
}
```

---

## 💬 ពាក្យបញ្ជា Bot

| Command | មុខងារ |
|---------|--------|
| `/start` | ស្វាគមន៍ |
| `/help` | ជំនួយ |
| `/products` | មើលបញ្ជីផលិតផល |
| វាយសំណួរ | AI ឆ្លើយតប |

---

## ❓ សំណួរញឹកញាប់

**Bot មិនដំណើរការ?**
→ ពិនិត្យ Token និង API Key ក្នុង Variables

**AI ឆ្លើយខុស?**
→ កែ `products.json` ឲ្យត្រឹមត្រូវ

**ចង់បន្ថែមមុខងារ?**
→ កែ `bot.py` ឬទំនាក់ទំនង developer
