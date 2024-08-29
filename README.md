
# 🚀 WhatsApp Automator

## 📖 Overview

**WhatsApp Automator** is a powerful Python tool designed to automate sending messages via WhatsApp Web. Whether you're sending text or media, this bot makes it simple and efficient to manage bulk messaging tasks while keeping things personalized.

## ✨ Features

- 📩 **Send Messages**: Automatically deliver text messages to multiple contacts from a CSV file.
- 🎥 **Send Messages with Media**: Attach images, videos, and other media to your messages.
- 🛠️ **Customizable**: Easily personalize your messages with names and other placeholders.
- 🔒 **Persistent Login**: No need to scan the QR code each time—your session is saved!

## 🛠️ Requirements

- **Python 3.x**
- **Google Chrome**
- **ChromeDriver** (automatically managed by `webdriver-manager`)

### 🧰 Install Dependencies

Make sure you have all the required Python packages by running:

```bash
pip install -r requirements.txt
```

**Packages you need**:
- `colorama`
- `selenium`
- `undetected-chromedriver`
- `webdriver-manager`

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/whatsapp-automator.git
cd whatsapp-automator
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Prepare Your Data

- **Message File**: Create a `.txt` file in the `data/` directory containing the message you want to send. Use `%NAME%` as a placeholder to personalize the message.
- **CSV File**: Prepare a `.csv` file in the `data/` directory with contact numbers and names. The CSV should have two columns: `Name` and `Number`.

**Important**: The numbers in the CSV file **should not** include the international prefix. The script will automatically prepend the prefix you set in `main.py`.

**Note**: The `message.txt` and `contacts.csv` are just example file names. The script scans for all `.txt` and `.csv` files in the `data` directory, allowing you to choose from multiple files during execution.

### 4. Set Your Country Prefix

Edit the `main.py` file and set your country’s prefix:

```bash
PREFIX = ""  # Your country prefix without the +
```

## 🚀 Running the Bot

To run the bot, simply execute:

```bash
python main.py
```

## 🎛️ Menu Options

1. **Send Messages**: Select your message and contact files, and the bot will send the messages to all contacts.
2. **Send Messages with Media**: Like the first option but with media attachments. Make sure your media is copied to the clipboard before running.
3. **Quit**: Exit the application.

### Example Files

- **Message File (`message.txt`)**:
  ```text
  Hello %NAME%,
  This is a reminder about our meeting tomorrow at 10 AM.
  ```

- **CSV File (`contacts.csv`)**:
  ```csv
  Name,Number
  John Doe,123456789
  Jane Doe,987654321
  ```

**Note**: The numbers in `contacts.csv` should **not** include the international prefix.

## ⚠️ Disclaimer

This software is an **unofficial** tool and is **not affiliated** with WhatsApp. It may potentially infringe on WhatsApp's Terms and Conditions. **Use at your own risk**.

## ❤️ Support

If this tool helps you, consider supporting by donating via MATIC, BEP20, ERC20, BTC, BCH, CRO, LTC, DASH, CELO, ZEC, XRP to `landifrancesco.wallet`.

## 📜 License

Licensed under the GPL-3.0 License.
