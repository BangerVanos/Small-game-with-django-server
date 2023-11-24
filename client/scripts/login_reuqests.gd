extends HTTPRequest

@export var username_textfield : LineEdit
@export var password_textfield : LineEdit


func _on_log_in_pressed():
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({'username': username_textfield.text,
							   'password': password_textfield.text})
	self.request("http://localhost:8000/api/users/login/", headers,
				 HTTPClient.METHOD_POST, body)
