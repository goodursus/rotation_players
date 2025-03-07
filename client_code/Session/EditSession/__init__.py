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

    last_record = app_tables.session.search(tables.order_by("session_id", ascending=False))
    next_id = (last_record[0]['session_id'] + 1) if last_record else 1  # Если нет записей, то ID = 1
    current_date = datetime.now().date()
    self.item['session_id'] = next_id
    self.item['data_session'] = current_date

