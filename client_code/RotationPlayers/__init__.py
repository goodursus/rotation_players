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

    self.repeating_panel_2.items = anvil.server.call('get_records_with_names')

    self.repeating_panel.set_event_handler('x-refresh-dropdowns', self.refresh_dropdowns)
    self.repeating_panel.set_event_handler('x-add-court', self.add_court) 
    self.repeating_panel.set_event_handler('x-save-court', self.save_court) 
    self.repeating_panel.set_event_handler('x-del-court', self.del_court) 
    
    # Полный список всех имен
    self.all_names = [row['name'] for row in app_tables.s_players.search()]
    
    # Инициализация данных для Repeating Panel
    self.repeating_panel.items = [
        {'name_1': None, 'name_2': None, 'name_3': None, 'name_4': None}
        for _ in range(5)  # Пример: 5 карточек
    ]    
    # Передача all_names в каждую карточку
    for card in self.repeating_panel.get_components():
        card.all_names = self.all_names
          
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
     
  def initialize_dropdowns(self):
      """Инициализация выпадающих списков для всех карточек."""
      # Получаем компоненты карточек
      card_components = self.repeating_panel.get_components()
      
      for card_index, card in enumerate(card_components):
          # Явное обращение к каждому выпадающему списку
          dropdown_names = ['name_1', 'name_2', 'name_3', 'name_4']
          for dropdown_name in dropdown_names:
              dropdown = card.get_component(dropdown_name)
              dropdown.items = self.get_available_names(card_index, dropdown_name)
              dropdown.set_event_handler('change', self.on_dropdown_change)
              
  def get_available_names(self, card_index, dropdown_name):
    """Получить список доступных имен для конкретного выпадающего списка."""
    selected_names_set = set(self.selected_names.values())
    
    # Если текущий выпадающий список уже имеет выбранное значение, добавляем его обратно
    key = (card_index, dropdown_name)
    if key in self.selected_names:
        selected_value = self.selected_names[key]
        return [name for name in self.all_names if name not in selected_names_set or name == selected_value]
    
    # В противном случае исключаем все выбранные имена
    return [name for name in self.all_names if name not in selected_names_set]
    
  def on_dropdown_change(self, sender, **event_args):
      """Обработчик изменения выбора в выпадающем списке."""
      # Получаем индекс карточки через родительский компонент
      card = sender.parent
      card_index = self.repeating_panel.get_components().index(card)
      
      dropdown_name = sender.name  # Имя выпадающего списка (например, 'name_1')
      selected_name = sender.selected_value
  
      # Удаляем предыдущее выбранное имя из словаря
      key = (card_index, dropdown_name)
      if key in self.selected_names:
          previously_selected = self.selected_names[key]
          if previously_selected:
              # Возвращаем ранее выбранное имя в общий пул
              self.all_names.append(previously_selected)
  
      # Обновляем словарь выбранных имен
      self.selected_names[key] = selected_name
  
      # Удаляем текущее выбранное имя из общего пула
      if selected_name:
          self.all_names.remove(selected_name)
  
      # Обновляем все выпадающие списки
      self.refresh_dropdowns()
  
  def refresh_dropdowns(self):
      """Обновление всех выпадающих списков в Repeating Panel."""
      # Получаем компоненты карточек
      card_components = self.repeating_panel.get_components()
      
      for card_index, card in enumerate(card_components):
          dropdown_names = ['name_1', 'name_2', 'name_3', 'name_4']
          for dropdown_name in dropdown_names:
              dropdown = card.get_component(dropdown_name)
              dropdown.items = self.get_available_names(card_index, dropdown_name)
          
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

