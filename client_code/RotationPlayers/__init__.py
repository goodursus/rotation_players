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

    last_record = app_tables.court.search(tables.order_by("game_id", ascending = False))
    self.last_game = last_record[0]['game_id']
    self.current_game_box.text = self.last_game

    self.repeating_panel_2.items = anvil.server.call('get_records_with_names')

    # Словарь для отслеживания выбранных имен по всем выпадающим спискам
    self.selected_players = {}  # Ключ: (card_index, dropdown_id), Значение: выбранное имя
    
    # Получаем Repeating Panel
    self.repeating_panel = self.repeating_panel_2
    self.repeating_panel.set_event_handler('x-refresh-dropdowns', self.refresh_dropdowns)
    
    # Инициализация выпадающих списков
    self.initialize_dropdowns()

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
      for card_index, card in enumerate(self.repeating_panel.items):
          for dropdown_id, dropdown in enumerate(card['dropdowns']):
              dropdown.items = self.get_available_players(card_index, dropdown_id)
              dropdown.set_event_handler('change', self.on_dropdown_change)

  def get_available_players(self, card_index, dropdown_id):
      """Получить список доступных имен для конкретного выпадающего списка."""
      selected_names = set(self.selected_players.values())
      return [player for player in self.all_players if player not in selected_names]

  def on_dropdown_change(self, sender, **event_args):
      """Обработчик изменения выбора в выпадающем списке."""
      card_index = event_args['item']['index']
      dropdown_id = event_args['dropdown_id']
      selected_name = sender.selected_value

      # Удаляем предыдущее выбранное имя из словаря
      key = (card_index, dropdown_id)
      if key in self.selected_players:
          previously_selected = self.selected_players[key]
          if previously_selected:
              self.all_players.append(previously_selected)

      # Обновляем словарь выбранных имен
      self.selected_players[key] = selected_name

      # Удаляем текущее выбранное имя из общего списка
      if selected_name:
          self.all_players.remove(selected_name)

      # Триггерим обновление всех выпадающих списков
      self.repeating_panel.raise_event('x-refresh-dropdowns')

  def refresh_dropdowns(self, **event_args):
      """Обновление всех выпадающих списков в Repeating Panel."""
      for card_index, card in enumerate(self.repeating_panel.items):
          for dropdown_id, dropdown in enumerate(card['dropdowns']):
            dropdown.items = self.get_available_players(card_index, dropdown_id)