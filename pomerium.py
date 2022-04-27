from config import GOOGLE_USER, GOOGLE_PASSWORD, REDMINE_USER, REDMINE_PASSWORD, REDMINE_URL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def get_pomerium_cookie():
    driver = webdriver.Firefox()
    driver.get(REDMINE_URL)
    google_email_elem = driver.find_element(By.ID, 'identifierId')
    google_email_elem.send_keys(GOOGLE_USER)
    google_email_elem.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.NAME, 'password')))

    google_password_elem = driver.find_element(By.NAME, 'password')
    google_password_elem.send_keys(GOOGLE_PASSWORD)
    google_password_elem.send_keys(Keys.RETURN)

    WebDriverWait(driver, 120).until(expected_conditions.title_is('Redmine'))

    redmine_user_elem = driver.find_element(By.ID, 'username')
    redmine_user_elem.send_keys(REDMINE_USER)

    redmine_password_elem = driver.find_element(By.ID, 'password')
    redmine_password_elem.send_keys(REDMINE_PASSWORD)

    redmine_login_elem = driver.find_element(By.ID, 'login-submit')
    redmine_login_elem.click()

    WebDriverWait(driver, 120).until(expected_conditions.title_is('My page - Redmine'))
    pomerium = driver.get_cookie('_pomerium').get('value')
    driver.close()
    return pomerium

