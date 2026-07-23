# TikTok Account Creator (Standalone)

Script to create TikTok accounts automatically using mobile endpoints (android) 

## ⚡ Setup

1. **Install requirements**
   ```bash
   pip install requests python-dotenv
   ```

2. **Get your API key**
   - Grab a free key on RapidAPI: [TikTok Signer API](https://rapidapi.com/labouakileed122/api/tiktok-signer-working)
   - *required to sign requests, free tier will allow you to create ~10 accounts, then you'll have to pay. I have to make money somehow yk*

3. **Configure environment**
   Create a `.env` file in the folder root:
   ```env
   RAPIDAPI_KEY=your_rapidapi_key_here
   ```

4. **Run the script**
   ```bash
   python main.py
   ```

## 🛠️ How it works

1. **Device Registration**: Generates device IDs, encrypts payload via RapidAPI, and registers the device.
2. **Age Verification**: Sets a randomized valid birthdate.
3. **Send Code**: Sends a verification code to your email.
4. **Verify & Register**: Verifies the code, sets a generated password, and saves account + session details.

Created accounts will be stored as JSON inside the `./accounts` directory.

## 💬 Contact & Support

- **Telegram**: [@Aznannnnls1903l](https://t.me/Aznannnnls1903l)
- **GitHub**: [labounq](https://github.com/labounq)
