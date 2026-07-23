<div align="center">

# 📱 TikTok Account Creator

**Create TikTok accounts automatically using mobile endpoints (android)**

[![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)](#)
[![RapidAPI](https://img.shields.io/badge/RapidAPI-0052CC?style=for-the-badge&logo=rapid&logoColor=white)](https://rapidapi.com/labouakileed122/api/tiktok-signer-working)
[![GPL-3.0](https://img.shields.io/badge/GPL--3.0-blue?style=for-the-badge&logo=gnu&logoColor=white)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Aznannnnls1903l)

💬 **[Questions or issues? Contact me on Telegram](https://t.me/Aznannnnls1903l)**

---

### 🌟 Support the project

**If this project helped you, please consider [starring the repository](../../stargazers).**  
*Your support means a lot, thank you! ❤️*

---

</div>

## 🚀 Setup

#### 1. **Install requirements**
```bash
pip install requests python-dotenv
```

#### 2. **Get your API key**
* Grab a free key on RapidAPI: [TikTok Signer API](https://rapidapi.com/labouakileed122/api/tiktok-signer-working)

> [!TIP]
> *The key is required to sign requests, free tier will allow you to create ~10 accounts, then you'll have to pay. I have to make money somehow yk*

#### 3. **Configure environment**
Create a `.env` file in the folder root:
```env
RAPIDAPI_KEY=your_rapidapi_key_here
```

#### 4. **Run the script**
```bash
python main.py
```

<br/>

## 🔮 How it works

1. **Device Registration**: Generates device IDs, encrypts payload via RapidAPI, and registers the device.
2. **Age Verification**: Sets a randomized valid birthdate.
3. **Send Code**: Sends a verification code to your email.
4. **Verify & Register**: Verifies the code, sets a generated password, and saves account + session details.

> Created accounts will be stored as JSON inside the `./accounts` directory.

<br/>

## 💬 Contact & Support

* **Telegram**: [@Aznannnnls1903l](https://t.me/Aznannnnls1903l)
* **GitHub**: [labounq](https://github.com/labounq)

<br/>

## ⚠️ Disclaimer

This tool is provided for educational and research purposes only. Please respect TikTok's Terms of Service (TOS). Do not use this repository or API for spamming, malicious activities, or anything harmful. The author is not responsible for any misuse or account bans resulting from the use of this script.
