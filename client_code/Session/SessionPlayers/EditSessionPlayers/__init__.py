from ._anvil_designer import EditSessionPlayersTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EditSessionPlayers(EditSessionPlayersTemplate):
#  def __init__(self, item = {}, **properties):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.list_players = [
      (player['name']) for player in app_tables.players.search()
    ]
    self.list_players_box.items = self.list_players
        
#    if self.player_number_box.text is None:
#      last_record = app_tables.s_players.search(tables.order_by("player_number", ascending = False))
#      self.next_id = last_record[0]['player_number'] + 1 if last_record else 1
#      self.player_number_box.text = self.next_id
#    else:  
#      self.next_id = self.player_number_box.text
      
  def list_players_box_change(self, **event_args):
    """This method is called when an item is selected"""
    selected = self.list_players_box.selected_value
    rows = app_tables.players.search(name = selected)
    self.item['player_number'] = rows[0]['player_id'] 
    self.player_number_box.text = rows[0]['player_id']