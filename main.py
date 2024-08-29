from driver import Bot, Fore, Style
import sys
import os

PREFIX = ""  # The national prefix without the +


class Menu:
    def __init__(self):
        self.bot = None
        self.choices = {
            "1": self.send_message,
            "2": self.send_with_media,
            "3": self.quit,
        }

    def display(self):
        try:
            assert PREFIX != "" and "+" not in PREFIX
            print("WHATSAPP AUTOMATOR")
            print(Fore.YELLOW + f"You have chosen this number prefix: {PREFIX}" + Style.RESET_ALL)
            print("""
                1. Send messages
                2. Send messages with media attached
                3. Quit
            """)
        except AssertionError:
            print(Fore.RED + "Please fill the PREFIX variable in main.py OR remove the + in the PREFIX." + Style.RESET_ALL)
            sys.exit(1)

    def settings(self):
        print("- Select the file to use for the message:")
        txt = self.load_file("txt")

        print("- Select the file to use for the numbers:")
        csv = self.load_file("csv")

        include_names = None
        while include_names not in ["y", "n"]:
            include_names = input("- Include names in the messages? Y/N\n> ").lower()

        include_names = True if include_names == "y" else False

        return csv, txt, include_names

    def send_message(self):
        print(Fore.GREEN + "SEND MESSAGES" + Style.RESET_ALL)
        csv, txt, include_names = self.settings()
        print("Ready to start sending messages.")
        self.bot = Bot()
        self.bot.csv_numbers = os.path.join("data", csv)
        self.bot.message = os.path.join("data", txt)
        self.bot.options = [include_names, False]
        self.bot.login(PREFIX)

    def send_with_media(self):
        print(Fore.GREEN + "SEND MESSAGES WITH MEDIA" + Style.RESET_ALL)
        input(Fore.YELLOW + "Please COPY the media you want to send with CTRL+C, then press ENTER." + Style.RESET_ALL)
        csv, txt, include_names = self.settings()
        print("Ready to start sending messages with media.")
        self.bot = Bot()
        self.bot.csv_numbers = os.path.join("data", csv)
        self.bot.message = os.path.join("data", txt)
        self.bot.options = [include_names, True]
        self.bot.login(PREFIX)

    def load_file(self, filetype):
        selection = 0
        idx = 1
        files = {}

        for file in os.listdir("data"):
            if file.endswith("." + filetype):
                files[idx] = file
                print(idx, ") ", file)
                idx += 1

        if len(files) == 0:
            raise FileNotFoundError

        while selection not in files.keys():
            selection = int(input("> "))

        return str(files[selection])

    def quit(self):
        print("If you like this script, please donate.")
        print("Send MATIC, BEP20, ERC20, BTC, BCH, CRO, LTC, DASH, CELO, ZEC, XRP to:")
        print(Fore.GREEN, "landifrancesco.wallet", Style.RESET_ALL)
        sys.exit(0)

    def run(self):
        while True:
            self.display()
            choice = input("Enter an option: ")
            action = self.choices[choice]
            if action:
                action()
                self.quit()
            else:
                print(Fore.RED, choice, " is not a valide choice")
                print(Style.RESET_ALL)


m = Menu()
m.run()
