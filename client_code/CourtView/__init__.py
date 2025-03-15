from ._anvil_designer import CourtViewTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CourtView(CourtViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.list_s_players = [
          (player['name']) for player in app_tables.s_players.search()
        ]
    self.drop_down_1.items = self.list_s_players