from ._anvil_designer import MeetupTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Meetup(MeetupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def save_credentials_click(self, **event_args):
    email = self.email_input.text
    password = self.password_input.text
    anvil.server.call('save_credentials', email, password)
    anvil.notify("Учетные данные сохранены!")

  def parse_attendees_click(self, **event_args):
    event_url = self.url_input.text
    try:
      attendees = anvil.server.call('parse_meetup_event', event_url)
      # Загрузка данных в таблицу
      self.attendees_grid.items = attendees
      # Сохранение в таблицу all_players
      for attendee in attendees:
        anvil.tables.get_table('meetup_players').add_row(
          position=attendee['position'],
          name=attendee['name'],
          profile_url=attendee['profile_url']
        )
      anvil.notify(f"Найдено {len(attendees)} участников!")
    except Exception as e:
      anvil.notify(str(e), level='error')
  