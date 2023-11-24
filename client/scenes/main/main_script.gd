extends Node

@export var username_label : Label
@export var balance_label : Label

@export var username_request : HTTPRequest
@export var balance_request : HTTPRequest
@export var refresh_request : HTTPRequest


# Called when the node enters the scene tree for the first time.
func _ready():
	username_request.handle_request()
	balance_request.get_balance()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_username_request_request_completed(result, response_code, headers, body):
	if response_code == HTTPClient.RESPONSE_OK:
		body = JSON.parse_string(body.get_string_from_utf8())
		username_label.text = "Hello, {username}!".format(body)
	elif response_code == HTTPClient.RESPONSE_UNAUTHORIZED:
		refresh_request.handle_request()
		await refresh_request.request_completed
		username_request.handle_request()


func _on_balance_request_request_completed(result, response_code, headers, body):
	if response_code == HTTPClient.RESPONSE_OK:
		body = JSON.parse_string(body.get_string_from_utf8())
		balance_label.text = "Your balance is: {balance}".format(body)
	elif response_code == HTTPClient.RESPONSE_UNAUTHORIZED:
		refresh_request.handle_request()
		await refresh_request.request_completed
		balance_request.get_balance()


func _on_balance_add_pressed():
	balance_request.manipulate_balance("add", 100.0)
	await balance_request.request_completed


func _on_balance_subtract_pressed():
	balance_request.manipulate_balance("subtract", 100.0)
	await balance_request.request_completed
