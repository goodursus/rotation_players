from ._anvil_designer import SessionPlayersTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .EditSessionPlayers import EditSessionPlayers

class SessionPlayers(SessionPlayersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items = [
                {
                    "player_number": row["player_number"],
                    "name": row["name"]
                }
                for row in app_tables.s_players.search()
            ]
    # Set an event handler on the RepeatingPanel (our 'articles_panel')
    self.repeating_panel_1.set_event_handler('x-delete-s_player', self.delete_s_player)
    #add this line to set the event handler
    self.repeating_panel_1.add_event_handler('x-edit-s_player', self.edit_s_player)
  
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

  def delete_s_player(self, player, **event_args):
    # Delete the article
    anvil.server.call('delete_s_player', player)
    # Refresh articles to remove the deleted article from the Homepage
    self.refresh_players()
    #self.parent.refresh_data_bindings()  # Обновляем таблицу в UI

  def refresh_players(self):
      self.repeating_panel_1.items = app_tables.s_players.search()   

  def edit_s_player(self, player, **event_args):
  #movie is the row from the Data Table
    item = dict(player)
    editing_form = EditSessionPlayers(item = item)

    #if the user clicks OK on the alert
    if alert(content = editing_form, large = True):
      #pass in the Data Table row and the updated info
      anvil.server.call('update_s_player', player, item)
      #refresh the Data Grid
      self.repeating_panel_1.items = app_tables.s_players.search()

  def home_session_players_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('RotationPlayers')
