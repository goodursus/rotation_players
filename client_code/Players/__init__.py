from ._anvil_designer import PlayersTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .PlayerEdit import PlayerEdit

class Players(PlayersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_player.items = app_tables.players.search()
    self.repeating_panel_player.add_event_handler("x-edit-player", self.edit_player)
    self.repeating_panel_player.add_event_handler("x-delete-player", self.delete_player)

  def player_add_click(self, **event_args):
    item = {}
    rows = list(app_tables.players.search())
    if not rows:
      # Если таблица пустая, создаем одну пустую запись
      item['player_id'] = 1
    else:
      last_record = app_tables.players.search(tables.order_by("player_id", ascending = False))
      next_id = (last_record[0]['player_id'] + 1) if last_record else 1  # Если нет записей, то ID = 1
      item['player_id'] = next_id
    
    editing_form = PlayerEdit(item=item)

    # if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
      # add the player to the Data Table with the filled in information
      anvil.server.call("add_player", item)
      # refresh the Data Grid
      self.repeating_panel_player.items = app_tables.players.search()

  def edit_player(self, player, **event_args):
    # player is the row from the Data Table
    item = dict(player)
    editing_form = PlayerEdit(item=item)

    # if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
      # pass in the Data Table row and the updated info
      anvil.server.call("update_player", player, item)
      # refresh the Data Grid
      self.repeating_panel_player.items = app_tables.players.search()

  def delete_player(self, player, **event_args):
    if confirm(f"Do you really want to delete the player {player['name']}?"):
      anvil.server.call("delete_player", player)
      # refresh the Data Grid
      self.repeating_panel_player.items = app_tables.players.search()

  
