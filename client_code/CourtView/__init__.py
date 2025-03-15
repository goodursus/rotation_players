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
      """Обработчик изменения выбора в выпадающем списке."""
      # Триггерим обновление всех выпадающих списков
      sender = event_args['sender']
      selected_name = sender.selected_value
  
      self.parent.raise_event('x-refresh-dropdowns', selected_name = selected_name)

