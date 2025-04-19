from ._anvil_designer import SessionTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
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
    #add this line to set the event handler
    self.repeating_panel_session.add_event_handler('x-edit-session', self.edit_session)
    self.repeating_panel_session.add_event_handler('x-delete-session', self.delete_session) 
  
  def add_session_button_click(self, **event_args):
    item = {}
    rows = list(app_tables.session.search())
    if not rows:
      # Если таблица пустая, создаем одну пустую запись
      item['session_id'] = 1
      item['data_session'] = datetime.now().date()
    else:
      last_record = app_tables.session.search(tables.order_by("session_id", ascending = False))
      next_id = (last_record[0]['session_id'] + 1) if last_record else 1  # Если нет записей, то ID = 1
      item['session_id'] = next_id
      item['data_session'] = datetime.now().date()

    players = list(app_tables.s_players.search())
    player_count = len(players)
    item['number_players'] = player_count
    item['number_courts']  = (player_count + 3) // 4
    editing_form = EditSession(item=item)

    # if the user clicks OK on the alert
    if alert(content = editing_form, large=True):
      # add the session to the Data Table with the filled in information
      anvil.server.call("add_session", item)
      # refresh the Data Grid
      self.repeating_panel_session.items = app_tables.session.search()

  def home_session_click(self, **event_args):
    open_form('RotationPlayers')

  def edit_session(self, session, **event_args):
    #movie is the row from the Data Table
    item = dict(session)
    editing_form = EditSession(item = item)
  
    #if the user clicks OK on the alert
    if alert(content = editing_form, large=True):
      #pass in the Data Table row and the updated info
      anvil.server.call('update_session', session, item)
      #refresh the Data Grid
      self.repeating_panel_session.items = app_tables.session.search()

  def delete_session(self, session, **event_args):
    if confirm(f"Do you really want to delete the session {session['session_id']} at {session['data_session']}?"):
      anvil.server.call('delete_session', session)
      #refresh the Data Grid
      self.repeating_panel_session.items = app_tables.session.search()
