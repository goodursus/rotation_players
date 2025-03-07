from ._anvil_designer import SessionTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .EditSession import EditSession
from datetime import datetime

class Session(SessionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_session.items = app_tables.session.search()

  def add_session_button_click(self, **event_args):
    last_record = app_tables.session.search(tables.order_by("session_id", ascending=False))
    next_id = (last_record[0]['session_id'] + 1) if last_record else 1  # Если нет записей, то ID = 1
    current_date = datetime.now().date()
    item = {'session_id': next_id, 'data_session': current_date}
    editing_form = EditSession(item=item)

    # if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
      # add the session to the Data Table with the filled in information
      anvil.server.call("add_session", item)
      # refresh the Data Grid
      self.repeating_panel_session.items = app_tables.session.search()

  def home_session_click(self, **event_args):
    open_form('RotationPlayers')
