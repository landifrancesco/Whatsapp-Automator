import csv
import os.path
import time
from time import sleep

from colorama import Fore, Style
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
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

        options.add_argument("start-maximized")

        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self._message = None
        self._csv_numbers = None
        self._options = [False, False]
        self._start = None
        self.__prefix = None

    def login(self, prefix):
        self.__prefix = prefix
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
                EC.element_to_be_clickable((By.XPATH, "//div[@class='_ak0w']")))
        except TimeoutException:
            print(Fore.RED, "Please login in Whatsapp Web via QR Code. That's the last warning before stopping the program!", Style.RESET_ALL)
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='_ak0w']")))
        t = time.localtime()
        self._start = str(time.strftime("%d-%m-%Y_%H%M%S", t))
        self.send_msg()

    def send_msg(self):
        if os.path.isfile(self.csv_numbers):
            with open(self.csv_numbers, mode="r") as file:
                csv_file = csv.reader(file)
                multiline = False
                
                for row in csv_file:
                    error = False
                    name = row[0]
                    number = row[1]

                    print("Sending message to: ", name, "|", number)

                    if self._options[0] and name != "":
                        message = self._message.replace("%NAME%", name)
                    else:
                        message = self._message.replace("%NAME%", "")

                    if "\n" in message:
                        words = message.split("\n")
                        multiline = True

                    try:
                        if not multiline:
                            url = 'https://web.whatsapp.com/send?phone=' + self.__prefix + number.strip() + '&text=' + message + '&type=phone_number&app_absent=0'
                        else:
                            url = 'https://web.whatsapp.com/send?phone=' + self.__prefix + number.strip() + '&text=&type=phone_number&app_absent=0'
                    except FileNotFoundError:
                        print(Fore.RED, "Error reading data, check numbers and message files.", Style.RESET_ALL)

                    sleep(1)
                    self.driver.get(url)
                    try:
                        sleep(10)
                        elements = self.driver.find_elements(By.XPATH, "//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")
                        # text_btn = WebDriverWait(self.driver, timeout).until(
                        #     EC.element_to_be_clickable((By.XPATH, "//p[@class='selectable-text copyable-text iq0m558w']")))
                        text_btn = elements[1]
                        if self.options[1]:
                            text_btn.send_keys(Keys.CONTROL + 'v')
                            sleep(3)
                            text_btn = WebDriverWait(self.driver, timeout).until(
                            EC.element_to_be_clickable((By.XPATH, "//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")))
                            image_btn = WebDriverWait(self.driver, timeout).until(
                                EC.element_to_be_clickable((By.XPATH, "//div[@class='x1n2onr6']")))
                            sleep(3)
                            if multiline:
                                for w in words:
                                    text_btn.send_keys(w)
                                    text_btn.send_keys(Keys.LEFT_SHIFT + Keys.RETURN)
                            image_btn.click()
                            text_btn.send_keys(Keys.RETURN)
                        else:
                            if multiline:
                                for w in words:
                                    text_btn.send_keys(w)
                                    text_btn.send_keys(Keys.LEFT_SHIFT + Keys.RETURN)
                            send_btn = WebDriverWait(self.driver, timeout).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            "//button[@class='x1c4vz4f x2lah0s xdl72j9 xfect85 x1iy03kw x1lfpgzf']")))
                            sleep(1)
                            send_btn.click()
                        sleep(3)
                    except Exception as e:
                        print(e)
                        error = True
                    finally:
                        if not error:
                            print(Fore.GREEN, "Message sent correctly to: ", name, "|", number)
                        else:
                            print(Fore.RED, "Error sending message to: ", name, "|", number)
                        self.log(number, error)
                        print(Style.RESET_ALL)
        else:
            error = False
            name = row[0]
            number = row[1]

            print("Sending message to: ", name, "|", number)

            if self._options[0] and name != "":
                message = self._message.replace("%NAME%", name)
            else:
                message = self._message.replace("%NAME%", "")

            if "\n" in self._message:
                words = self._message.split("\n")
                multiline = True

            try:
                if not multiline:
                    url = 'https://web.whatsapp.com/send?phone=' + self.__prefix + number.strip() + '&text=' + message
                else:
                    url = 'https://web.whatsapp.com/send?phone=' + self.__prefix + number.strip() + '&text='
            except FileNotFoundError:
                print(Fore.RED, "Error reading data, check numbers and message files.", Style.RESET_ALL)

            self.driver.get(url)
            try:
                text_btn = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//p[@class='selectable-text copyable-text iq0m558w']")))
                if self.options[1]:
                    text_btn.send_keys(Keys.CONTROL + 'v')
                    sleep(3)
                    text_btn = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='fd365im1 to2l77zo bbv8nyr4 mwp4sxku gfz4du6o ag5g9lrv']")))
                    image_btn = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@class='_33pCO']")))
                    if multiline:
                        for w in words:
                            text_btn.send_keys(w)
                            text_btn.send_keys(Keys.LEFT_SHIFT + Keys.RETURN)
                    image_btn.click()
                    text_btn.send_keys(Keys.RETURN)
                else:
                    if multiline:
                        for w in words:
                            text_btn.send_keys(w)
                            text_btn.send_keys(Keys.LEFT_SHIFT + Keys.RETURN)
                    text_btn.send_keys(Keys.RETURN)
                sleep(3)
            except Exception as e:
                print(e)
                error = True
            finally:
                if not error:
                    print(Fore.GREEN, "Message sent correctly to: ", name, "|", number)
                else:
                    print(Fore.RED, "Error sending message to: ", name, "|", number)
                self.log(number, error)
                print(Style.RESET_ALL)

    def log(self, string, error):
        assert self._start is not None
        path_sent = "logs/" + self._start + "_sent.txt"
        path_notsent = "logs/" + self._start + "_notsent.txt"

        if not os.path.exists(path_sent):
            with open(path_sent, "w") as f:
                f.write("")
        if not os.path.exists(path_notsent):
            with open(path_notsent, "w") as f:
                f.write("")

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
