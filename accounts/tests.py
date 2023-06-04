from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from selenium.webdriver.common.by import By


class TestLogin(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        cls.selenium = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=options,
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # ログインページを開く
        # サービス名画 dev_webみたいなアンダース個だとエラー
        self.selenium.get('http://app:8000' +
                          str(reverse_lazy('account_login')))
        # ログイン
        username_input = self.selenium.find_element(By.NAME, "login")
        username_input.send_keys('sample@yahoo.com')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('11235i')
        self.selenium.find_element(By.CLASS_NAME, 'btn').click()

        # ページタイトルの検証
        self.assertEquals('日記一覧 | Private Diary', self.selenium.title)
