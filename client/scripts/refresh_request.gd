extends HTTPRequest


func handle_request():
	var headers = [
		"Content-Type: application/json"		
	]
	var body = JSON.stringify({
		"refresh": Globals.refresh_token
	})
	self.request("http://localhost:8000/api/users/refresh/", headers, HTTPClient.METHOD_POST,
				 body)


func _on_request_completed(_result, response_code, _headers, body):
	if response_code == HTTPClient.RESPONSE_OK:
		var access_token: String = JSON.parse_string(body.get_string_from_utf8())['access']
		Globals.access_token = access_token
