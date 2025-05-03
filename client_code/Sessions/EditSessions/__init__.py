from ._anvil_designer import EditSessionsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime


class EditSessions(EditSessionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def date_picker_session_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.item["data_session"] = self.date_picker_session.date

  def text_box_3_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.text_box_4.text  = (self.text_box_3.text + 3) // 4
    self.item['number_courts'] = self.text_box_4.text
