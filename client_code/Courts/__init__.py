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
    self.refresh_dropdown_session()
    
    self.repeating_panel.set_event_handler("x-save-court", self.save_court)
  
  def dropdown_session_change(self, **event_args):
    selected = self.dropdown_session.selected_value
    number_players = selected['number_players']
    self.multi_select_dropdown_1.set_options([row['name'] for row in app_tables.players.search()], number_players)
#    self.multi_select_dropdown_1.set_options(["Яблоко", "Банан", "Апельсин", "Груша"], 2)

#    if selected:
#      alert(f"You selected: {selected}")
  
  def refresh_dropdown_session(self):
    items = anvil.server.call('get_session_dropdown_items')
    self.dropdown_session.items = items


