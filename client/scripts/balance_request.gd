extends HTTPRequest


func get_balance():
	var headers = [
		"Content-Type: application/json",
		"Authorization: Bearer %s" % Globals.access_token
	]
	self.request("http://localhost:8000/api/users/balance/", headers, HTTPClient.METHOD_GET)	

func manipulate_balance(action: String = 'add', value: float = 0):
	var headers = [
		"Content-Type: application/json",
		"Authorization: Bearer %s" % Globals.access_token
	]
	var body = JSON.stringify({
		"action": action,
		"value": value
	})
	self.request("http://localhost:8000/api/users/balance/", headers, HTTPClient.METHOD_POST, body)
