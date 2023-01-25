# Whatsapp Automator

A bot that automates sending messages in bulk via Whatsapp Web. <br>
You can:
- Send messages in bulk
- Send messages in bulk with media attached
- Send a test message to a number of you choice (TEST_NUMBER variable must be set in main.py)

The script saves a log file of the correctly and not correctly sent messages. The name syntax is DD-MM-YYYY_HMS.

**TESTED ON WINDOWS and LINUX**

## How-to

The numbers' and message files **must** be in the _data directory_
<br>

### 1) Requirements

```bash
pip3 install -r requirements.txt
```

YOU MUST SET **PREFIX** and **TEST_NUMBER** variables.

Example:
> PREFIX = "+39" # The national prefix
> TEST_NUMBER = "3333333333" # Test number without national prefix

### 2) Phone numbers file

It must be a **.csv** file with this syntax:

> NAME1, NUMBER1 <br>
> NAME2, NUMBER2 <br>
> etc.

N.B. If you don't have any names, please **leave the first column empty**.

### 3) Message file

It must be a **.txt** file. <br>
If you'd like to include the names of the people, you must write **%NAME%** in the message file then the script will automatically overwrite it.

### 4) Execution

```bash
python3 main.py
```

## To-Do

- [ ] IMPLEMENT EMOJI PASTING
- [ ] Clean code and add useful comments
- [ ] Check for most of the exceptions that could occur
- [X] Test the script on Windows and Mac OS

## Donate

If you like this script, please donate.

Send MATIC, BEP20, ERC20, BTC, BCH, CRO, LTC, DASH, CELO, ZEC, XRP to:
**landifrancesco.wallet**

#### My profile on Unstoppable Domains:
https://ud.me/landifrancesco.wallet

## Disclaimer

This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by WhatsApp or any of its affiliates or subsidiaries. This is an independent and unofficial software. Use at your own risk. Commercial use of this code/repo is strictly prohibited.