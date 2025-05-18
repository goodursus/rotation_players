from ._anvil_designer import RowTemplateEditSessionsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplateEditSessions(RowTemplateEditSessionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
#    self.text_1.text = self.item['rule']['name']
    # Any code you write here will run before the form opens.
    # Если значение поля is_active = True, подсветим строку
    is_active = self.item['open']
    if is_active:
      self.label_check.text = "✅"
      self.role = "highlight-row"  # Подсветим строку
    else:
      self.label_check.text = "☐"  # Или "☐", или "—"

#    if self.item['open']:
#      self.role = "highlight-row"

  def edit_row_click(self, **event_args):
    self.parent.raise_event("x-edit-session", session=self.item)

  def delete_row_click(self, **event_args):
    self.parent.raise_event("x-delete-session", session=self.item)
