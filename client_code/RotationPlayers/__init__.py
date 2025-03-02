from ._anvil_designer import RotationPlayersTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .EditListPlayers import EditListPlayers

class RotationPlayers(RotationPlayersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items = app_tables.players.search()
    self.repeating_panel_1.add_event_handler('x-edit-player', self.edit_player)
  
  def add_player_click(self, **event_args):
    item = {}
    editing_form = EditListPlayers(item=item)
  
    #if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
      #add the player to the Data Table with the filled in information
      anvil.server.call('add_player', item)
      #refresh the Data Grid
      self.repeating_panel_1.items = app_tables.players.search()

  def edit_player(self, player, **event_args):
    #player is the row from the Data Table
    item = dict(player)
    editing_form = EditListPlayers(item=item)
  
    #if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
      #pass in the Data Table row and the updated info
      anvil.server.call('update_player', player, item)
      #refresh the Data Grid
      self.repeating_panel_1.items = app_tables.players.search()