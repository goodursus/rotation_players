from ._anvil_designer import EditSessionTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class EditSession(EditSessionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def date_picker_session_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.item['data_session'] = self.date_picker_session.date

    