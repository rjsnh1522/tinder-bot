import time

from selenium import webdriver
from bot_helper_urls import *
from secrets import GMAIL_LOGIN_CRED, GMAIL_LOGIN_PASS, FB_LOGIN_CRED, FB_LOGIN_PASS, login_by


class TinderBot:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get(TINDER_URL)
        time.sleep(5)

        try:
            more_option = self.driver.find_element_by_xpath(CLICK_MORE_OPTION)
            if more_option.text != 'Trouble logging in?':
                more_option.click()
                time.sleep(4)
        except Exception as e:
            print(e)
        if login_by == 'google':
            google_btn = self.driver.find_element_by_xpath(LOGIN_BTN_X_PATH)
            google_btn.click()
        elif login_by == 'fb':
            fb_btn = self.driver.find_element_by_xpath(FB_LOGIN_X_PATH)
            fb_btn.click()
        windows = self.driver.window_handles
        base_window = windows[0]
        popup_window = windows[-1]
        self.driver.switch_to.window(popup_window)

        if login_by == 'google':
            self.login_using_g_mail()
        elif login_by == 'fb':
            self.login_facebook()

        # till here login is done
        self.driver.switch_to.window(base_window)
        self.handle_tinder_unwanted_pop()
        self.auto_swipe()

    def login_using_g_mail(self):
        gmail_input = self.driver.find_element_by_xpath(GMAIL_LOGIN_INPUT)
        gmail_input.clear()
        gmail_input.send_keys(GMAIL_LOGIN_CRED)
        next_input = self.driver.find_element_by_xpath(GMAIL_EMAIL_NEXT)
        next_input.click()
        time.sleep(3)
        pass_input = self.driver.find_element_by_xpath(GMAIL_PASS_INPUT)
        pass_input.clear()
        pass_input.send_keys(GMAIL_LOGIN_PASS)
        pass_next = self.driver.find_element_by_xpath(PASSWORD_NEXT)
        pass_next.click()
        time.sleep(3)

    def login_facebook(self):
        email_in = self.driver.find_element_by_xpath(FB_LOGIN_INPUT)
        email_in.send_keys(FB_LOGIN_CRED)

        pw_in = self.driver.find_element_by_xpath(FB_PASS_INPUT)
        pw_in.send_keys(FB_LOGIN_PASS)

        login_btn = self.driver.find_element_by_xpath(FB_LOGIN_BTN)
        login_btn.click()

    def handle_tinder_unwanted_pop(self):
        try:
            time.sleep(5)
            allow = self.driver.find_element_by_css_selector(ALLOW_PATH_CSS)
            allow.click()
            time.sleep(3)
            not_interested = self.driver.find_element_by_css_selector(NOT_INTERESTED_CSS)
            not_interested.click()
            time.sleep(3)
            no_thanks = self.driver.find_element_by_css_selector(NO_THANKS_CSS)
            no_thanks.click()
        except Exception as e:
            import ipdb; ipdb.set_trace()
            print("Error in popup resolving", e)

    def like(self):
        like_btn = self.driver.find_element_by_xpath(LINK_BTN)
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath(DISLIKE_BTN)
        dislike_btn.click()

    def open_all_images(self):
        left_right_clicker = self.driver.find_elements_by_css_selector(LEFT_RIGHT_CLICKER)
        import ipdb; ipdb.set_trace()
        left = left_right_clicker[2]
        right = left_right_clicker[3]
        all_done = False
        all_images = []
        while True:
            try:
                if not all_done:
                    current_selected = self.driver.find_element_by_css_selector(CURRENT_SEL_PROFILE)
                    all_divs = current_selected.find_elements_by_tag_name('div')
                    for div in all_divs:
                        ele = div.find_elements_by_css_selector('div div')[-1].get_attribute("style")
                        url = ele.value_of_css_property('background-image')
                        all_images.append(url)
                    left.click()
                    time.sleep(3)
                else:
                    break
            except Exception as e:
                all_done = True
                break
        print("All Images open", all_images)

    def auto_swipe(self):
        while True:
            self.open_all_images()
            time.sleep(1)
            try:
                pass
                # self.like()
            except Exception:
                try:
                    pass
                    # self.close_popup()
                except Exception:
                    pass
                    # self.close_match()

tt = TinderBot()
tt.login()
