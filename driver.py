import csv
import os.path
import random
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
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager


# Define a timeout for waiting for elements to load
timeout = 30


class Bot:
    """
    Bot class that automates WhatsApp Web interactions using a Chrome driver.
    """

    def __init__(self):
        # Configure Chrome options
        options = Options()
        # Use a specific Chrome user profile to save the session
        options.add_argument("user-data-dir=./chrome-data")  # Path to where the user data will be stored

        # Initialize the undetected Chrome driver
        self.driver = Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self._message = None
        self._csv_numbers = None
        self._options = [False, False]  # [include_names, include_media]
        self._start_time = None
        self.__prefix = None

    def click_button(self, css_selector):
        """
        Clicks the send button (specified by its CSS selector).
        """
        button = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        sleep(1)
        button.click()

    def construct_whatsapp_url(self, number):
        """
        Constructs the WhatsApp Web URL for opening a chat with a contact.
        """
        return f'https://web.whatsapp.com/send?phone={self.__prefix}{number.strip()}&type=phone_number&app_absent=0'

    def login(self, prefix):
        """
        Logs in to WhatsApp Web by navigating to the login page.
        Waits indefinitely until the QR code is scanned and/or clickable element appears.
        """
        self.__prefix = prefix
        try:
            self.driver.get('https://web.whatsapp.com')
        except Exception as e:
            print(e)
            print("Retrying login...")
            self.driver.get('https://web.whatsapp.com')

        # Reusing the method to wait for the QR code scan
        self.wait_for_element_to_be_clickable(
            "//div[@class='x1n2onr6 x14yjl9h xudhj91 x18nykt9 xww2gxu']",
            success_message="Logged in successfully!",
            error_message="Please login to WhatsApp Web via QR Code."
        )

        # Record the start time for logs
        self._start_time = time.strftime("%d-%m-%Y_%H%M%S", time.localtime())
        self.send_messages_to_all_contacts()

    def log_result(self, number, error):
        """
        Logs the result of each message send attempt.
        """
        assert self._start_time is not None
        log_path = "logs/" + self._start_time + ("_notsent.txt" if error else "_sent.txt")

        with open(log_path, "a") as logfile:
            logfile.write(number.strip() + "\n")

    def paste_media(self):
        """
        Pastes selected media using CTRL+V.
        """
        message_box = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Type a message'][contenteditable='true']"))
        )
        message_box.send_keys(Keys.CONTROL, 'v')

    def prepare_message(self, name):
        """
        Prepares the message, including the recipient's name if specified.
        """
        if self._options[0] and name:
            return self._message.replace("%NAME%", name)
        return self._message.replace("%NAME%", "")

    def quit_driver(self):
        """
        Closes the WebDriver session and quits the browser.
        """
        if self.driver:
            self.driver.quit()
            print(Fore.YELLOW, "Driver closed successfully.", Style.RESET_ALL)

    def send_messages_to_all_contacts(self):
        """
        Sends messages to all contacts listed in the provided CSV file.
        Closes the driver after execution.
        """
        if not os.path.isfile(self._csv_numbers):
            print(Fore.RED, "CSV file not found!", Style.RESET_ALL)
            return

        try:
            with open(self._csv_numbers, mode="r") as file:
                csv_reader = csv.reader(file)
                multiline = "\n" in self._message

                for row in csv_reader:
                    name, number = row[0], row[1]
                    print(f"Sending message to: {name} | {number}")
                    message = self.prepare_message(name)
                    url = self.construct_whatsapp_url(number)  # Generate URL without the message

                    error = self.send_message_to_contact(url, message)
                    self.log_result(number, error)

                    # Random sleep between sending messages to avoid being detected
                    sleep(random.uniform(1, 10))
        finally:
            self.quit_driver()

    def type_message(self, text_element, message):
        """
        Types the message into the appropriate text element.
        Handles multiline messages.
        """
        multiline = "\n" in message
        if multiline:
            for line in message.split("\n"):
                text_element.send_keys(line)
                text_element.send_keys(Keys.LEFT_SHIFT + Keys.RETURN)
        else:
            text_element.send_keys(message)

    def wait_for_element_to_be_clickable(self, xpath, success_message=None, error_message=None):
        """
        Waits indefinitely for an element to be clickable.
        :param xpath: The XPATH of the element to wait for.
        :param success_message: Message to display when the element becomes clickable.
        :param error_message: Message to display in case of timeout.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            if success_message:
                print(Fore.GREEN, success_message, Style.RESET_ALL)
        except TimeoutException:
            if error_message:
                print(Fore.RED, error_message, Style.RESET_ALL)
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, txt_file):
        with open(txt_file, "r") as file:
            self._message = file.read()

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
