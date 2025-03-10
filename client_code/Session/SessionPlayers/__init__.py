from ._anvil_designer import SessionPlayersTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .EditSessionPlayers import EditSessionPlayers

class SessionPlayers(SessionPlayersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items = app_tables.s_players.search()

  def add_player_click(self, **event_args):
    #pass in an empty dictionary to MovieEdit
    item = {}
    editing_form = EditSessionPlayers(item = item)
    
    #if the user clicks OK on the alert
    if alert(content = editing_form, large=True):
      #add the movie to the Data Table with the filled in information
      anvil.server.call('add_s_player', item)
      #refresh the Data Grid
      self.repeating_panel_1.items = app_tables.s_players.search()
