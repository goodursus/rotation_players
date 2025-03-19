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

  def drop_down_1_change(self, **event_args):
    sender = event_args['sender']
    self.selected_name['new_name_1'] = sender.selected_value

    self.parent.raise_event('x-refresh-dropdowns')

  def drop_down_2_change(self, **event_args):
    sender = event_args['sender']
    self.selected_name['new_name_2'] = sender.selected_value

    self.parent.raise_event('x-refresh-dropdowns')

  def add_court_button_click(self, **event_args):
    self.parent.raise_event('x-add-court', item = {})

  def save_court_button_click(self, **event_args):
    self.item['name_1'] = self.drop_down_1.selected_value
    self.item['name_2'] = self.drop_down_2.selected_value
    self.item['name_3'] = self.drop_down_3.selected_value
    self.item['name_4'] = self.drop_down_4.selected_value
    self.parent.raise_event('x-save-court', court = self.item)

  def del_court_button_click(self, **event_args):
    self.parent.raise_event('x-del-court', court = self.item)

