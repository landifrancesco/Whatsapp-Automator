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
timeout = 120


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
        # Selector may change in time
        self.__main_selector = "//p[@dir='ltr']"
        self.__fallback_selector = "//div[@class='x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf']//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']"
        self.__media_selector = "//div[@class='x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x1lkfr7t']//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']"

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
        Prompts the user every few seconds to scan the QR code if not already logged in.
        """
        self.__prefix = prefix
        logged_in = False  # Track login status
        page_load = False  # Track page load status

        while not logged_in:  # Loop only until login is successful
            try:
                if not page_load:
                    self.driver.get('https://web.whatsapp.com')
                print("Attempting to load WhatsApp Web...")

                # Wait for the clickable element, success_message and error_message are shown only once
                logged_in = self.wait_for_element_to_be_clickable(
                    "//div[@class='x1n2onr6 x14yjl9h xudhj91 x18nykt9 xww2gxu']",
                    success_message="Logged in successfully!",
                    error_message="Waiting for QR code to be scanned..."
                )

                if logged_in:
                    break  # Exit the loop on successful login

            except Exception as e:
                page_load = True
                print(f"Error during login: {e}")
                print("Retrying login...")

            # Wait before retrying to prevent an infinite loop from flooding the system
            time.sleep(5)

        # Record the start time for logs once the login is successful
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

    def send_message_to_contact(self, url, message):
        """
        Sends a message or media via WhatsApp Web by interacting with the webpage elements.
        """
        try:
            self.driver.get(url)

            # Try to click the main input box, if it fails, try the fallback
            try:
                message_box = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, self.__main_selector))
                )

            except:
                message_box = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, self.__fallback_selector))
                )

            # If media is included proceed differently
            if self._options[1]:
                message_box.send_keys(Keys.CONTROL, 'v')
                sleep(random.uniform(2, 5))  # Allow time for media to paste
                message_box = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, self.__media_selector))
                )

            # Type and send the message
            self.type_message(message_box, message)

            # Click the send button
            self.click_button("span[data-icon='send']")

            sleep(random.uniform(2, 5))  # Delay before moving on
            print(Fore.GREEN + "Message and media (if any) sent successfully." + Style.RESET_ALL)
            return False  # No error

        except Exception as e:
            print(e)
            print(Fore.RED + "Error sending message and media." + Style.RESET_ALL)
            return True  # Error occurred


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

    def wait_for_element_to_be_clickable(self, xpath, success_message=None, error_message=None, timeout=timeout):
        """
        Waits for an element to be clickable within the specified timeout period.
        :param xpath: The XPATH of the element to wait for.
        :param success_message: Message to display when the element becomes clickable.
        :param error_message: Message to display in case of timeout.
        :param timeout: Time (in seconds) to wait for the element to become clickable.
        :return: True if the element becomes clickable, False otherwise.
        """
        try:
            # Wait for the element to become clickable
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            if success_message:
                print(Fore.GREEN + success_message + Style.RESET_ALL)
            return True  # Element is clickable, return True

        except TimeoutException:
            if error_message:
                print(Fore.RED + error_message + Style.RESET_ALL)
            return False  # Timeout occurred, return False

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
