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
from .MultiSelectDropdown import MultiSelectDropdown

class Courts(CourtsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Создаём экземпляр компонента
#    self.dropdown_component = MultiSelectDropdown()
#    self.column_panel_1.add_component(self.dropdown_component)
    
    # Any code you write here will run before the form opens.
    self.all_names = []
    self.refresh_dropdown_session()
 
  def dropdown_session_change(self, **event_args):
    selected = self.dropdown_session.selected_value
    number_players = selected['number_players']
    session_id = selected['session_id']
    # Полный список всех имен
    self.all_names = [row["name"] for row in app_tables.s_players.search(session_id = session_id)]
    if not self.all_names:
      self.multi_select_dropdown_1.set_options([row["name"] for row in app_tables.players.search()], number_players, session_id)
    else:
      print(self.all_names)

  def refresh_dropdown_session(self):
    items = anvil.server.call('get_session_dropdown_items')
    self.dropdown_session.items = items


