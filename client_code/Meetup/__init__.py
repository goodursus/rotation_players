from ._anvil_designer import MeetupTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json

class Meetup(MeetupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.repeating_panel_1.items = app_tables.meetup_players.search()

#  def save_credentials_click(self, **event_args):
#    email = self.email_input.text
#    password = self.password_input.text
#    anvil.server.call('save_credentials', email, password)
#    anvil.notify("Учетные данные сохранены!")

#  def parse_attendees_click(self, **event_args):
#    event_url = self.url_input.text
#    try:
#      attendees = anvil.server.call('parse_meetup_event', event_url)
#      # Загрузка данных в таблицу
#      self.attendees_grid.items = attendees
#      # Сохранение в таблицу all_players
#      for attendee in attendees:
#        anvil.tables.get_table('meetup_players').add_row(
#          position=attendee['position'],
#          name=attendee['name'],
#          profile_url=attendee['profile_url']
#        )
#      anvil.notify(f"Найдено {len(attendees)} участников!")
#    except Exception as e:
#      anvil.notify(str(e), level='error')

  def file_loader_change(self, file, **event_args):
    """Обработчик загрузки файла"""
    if file.name.endswith('.json'):
      try:
        # Читаем содержимое файла
        json_data = json.loads(file.get_bytes().decode('utf-8'))

        # Вызываем серверную функцию
        result = anvil.server.call('import_players_from_json', json_data)
        alert(result)

        # Обновляем таблицу (если она есть на форме)
        if hasattr(self, 'players_repeating_panel'):
          self.players_repeating_panel.items = app_tables.all_players.search()

      except Exception as e:
        alert(f"Ошибка при обработке файла: {str(e)}")
    else:
      alert("Пожалуйста, загрузите JSON файл")  