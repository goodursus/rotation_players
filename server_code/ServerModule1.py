import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

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

def get_game_status(value):
  color_map = {1: "#d4edda", -1: "#cce5ff", 0: "#fff3cd"}  # Цвет фона
  return color_map.get(value, "#ffffff")

@anvil.server.callable
def get_records_with_names():
    # Создаем словарь кодов и имен
    players_dict = {row['number_player']: row['name'] for row in app_tables.players.search()}
    
    # Загружаем записи и подставляем имя + другие данные
    records = [
        {
            "name_1": players_dict.get(row['player_id_1'], "Неизвестно"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_1": row['player_id_1'],
            "name_2": players_dict.get(row['player_id_2'], "Неизвестно"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_2": row['player_id_2'],
            "name_3": players_dict.get(row['player_id_3'], "Неизвестно"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_3": row['player_id_3'],
            "name_4": players_dict.get(row['player_id_4'], "Неизвестно"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_4": row['player_id_4'],
            "id": row['id'],  # Дополнительные текстовые поля
            "game_id": row['game_id'],
            "bg_color_1": get_game_status(row['status_1']),
            "status_1": row['status_1'],
            "bg_color_2": get_game_status(row['status_2']),
            "status_2": row['status_2'],
            "bg_color_3": get_game_status(row['status_3']),
            "status_3": row['status_3'],
            "bg_color_4": get_game_status(row['status_4']),
            "status_4": row['status_4'],
        }
        for row in app_tables.court.search()
    ]
    # *** ОТЛАДОЧНЫЙ ВЫВОД ***
    #for record in records:
    #    print(f"Status: {record['status']}, Bg Color: {record['bg_color']}")
    return records

@anvil.server.callable
def add_session(session_data):
  if session_data.get('session_id') and session_data.get('data_session') and session_data.get('number_players'):
      app_tables.session.add_row(**session_data)

@anvil.server.callable
def update_session(session, session_data):
  if session_data['session_id'] and session_data['data_session'] and session_data['number_players'] and session_data['number_courts']:
    session.update(**session_data)

@anvil.server.callable
def delete_session(session):
    session.delete()    