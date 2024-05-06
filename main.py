from driver import Bot, Fore, Style
import sys
import os

PREFIX = ""  # The national prefix without the +
TEST_NUMBER = ""  # Test number without national prefix


class Menu:
    def __init__(self):
        self.bot = None
        self.choices = {
            "1": self.test_msg,
            "2": self.send_msg,
            "3": self.send_withmedia,
            "4": self.quit,
        }

    def display(self):
        try:
            assert PREFIX != "" and "+" not in PREFIX
            print("WHATSAPP AUTOMATOR\n", Fore.YELLOW, "You have chosen this number prefix: ", PREFIX, Style.RESET_ALL)
            print("""
                  1. Send test message
                  2. Send messages
                  3. Send messages with media attached
                  4. Quit
                  """)
        except AssertionError:
            print(Fore.RED, "Please fill the PREFIX variable in main.py OR try removing the + in the PREFIX",
                  Style.RESET_ALL)
            exit()

    def settings(self, test_mode=False):
        include_names = None

        print("- Select the file to use to get the message: ")
        try:
            txt = self.load_file("txt")
        except FileNotFoundError:
            print(Fore.RED, "Cannot find any txt file to get the message!!", Style.RESET_ALL)
        except ValueError:
            print(Fore.RED, "Wrong selection!", Style.RESET_ALL)
            self.quit()

        if not test_mode:
            print("- Select the file to use to get the numbers: ")
            try:
                csv = self.load_file("csv")
            except FileNotFoundError:
                print(Fore.RED, "Cannot find any csv file to get the numbers!!", Style.RESET_ALL)
            except ValueError:
                print(Fore.RED, "Wrong selection!", Style.RESET_ALL)
                self.quit()

            while include_names != "y" and include_names != "n":
                include_names = input("- Include names in the messages? Y/N\n> ").lower()

            if include_names == "y":
                include_names = True
            else:
                include_names = False

            return [csv, txt, include_names]

        else:
            return txt

    def test_msg(self):
        include_media = None

        while include_media != "y" and include_media != "n":
            include_media = input("- Include media in the test message? Y/N\n> ").lower()

            if include_media == "y":
                self.send_withmedia(TEST_NUMBER)
            else:
                self.send_msg(TEST_NUMBER)

    def send_msg(self, test_number=False):
        if not test_number:
            print(Fore.GREEN, "SEND MESSAGES", Style.RESET_ALL)
            csv, txt, include_names = self.settings()
            print("Ready to start sending messages.")
            self.bot = Bot()
            self.bot.csv_numbers = "data/" + csv
            self.bot.message = "data/" + txt
            self.bot.options = [include_names, False]
            self.bot.login(PREFIX)
        else:
            try:
                assert TEST_NUMBER != ""
                print(Fore.GREEN, "SEND TEST MESSAGE", Style.RESET_ALL)
                txt = self.settings(test_mode=True)
                print("Sending test message.")
                self.bot = Bot()
                self.bot.csv_numbers = TEST_NUMBER
                self.bot.message = "data/" + txt
                self.bot.options = [False, False]
                self.bot.login(PREFIX)
            except AssertionError:
                print(Fore.RED, "You MUST set the TEST_NUMBER variable in main.py", Style.RESET_ALL)
                exit()

    def send_withmedia(self, test_number=False):
        if not test_number:
            print(Fore.GREEN, "SEND MESSAGES WITH MEDIA", Style.RESET_ALL)
            input(Fore.YELLOW + "Please COPY with CTRL+C the media you want to send, then press ENTER.")
            print(Style.RESET_ALL)
            csv, txt, include_names = self.settings()
            print("Ready to start sending messages.")
            self.bot = Bot()
            self.bot.csv_numbers = "data/" + csv
            self.bot.message = "data/" + txt
            self.bot.options = [include_names, True]
            self.bot.login(PREFIX)
        else:
            try:
                assert TEST_NUMBER != ""
                print(Fore.GREEN, "SEND TEST MESSAGE WITH MEDIA", Style.RESET_ALL)
                txt = self.settings(test_mode=True)
                print("Sending test message.")
                self.bot = Bot()
                self.bot.csv_numbers = TEST_NUMBER
                self.bot.message = "data/" + txt
                self.bot.options = [False, True]
                self.bot.login(PREFIX)
            except AssertionError:
                print(Fore.RED, "You MUST set the TEST_NUMBER variable in main.py", Style.RESET_ALL)
                exit()

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
