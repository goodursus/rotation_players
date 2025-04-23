from ._anvil_designer import MainTemplateTemplate
from ._anvil_designer import CourtsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class MainTemplate(MainTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    # Проверка у сервера, локальный ли запуск
    try:
      if not anvil.server.call("is_local_server"):
        self.copy_data_btn.visible = False
    except Exception as e:
      # Если что-то пошло не так (например, нет соединения), скроем кнопку
      self.copy_data_btn.visible = False

  def link_players_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Players')

  def link_courts_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Courts')

  def copy_data_btn_click(self, **event_args):
    try:
        anvil.server.call('copy_cloud_to_local')
        alert("✅ Данные успешно скопированы из облака в локальные таблицы.")
    except Exception as e:
        alert(f"❌ Ошибка при копировании: {e}")

