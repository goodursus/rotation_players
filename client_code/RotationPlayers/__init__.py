from ._anvil_designer import RotationPlayersTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ListPlayers import ListPlayers

class RotationPlayers(RotationPlayersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Запрос данных из таблицы
    rows = list(app_tables.court.search())
    self.repeating_panel = self.repeating_panel_2
    # Словарь для отслеживания выбранных имен по всем выпадающим спискам
#    self.selected_players = {}# Ключ: (card_index, dropdown_id), Значение: выбранное имя
#   self.selected_players = []# Ключ: (card_index, dropdown_id), Значение: выбранное имя

    # Загрузка данных из таблицы соответствия
    correspondence_table = app_tables.s_players.search()
        # Создание словаря соответствия
    self.name_to_code = {row['name']: row['player_number'] for row in correspondence_table}

    
    # Проверка, пуста ли таблица
    if not rows:
    # Если таблица пустая, создаем одну пустую запись
      empty_record = self.empty_court()
      self.add_court(empty_record)
    else:
      last_record = app_tables.court.search(tables.order_by("game_id", ascending = False))
      self.last_game = last_record[0]['game_id']
      self.current_game_box.text = self.last_game

#    self.repeating_panel_2.items = anvil.server.call('get_records_with_names')

#    self.repeating_panel.set_event_handler('x-refresh-dropdowns', self.refresh_dropdowns)
    self.repeating_panel.set_event_handler('x-add-court', self.add_court) 
    self.repeating_panel.set_event_handler('x-save-court', self.save_court) 
    self.repeating_panel.set_event_handler('x-del-court', self.del_court) 
    
    # Полный список всех имен
    self.all_names = [row['name'] for row in app_tables.s_players.search()]
    
    self.repeating_panel_2.items = anvil.server.call('get_records_with_names')
          
    # Передача all_names в каждую карточку
    card_components = self.repeating_panel.get_components()
    for card in card_components:
        card.set_all_names(self.all_names)  # Передаем список имен через метод
         
  def edit_player_click(self, **event_args):
#    open_form(ListPlayers())
    ListPlayers()

  def link_players_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('RotationPlayers.ListPlayers')

  def link_session_click(self, **event_args):
    open_form('Session')

  def link_s_players_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Session.SessionPlayers')
     
  def add_court(self, item, **event_args):
#    item = {}
      
    rows = list(app_tables.court.search())
    # Проверка, пуста ли таблица
    if rows:
      item = self.empty_court()
      last_court = app_tables.court.search(tables.order_by("id", ascending = False))
      last_id = last_court[0]['id']
      item['id'] = last_id + 1

    # refresh the Data Grid
    anvil.server.call("add_court", item)
    self.repeating_panel.items = anvil.server.call('get_records_with_names')
    self.initialize_dropdowns()

  def del_court(self, court, **event_args):
    # Получение уникального идентификатора из словаря
    row_id = court['id']
    # Поиск строки в таблице
    row_to_delete = app_tables.court.get(id = row_id)
    row_to_delete.delete()
    self.repeating_panel.items = anvil.server.call('get_records_with_names')
    self.initialize_dropdowns()

  def save_court(self, court, **event_args):
    # Получение уникального идентификатора из словаря
    row_id = court['id']
    # Поиск строки в таблице
    row_to_edit = app_tables.court.get(id = row_id)

    row_to_edit['player_id_1'] = self.name_to_code[court['name_1']] 
    row_to_edit['player_id_2'] = self.name_to_code[court['name_2']] 
    row_to_edit['player_id_3'] = self.name_to_code[court['name_3']] 
    row_to_edit['player_id_4'] = self.name_to_code[court['name_4']] 

    row_to_edit.update()
    
    self.repeating_panel.items = anvil.server.call('get_records_with_names')
    self.initialize_dropdowns()

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
#        "bg_color_1": get_color_status(-1),
        "status_1": -1,
#        "bg_color_2": get_color_status(-1),
        "status_2": -1,
#        "bg_color_3": get_color_status(-1),
        "status_3": -1,
#        "bg_color_4": get_color_status(-1),
        "status_4": -1,
    }
    return records

