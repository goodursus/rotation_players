from ._anvil_designer import RowTemplateSessionPlayerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplateSessionPlayer(RowTemplateSessionPlayerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def del_button_click(self, **event_args):
    # Get the user to confirm if they wish to delete the article
    # If yes, raise the 'x-delete-article' event on the parent 
    # (which is the articles_panel on Homepage)
#    if confirm("Are you sure you want to delete {}?".format(self.item['name'])):
    id_to_delete = self.item['player_number']  # id - первый элемент кортежа
    row_to_delete = app_tables.s_players.get(player_number = id_to_delete)

    self.parent.raise_event('x-delete-s_player', player = row_to_delete)

  def edit_s_player_button_click(self, **event_args):
    self.parent.raise_event('x-edit-s_player', player = self.item)
