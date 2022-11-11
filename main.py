from driver import Bot, Fore, Style
import sys
import os

TEST_NUMBER = ""


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
        print("""
              Whatsapp Automator: 

              1. Send test message
              2. Send messages
              3. Send messages with media attached
              4. Quit
              """)

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
        try:
            assert TEST_NUMBER != ""
            print(Fore.GREEN, "SEND TEST MESSAGE", Style.RESET_ALL)
            txt = self.settings(test_mode=True)
            print("Sending test message.")
            self.bot = Bot()
            self.bot.csv_numbers = TEST_NUMBER
            self.bot.message = "data/" + txt
            self.bot.options = [False, False]
            self.bot.login()
        except AssertionError:
            print(Fore.RED, "You MUST set the TEST_NUMBER variable in main.py", Style.RESET_ALL)

    def send_msg(self):
        print(Fore.GREEN, "SEND MESSAGES", Style.RESET_ALL)
        csv, txt, include_names = self.settings()
        print("Ready to start sending messages.")
        self.bot = Bot()
        self.bot.csv_numbers = "data/" + csv
        self.bot.message = "data/" + txt
        self.bot.options = [include_names, False]
        self.bot.login()

    def send_withmedia(self):
        print(Fore.GREEN, "SEND MESSAGES WITH MEDIA", Style.RESET_ALL)
        input(Fore.YELLOW + "Please COPY with CTRL+C the media you want to send, then press ENTER.")
        print(Style.RESET_ALL)
        csv, txt, include_names = self.settings()
        print("Ready to start sending messages.")
        self.bot = Bot()
        self.bot.csv_numbers = "data/" + csv
        self.bot.message = "data/" + txt
        self.bot.options = [include_names, True]
        self.bot.login()

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
        print("Send BTC, ETH, BNB, LTC, MATIC to:")
        print(Fore.GREEN, "landifrancesco.wallet")
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
