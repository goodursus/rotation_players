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
    self.refresh_sessions_dropdown()

  def session_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

def refresh_sessions_dropdown(self):
  items = anvil.server.call('get_session_dropdown_items')
  self.session_dropdown.items = items

def session_dropdown_change(self, **event_args):
  selected = self.session_dropdown.selected_value
  if selected:
    alert(f"You selected: {selected}")