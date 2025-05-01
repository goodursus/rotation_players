#from ._anvil_designer import MultiSelectDropDownTemplate
from ._anvil_designer import CourtsTemplate
from anvil import *
import anvil.server
#import anvil.google.auth, anvil.google.drive
#from anvil.google.drive import app_files
import anvil.tables as tables
from anvil.google.drive import app_files
import anvil.tables.query as q
from anvil.tables import app_tables


class Courts(CourtsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
#    self.repeating_panel_player.items = app_tables.players.search()
    self.multi_select_dropdown_1.set_options([r['name'] for r in app_tables.players.search()], 5)
