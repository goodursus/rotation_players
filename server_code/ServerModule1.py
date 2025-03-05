import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def add_player(player_data):
  if player_data.get('number_player') and player_data.get('name'):
      app_tables.players.add_row(**player_data)

@anvil.server.callable
def update_player(player, player_data):
  if player_data['number_player'] and player_data['name']:
    player.update(**player_data)

@anvil.server.callable
def delete_player(player):
    player.delete()    

# In your Server Module
@anvil.server.callable
def get_courts():
  # Get a list of articles from the Data Table, sorted by 'created' column, in descending order
  return app_tables.court.search(
    tables.order_by("id", ascending = True)
  )  