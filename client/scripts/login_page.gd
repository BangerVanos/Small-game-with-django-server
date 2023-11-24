extends Node


func _on_http_request_request_completed(result, response_code, headers, body):
	if response_code == HTTPClient.RESPONSE_UNAUTHORIZED:
		print(JSON.parse_string(body.get_string_from_utf8())['detail'])
	elif response_code == 200:
		var tokens = JSON.parse_string(body.get_string_from_utf8())
		Globals.access_token = tokens['access']
		Globals.refresh_token = tokens['refresh']
		get_tree().change_scene_to_file("res://scenes/main/main_game.tscn")
