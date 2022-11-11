import csv
import os.path
import time
from time import sleep

from colorama import Fore, Style
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

timeout = 30


class Bot:
    """
    Bot class that install Chrome driver automatically
    """

    def __init__(self):
        options = Options()
        # options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--profile-directory=Default")
        # options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self._message = None
        self._csv_numbers = None
        self._options = [False, False]
        self._start = None

    def login(self):
        try:
            self.driver.get('https://web.whatsapp.com')
        except Exception as e:
            print(e)
            print("Trying again ...")
            self.driver.get('https://web.whatsapp.com')
        self.wait()
        self.driver.close()

    def wait(self):
        print("Please login in Whatsapp Web via QR Code")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='ldL67 _2i3T7']")))
        except TimeoutException:
            self.wait()
        self.send_msg()

    def send_msg(self):
        if os.path.isfile(self.csv_numbers):
            with open(self.csv_numbers, mode="r") as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    error = False
                    name = row[0]
                    number = row[1]

                    print("Sending message to: ", name, "|", number)

                    if self._options[0] and name != "":
                        message = self._message.replace("%NAME%", name)
                    else:
                        message = self._message.replace("%NAME%", "")

                    try:
                        url = 'https://web.whatsapp.com/send?phone=+39' + number.strip() + '&text=' + message
                    except FileNotFoundError:
                        print(Fore.RED, "Error reading data, check numbers and message files.", Style.RESET_ALL)

                    self.driver.get(url)
                    try:
                        t = time.localtime()
                        self._start = str(time.strftime("%d-%m-%Y_%H%M%S", t))
                        text_btn = WebDriverWait(self.driver, timeout).until(
                            EC.element_to_be_clickable((By.XPATH, "//p[@class='selectable-text copyable-text']")))
                        if self.options[1]:
                            text_btn.send_keys(Keys.CONTROL + 'v')
                            image_btn = WebDriverWait(self.driver, timeout).until(
                                EC.element_to_be_clickable((By.XPATH, "//div[@class='_33pCO']")))
                            image_btn.click()
                        else:
                            text_btn.send_keys(Keys.RETURN)
                        sleep(3)
                    except Exception as e:
                        print(e)
                        error = True
                    finally:
                        if not error:
                            print(Fore.GREEN, "Message sent correctly to: ", name, "|", number)
                            self.log(number, error)
                        else:
                            print(Fore.RED, "Error sending message to: ", name, "|", number)
                            self.log(number, error)
                        print(Style.RESET_ALL)
        else:
            error = False
            number = str(self.csv_numbers)  # Get the test number
            message = self._message

            url = 'https://web.whatsapp.com/send?phone=' + number.strip() + '&text=' + message

            self.driver.get(url)
            try:
                text_btn = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//p[@class='selectable-text copyable-text']")))
                text_btn.send_keys(Keys.RETURN)
                sleep(3)
            except Exception as e:
                print(e)
                error = True
            finally:
                if not error:
                    print(Fore.GREEN, "Test message sent correctly to: ", number)
                else:
                    print(Fore.RED, "Error sending test message to: ", number)
                print(Style.RESET_ALL)

    def log(self, string, error):
        assert self._start is not None
        path_sent = "logs/" + self._start + "_sent.txt"
        path_notsent = "logs/" + self._start + "_notsent.txt"

        if not os.path.exists(path_sent):
            with open(path_sent, "w") as f:
                pass
        if not os.path.exists(path_notsent):
            with open(path_notsent, "w") as f:
                pass

        if not error:
            textfile = open(path_sent, "a")
        else:
            textfile = open(path_notsent, "a")
        textfile.write(string.strip())
        textfile.write("\n")
        textfile.close()

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, txt_file):
        f = open(txt_file, "r")
        self._message = f.read()
        f.close()

    @property
    def csv_numbers(self):
        return self._csv_numbers

    @csv_numbers.setter
    def csv_numbers(self, csv_file):
        self._csv_numbers = csv_file

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, opt):
        self._options = opt
