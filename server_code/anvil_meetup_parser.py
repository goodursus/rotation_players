import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

# Инициализируем Anvil server
anvil.server.connect("server_B4ZFEUG46HMHBL3JVD4YFEC5-HW6VNODCLGIW6CVK")

# Глобальные переменные для хранения данных авторизации
meetup_credentials = {}

@anvil.server.callable
def save_credentials(email, password):
  """Сохраняет учетные данные пользователя"""
  global meetup_credentials
  meetup_credentials = {
    "email": email,
    "password": password
  }
  return True

@anvil.server.callable
def get_credentials():
  """Возвращает сохраненные учетные данные"""
  return meetup_credentials

def setup_driver():
  """Настройка Selenium WebDriver"""
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service, options=chrome_options)
  return driver

def login_meetup(driver, email, password):
  """Автоматический вход в аккаунт Meetup"""
  try:
    driver.get("https://www.meetup.com/login/")

    # Ожидаем загрузки формы входа
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.NAME, "email"))
    )

    # Вводим email и пароль
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)

    # Нажимаем кнопку входа
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Ожидаем успешного входа
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='user-menu']"))
    )
    return True
  except Exception as e:
    print(f"Ошибка при входе: {str(e)}")
    return False

def parse_attendees(driver, event_url):
  """Парсинг списка участников"""
  try:
    driver.get(event_url)

    # Ожидаем загрузки страницы
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "div.w-full.items-center.rounded-2xl"))
    )

    # Прокрутка страницы для загрузки всех элементов
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(2)
      new_height = driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
        break
      last_height = new_height

      # Ищем карточки участников
    attendees = []

    # Ищем карточку с вашими данными
    my_profile = driver.find_element(By.CSS_SELECTOR, "button[aria-label='tooltip']")
    my_name = my_profile.text
    my_profile_url = my_profile.get_attribute("href")
    attendees.append({
      "position": 1,
      "name": my_name,
      "profile_url": my_profile_url
    })

    # Ищем остальные карточки
    attendee_cards = driver.find_elements(By.CSS_SELECTOR, "div.w-full.items-center.rounded-2xl:not(:has(button[aria-label='tooltip']))")
    for i, card in enumerate(attendee_cards, start=2):
      try:
        name_element = card.find_element(By.CSS_SELECTOR, "h3")
        name = name_element.text
        profile_url = name_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        attendees.append({
          "position": i,
          "name": name,
          "profile_url": profile_url
        })
      except Exception as e:
        print(f"Ошибка при обработке карточки {i}: {str(e)}")
        continue

    return attendees
  except Exception as e:
    print(f"Ошибка при парсинге: {str(e)}")
    return []
  finally:
    driver.quit()

@anvil.server.callable
def parse_meetup_event(event_url):
  """Основная функция для парсинга события Meetup"""
  credentials = get_credentials()
  if not credentials:
    raise Exception("Сначала сохраните учетные данные Meetup")

  driver = setup_driver()
  if not login_meetup(driver, credentials["email"], credentials["password"]):
    raise Exception("Не удалось войти в аккаунт Meetup")

  attendees = parse_attendees(driver, event_url)
  return attendees

# Запуск сервера Anvil
anvil.server.wait_forever()

