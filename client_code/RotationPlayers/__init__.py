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
    self.selected_players = {}# Ключ: (card_index, dropdown_id), Значение: выбранное имя
    
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
    for card_index, card_data in enumerate(self.repeating_panel.items):
      # Получаем ссылку на карточку (компоненту outlined_card)
      card = self.repeating_panel.get_components()[card_index]
      self.list_s_players = [
            (player['name']) for player in app_tables.s_players.search()
          ]
      card.drop_down_1.items = self.get_available_players(card_index)
      card.drop_down_2.items = self.get_available_players(card_index)
      card.drop_down_3.items = self.get_available_players(card_index)
      card.drop_down_4.items = self.get_available_players(card_index)

  def get_available_players(self, card_index):
      """Получить список доступных имен для конкретного выпадающего списка."""
      selected_names = set(self.selected_players.values())
      return [player for player in self.list_s_players if player not in selected_names]

  def refresh_dropdowns(self, selected_name, **event_args):
      """Обновление всех выпадающих списков в Repeating Panel."""
      # Удаляем текущее выбранное имя из общего списка
      self.selected_players.append(selected_name)
      if selected_name:
          self.list_s_players.remove(selected_name)

      for card_index, card_data in enumerate(self.repeating_panel.items):
        # Получаем ссылку на карточку (компоненту outlined_card)
        card = self.repeating_panel.get_components()[card_index]
        card.drop_down_1.items = self.get_available_players(card_index)
        card.drop_down_2.items = self.get_available_players(card_index)
        card.drop_down_3.items = self.get_available_players(card_index)
        card.drop_down_4.items = self.get_available_players(card_index)
