extends HTTPRequest


func handle_request():
	var headers = [
		"Content-Type: application/json",
		"Authorization: Bearer %s" % Globals.access_token
	]
	self.request("http://localhost:8000/api/users/info/", headers, HTTPClient.METHOD_GET)
