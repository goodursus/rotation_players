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

    # Флаг для проверки, были ли установлены all_names
    self._initialized = False

  def set_all_names(self, all_names):
      """Установка списка all_names."""
      self.all_names = all_names
      self._initialized = True
      
      # Инициализация выпадающих списков после установки all_names
      self.drop_down_1.items = self.get_available_names('name_1')
      self.drop_down_2.items = self.get_available_names('name_2')
      self.drop_down_3.items = self.get_available_names('name_3')
      self.drop_down_4.items = self.get_available_names('name_4')
      
      # Установка обработчиков событий
      self.drop_down_1.set_event_handler('change', lambda **e: self.on_dropdown_change('name_1'))
      self.drop_down_2.set_event_handler('change', lambda **e: self.on_dropdown_change('name_2'))
      self.drop_down_3.set_event_handler('change', lambda **e: self.on_dropdown_change('name_3'))
      self.drop_down_4.set_event_handler('change', lambda **e: self.on_dropdown_change('name_4'))

#  def drop_down_1_change(self, **event_args):
#    self.parent.raise_event('x-refresh-dropdowns')

  def get_available_names(self, dropdown_name):
    """Получить список доступных имен для конкретного выпадающего списка."""
    if not self._initialized:
        raise ValueError("Список all_names не был установлен.")
    
    selected_names_set = set(self.item.values())  # Все выбранные имена в карточке
    return [
        name for name in self.all_names
        if name not in selected_names_set or name == self.item[dropdown_name]
    ]

  def on_dropdown_change(self, dropdown_name):
    """Обработчик изменения выбора в выпадающем списке."""
    if not self._initialized:
        raise ValueError("Список all_names не был установлен.")
    
    selected_value = getattr(self, f"drop_down_{dropdown_name[-1]}").selected_value
    self.item[dropdown_name] = selected_value
    self.save_court_button.background = '#FFCCCC'  # Светло-красный цвет
    self.refresh_dropdowns()

  def refresh_dropdowns(self):
    """Обновление доступных значений для всех выпадающих списков."""
    if not self._initialized:
        raise ValueError("Список all_names не был установлен.")
    
    self.drop_down_1.items = self.get_available_names('name_1')
    self.drop_down_2.items = self.get_available_names('name_2')
    self.drop_down_3.items = self.get_available_names('name_3')
    self.drop_down_4.items = self.get_available_names('name_4')   
    
#  def drop_down_2_change(self, **event_args):
#    sender = event_args['sender']
#    self.selected_name['new_name_2'] = sender.selected_value

#    self.parent.raise_event('x-refresh-dropdowns')

  def add_court_button_click(self, **event_args):
    self.parent.raise_event('x-add-court', item = {})
#    self.refresh_dropdowns()

  def save_court_button_click(self, **event_args):
    self.parent.raise_event('x-save-court', court = self.item)
    # Возвращаем кнопке исходный цвет
    self.save_court_button.background = None  # Цвет по умолчанию
    self.refresh_dropdowns()

  def del_court_button_click(self, **event_args):
    self.parent.raise_event('x-del-court', court = self.item)

  def score_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass

