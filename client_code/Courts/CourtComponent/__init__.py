from ._anvil_designer import CourtComponentTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
#import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
#from .ListPlayers import ListPlayers
import random
from datetime import timedelta


class CourtComponent(CourtComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Поиск не полного корта для отдыха
    #    self.not_full_court = self.find_rest_courty()
    #    self.mark_rest_court()

    # Запрос данных из таблицы
    rows = list(app_tables.courts.search())
    self.repeating_panel = self.repeating_panel_2
#    try:

  # Загрузка данных из таблицы соответствия
    correspondence_table = app_tables.s_players.search()
    # Создание словаря соответствия
    self.name_to_code = {
      row["name"]: row["player_number"] for row in correspondence_table
    }

  # Проверка, пуста ли таблица
    if not rows:
      # Если таблица пустая, создаем одну пустую запись
      empty_record = self.empty_court()
      #      self.add_court(empty_record)
      anvil.server.call("add_court", empty_record)
    else:
      last_record = app_tables.courts.search(
        tables.order_by("game_id", ascending=False)
      )
      self.last_game = last_record[0]["game_id"]
      self.current_game_box.text = self.last_game
      # Поиск не полного корта для отдыха
      self.not_full_court = self.find_rest_courty()
      self.mark_rest_court()

    # Полный список всех имен
    self.all_names = [row["name"] for row in app_tables.s_players.search()]

    self.repeating_panel_2.items = anvil.server.call("get_records_with_names")

    self.repeating_panel.set_event_handler("x-add-court", self.add_court)
    self.repeating_panel.set_event_handler("x-save-court", self.save_court)
    self.repeating_panel.set_event_handler("x-del-court", self.del_court)

    # Передача all_names в каждую карточку
    card_components = self.repeating_panel.get_components()
    for card in card_components:
      card.set_all_names(self.all_names)  # Передаем список имен через метод

    # Инициализация переменных
    self.total_time = timedelta(
      minutes=1
    )  # Общий временной интервал (например, 5 минут)
    self.elapsed_time = timedelta(seconds=0)  # Прошедшее время
    self.timer_running = False  # Флаг состояния таймера

    # Настройка таймера
    self.timer_component.interval = 1  # Интервал обновления в секундах
    self.timer_component.enabled = False  # Таймер изначально выключен

    # Привязка обработчика к событию 'tick'
#    self.timer_component.set_event_handler("tick", self.timer_tick)

    # Установка обработчиков событий
    self.button_start.set_event_handler("click", self.start_timer)
    self.button_stop.set_event_handler("click", self.stop_timer)

    # Начальные значения меток
    self.label_elapsed_time.text = "00:00:00"
    self.label_remaining_time.text = f"{str(self.total_time)}"
#    except Exception as e:
#      print("Пропущено в режиме дизайна или при ошибке доступа к таблице:", e)

  def edit_player_click(self, **event_args):
    #    open_form(ListPlayers())
    ListPlayers()

  def link_players_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("RotationPlayers.ListPlayers")

  def link_session_click(self, **event_args):
    open_form("Session")

  def link_s_players_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Session.SessionPlayers")

  def add_court(self, item, **event_args):
    rows = list(app_tables.courts.search())
    # Проверка, пуста ли таблица
    if rows:
      item = self.empty_court()
      last_court = app_tables.courts.search(tables.order_by("id", ascending=False))
      last_id = last_court[0]["id"]
      item["id"] = last_id + 1

      # refresh the Data Grid
      anvil.server.call("add_court", item)
      self.repeating_panel.items = anvil.server.call("get_records_with_names")
      self.set_list_name()
    else:
      anvil.server.call("add_zero_court", item)

  def del_court(self, court, **event_args):
    # Получение уникального идентификатора из словаря
    row_id = court["id"]
    # Поиск строки в таблице
    row_to_delete = app_tables.courts.get(id=row_id)
    row_to_delete.delete()
    self.repeating_panel.items = anvil.server.call("get_records_with_names")
    self.set_list_name()

  def save_court(self, court, **event_args):
    """Сохранение данных о кортах в таблицу."""
    for card_index, card in enumerate(self.repeating_panel.items):
      court_id = card["id"]
      players = {
        "player_id_1": self.name_to_code[card["name_1"]],
        "player_id_2": self.name_to_code[card["name_2"]],
        "player_id_3": self.name_to_code[card["name_3"]],
        "player_id_4": self.name_to_code[card["name_4"]],
        "status_1": int(card["score_1"]),
        "status_2": int(card["score_1"]),
        "status_3": int(card["score_3"]),
        "status_4": int(card["score_3"]),
      }
      # Обновление записи в таблице court
      court_row = app_tables.courts.get(id=court_id)
      if court_row:
        court_row.update(**players)

  def get_color_status(self, value):
    color_map = {1: "#d4edda", -1: "#cce5ff", 0: "#fff3cd"}  # Цвет фона
    return color_map.get(value, "#ffffff")

  def empty_court(self):
    records = {
      #        "name_1": "Неизвестно",
      "player_id_1": 0,
      #        "name_2": "Неизвестно",
      "player_id_2": 0,
      #        "name_3": "Неизвестно",
      "player_id_3": 0,
      #        "name_4": "Неизвестно",
      "player_id_4": 0,
      "id": 1,  # Дополнительные текстовые поля
      "game_id": 1,
      #        "bg_color_1": self.get_color_status(-1),
      "status_1": -1,
      #        "bg_color_2": self.get_color_status(-1),
      "status_2": -1,
      #        "bg_color_3": self.get_color_status(-1),
      "status_3": -1,
      #        "bg_color_4": self.get_color_status(-1),
      "status_4": -1,
    }
    return records

  def set_list_name(self):
    # Передача all_names в каждую карточку
    card_components = self.repeating_panel.get_components()
    for card in card_components:
      card.set_all_names(self.all_names)  # Передаем список имен через метод

  def lottery_click(self, **event_args):
    # Запрос подтверждения у пользователя
    user_response = confirm(
      "Are you sure you want to delete all court records",
      title="Confirm Delete",
      buttons=["Yes", "No"],
    )
    if user_response == "Yes":
      # Поиск всех строк в таблице
      rows = app_tables.courts.search()
      # Удаление каждой строки
      for row in rows:
        row.delete()

      last_record = app_tables.session.search(
        tables.order_by("session_id", ascending=False)
      )
      last_session = last_record[0]["session_id"]
      current_session = app_tables.session.get(session_id=last_session)
      session = dict(current_session)
      for i in range(session["number_courts"]):
        item = self.empty_court()
        item["id"] = i + 1
        anvil.server.call("add_court", item)

      rows = app_tables.s_players.search()
      names = [row["name"] for row in rows]
      random.shuffle(names)
      shuffled_names = names
      player_count = len(shuffled_names)
      courts_count = (player_count + 3) // 4
      cards_data = [shuffled_names[i * 4 : (i + 1) * 4] for i in range(courts_count)]

      # Обновление полей name_1, name_2, name_3, name_4 в существующем списке
      self.update_repeating_panel_items(cards_data)

      # Передача данных в каждую карточку
      card_components = self.repeating_panel.get_components()
      for card in card_components:
        card.set_all_names(names)  # Передаем полный список имен

  def update_repeating_panel_items(self, cards_data):
    current_items = self.repeating_panel.items
    for i, card in enumerate(cards_data):
      # Получаем текущий элемент items
      item = current_items[i]

      # Обновляем только поля name_1, name_2, name_3, name_4
      item["name_1"] = card[0] if len(card) > 0 else None
      item["name_2"] = card[1] if len(card) > 1 else None
      item["name_3"] = card[2] if len(card) > 2 else None
      item["name_4"] = card[3] if len(card) > 3 else None

      if len(card) < 4:
        self.not_full_court = i

    #     all_player_ids = []
    for card_index, card in enumerate(self.repeating_panel.items):
      court_id = card["id"]
      player_ids = {}
      for i in range(1, 5):
        key = "player_id_" + str(i)
        if card["name_" + str(i)] is not None:
          value = self.name_to_code[card["name_" + str(i)]]
          player_ids[key] = value

      #        players = {
      #            'player_id_1': self.name_to_code[card['name_1']] if card['name_1'] is not None,
      #            'player_id_2': self.name_to_code[card['name_2']],
      #            'player_id_3': self.name_to_code[card['name_3']],
      #            'player_id_4': self.name_to_code[card['name_4']],
      #        }
      # Обновление записи в таблице court
      court_row = app_tables.courts.get(id=court_id)
      if court_row:
        court_row.update(**player_ids)

    self.repeating_panel.items = anvil.server.call("get_records_with_names")

    self.mark_rest_court()

  def mark_rest_court(self):
    # Обновляем выпадающие списки вручную
    card_components = self.repeating_panel_2.get_components()
    for i, card in enumerate(card_components):
      if self.not_full_court == i:
        card.outlined_card_3.background = "#FFCCCC"

    self.repeating_panel_2.raise_event("x-refresh")

  ##############################################################
  # Timer
  def start_timer(self, **event_args):
    """Запуск таймера."""
    if not self.timer_running:
      self.timer_running = True
      self.timer_component.enabled = True  # Включение таймера

  def button_reset_click(self, **event_args):
    """Сброс таймера."""
    self.elapsed_time = timedelta(seconds=0)
    self.label_elapsed_time.text = "00:00:00"
    self.label_remaining_time.text = f"{str(self.total_time)}"

  def stop_timer(self, **event_args):
    """Остановка таймера."""
    if self.timer_running:
      self.timer_running = False
      self.timer_component.enabled = False  # Выключение таймера

  def timer_tick(self, **event_args):
    """Обработчик события таймера (вызывается каждую секунду)."""
    if self.timer_running and self.elapsed_time < self.total_time:
      # Увеличиваем прошедшее время на 1 секунду
      self.elapsed_time += timedelta(seconds=1)

      # Обновляем метки
      self.label_elapsed_time.text = f"{str(self.elapsed_time)}"
      remaining_time = self.total_time - self.elapsed_time
      self.label_remaining_time.text = f"{str(remaining_time)}"

      # Если время истекло, останавливаем таймер
      if self.elapsed_time >= self.total_time:
        self.stop_timer()
        self.label_remaining_time.text = "Finished!"
    else:
      self.stop_timer()

  def find_rest_courty(self):
    """Поиск записей, где хотя бы одно из полей name_1, name_2, name_3, name_4 равно None."""
    # Получаем все записи из таблицы
    rows = app_tables.courts.search(game_id=1)

    # Фильтруем записи, где хотя бы одно из полей равно None
    null_records = [
      row
      for row in rows
      if row["player_id_1"] == 0
      or row["player_id_2"] == 0
      or row["player_id_3"] == 0
      or row["player_id_4"] == 0
    ]
    if len(null_records) > 0:
      for record in null_records:
        null_record = record["id"]
    else:
      null_record = 0

    return null_record

