from ._anvil_designer import MultiSelectDropdownTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables

class MultiSelectDropdown(MultiSelectDropdownTemplate):
    def __init__(self, **properties):
      self.init_components(**properties)

      self.selected_values = []
      self.all_options = []
      self.options_rp.role = 'options-dropdown'
      self.tag_display.role = 'tag_display'
      self.options_rp.set_event_handler("x-click", self.option_selected)
      self.dropdown_area.visible = False
      self.limit_text.text = ""
  
      #      self.set_options([row['name'] for row in app_tables.players.search()], 11)
#      self.set_options(["Яблоко", "Банан", "Апельсин", "Груша"], 2)

    def set_options(self, options, limit):
      self.all_options = options
      self.selection_limit = limit
      self.update_options()
  
    def update_options(self):
      self.options_rp.items = [o for o in self.all_options if o not in self.selected_values]
#      print("options_rp.items is: ", self.options_rp.items)
#      print("options_rp.visible is: ", self.options_rp.visible)


    def update_stats(self):
      total = len(self.all_options)  # Общее кол-во игроков
      selected = len(self.selected_values)
      limit = self.selection_limit
      self.stats_label.text = f"All players: {total} / Selected: {selected} / Limit: {limit}"

    def option_selected(self, item, **event_args):
      if item in self.selected_values:
        return
  
      if len(self.selected_values) >= self.selection_limit:
        # Блокируем выбор
        alert(f"Limit reached: {self.selection_limit} players.")
        self.dropdown_area.visible = False
        return
  
      self.selected_values.append(item)
      self.update_tags()
      self.update_options()
      self.update_stats()
#      self.dropdown_area.visible = False

    def update_tags(self):
      # Очищаем область отображения
      self.tag_display.clear()

      for val in self.selected_values:
        button = Button(
          text=val + " ✖",
          role="tag-button",
        )
        button.tag.value = val
        button.role = 'tag-button'
        button.set_event_handler("click", self.remove_tag)
        self.tag_display.add_component(button)

    def remove_tag(self, sender, **event_args):
      val = sender.tag.value
      if val in self.selected_values:
        self.selected_values.remove(val)
        self.update_tags()
        self.update_options()  # Обновляем список выбора
  
        self.update_stats()
  
    def toggle_dropdown(self, **event_args):
      self.dropdown_area.visible = not self.dropdown_area.visible
#      self.dropdown_area.visible = True
      
    def tag_clickable_area_click(self, **event_args):
      self.toggle_dropdown()

    def icon_button_1_click(self, **event_args):
      self.parent.raise_event('x-add-s-players', item = {})
