import requests

class BaseIntegrationApi:
	_url = None
	headers = {"Content-Type": "application/json"}

	def _get(self, path, params=None):
		res = requests.get(
			self._url + path, verify=False, params=params, headers=self.headers
		)
		if res.status_code == 200:
			return res.json()
		else:
			raise ValueError(
				f"Error in get services: {self._url + path}, {res.text}"
			)

	def _post(self, path, obj, params=None, custom_url=None):
		headers = {"Content-Type": "application/json"}
		base_url = self._url
		if custom_url is not None:
			base_url = custom_url
		res = requests.post(
			base_url + path, obj, verify=False, headers=headers, params=params
		)
		if res.status_code == 200:
			return res.json()
		else:
			raise ValueError(
				f"Error in post services: {base_url + path}, {res.text}"
			)

	def _put(self, path, obj=None, params=None):
		headers = {"Content-Type": "application/json"}
		res = requests.put(
			self._url + path, obj, verify=False, headers=headers, params=params
		)
		if res.status_code == 200:
			return res.json()
		else:
			raise ValueError(
				f"Error in put service: {self._url + path}, {res.text}"
			)

	def _delete(self, path, params=None):
		headers = {"Content-Type": "application/json"}
		res = requests.delete(
			self._url + path, verify=False, headers=headers, params=params
		)
		if res.status_code == 200:
			return res.json()
		else:
			raise ValueError(
				f"Error in delete service: {self._url + path}, {res.text}"
			)