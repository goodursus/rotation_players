from ._anvil_designer import EditSessionPlayersTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EditSessionPlayers(EditSessionPlayersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.list_players = [
#      (player['name'], player) for player in app_tables.players.search()
      (player['name']) for player in app_tables.players.search()
    ]
    self.list_players_box.items = self.list_players

  def list_players_box_change(self, **event_args):
    """This method is called when an item is selected"""
  #  self.item['name'] = self.list_players_box.selected_value
