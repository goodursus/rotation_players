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
from .CourtComponent import CourtComponent

class Courts(CourtsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.all_names = []
    self.session_id = 0
    self.refresh_dropdown_session()
 
  def dropdown_session_change(self, **event_args):
    selected = self.dropdown_session.selected_value
    number_players = selected['number_players']
    self.multi_select_dropdown_1.selection_limit = number_players
    self.session_id = selected['session_id']
    session_rule = selected['rule']
    self.text_name_rule.text = 'Rule: ' + session_rule['name']
    self.text_name_rule.text_color = 'blue'
    # Полный список всех имен
    self.selected_names = [row["name"] for row in app_tables.s_players.search(session_id = self.session_id)]
    if not self.selected_names:
      self.multi_select_dropdown_1.set_options([row["name"] for row in app_tables.players.search()], number_players, self.session_id)
    else:
      self.all_names = [row["name"] for row in app_tables.players.search()]
      self.multi_select_dropdown_1.selected_values = self.selected_names 
      self.multi_select_dropdown_1.all_options = self.all_names
      self.multi_select_dropdown_1.tag_display.clear()
      for val in self.all_names:
        button = Button(
          text=val + " ✖",
          role="tag-button",
        )
        button.tag.value = val
        button.role = 'tag-button'
        button.set_event_handler("click", self.multi_select_dropdown_1.remove_tag)
        self.multi_select_dropdown_1.tag_display.add_component(button)

  def refresh_dropdown_session(self):
    items = anvil.server.call('get_session_dropdown_items')
    self.dropdown_session.items = items

  def arrangement_button_click(self, **event_args):
    group_courts = anvil.server.call("get_court_groups", self.session_id)
    print(group_courts)
    # Создаём экземпляр формы с параметрами
    self.court_form = CourtComponent()

    # Вставляем её на форму (например, в ColumnPanel или FlowPanel)
    self.courts_panel.clear()
    self.courts_panel.add_component(self.court_form)
    self.court_form.lottery_click()


