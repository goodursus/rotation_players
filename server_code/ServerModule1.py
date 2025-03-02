import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def add_player(player_data):
  if player_data.get('number_player') and player_data.get('name'):
      app_tables.players.add_row(**player_data)