from ._anvil_designer import OptionTemplateTemplate
from anvil import *
import anvil.server


class OptionTemplate(OptionTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.link_1.text = self.item  # Отображаем текст элемента
    self.link_1.role = 'option-item'  
  #        self.parent.link_1.set_event_handler("click", self.item_clicked)

  #    def item_clicked(self, **event_args):
  #        self.parent.raise_event("x-select", item=self.item)

    def link_1_click(self, **event_args):
      self.parent.raise_event("x-click", item=self.item)