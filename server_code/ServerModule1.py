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

@anvil.server.callable
def get_records_with_names():
    # Создаем словарь кодов и имен
    players_dict = {row['number_player']: row['name'] for row in app_tables.players.search()}
    
    # Загружаем записи и подставляем имя вместо кода
    return [
        {
            "name_1": players_dict.get(row['player_id_1'], "Неизвестно"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_1": row['player_id_1'],
            "name_2": players_dict.get(row['player_id_2'], "Неизвестно"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_2": row['player_id_2'],
            "name_3": players_dict.get(row['player_id_3'], "Неизвестно"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_3": row['player_id_3'],
            "name_4": players_dict.get(row['player_id_4'], "Неизвестно"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_4": row['player_id_4'],
        }
        for row in app_tables.court.search()
    ]  