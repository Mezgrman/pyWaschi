#!/usr/bin/env python
# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

import random
import requests

class API:
	def __init__(self):
		self.server_list = []
		self.object_lists = {}
		self.reload_server_list()
		self.reload_object_lists()
	
	def reload_server_list(self):
		self.server_list = [url.replace("receive.php", "") for url in requests.get("http://waschi.org/servers.php").text.splitlines()]
	
	def reload_object_lists(self):
		for server in self.server_list:
			self.object_lists[server] = self.get_object_list(server)
	
	def choose_server(self):
		server = random.choice(self.server_list)
		return server
	
	def wash(self, clothing = None, username = "Hugo", password = "mycock", random_word = False):
		server = self.choose_server()
		data = {'Kleidung': clothing, 'Username': username, 'Password': password}
		if random_word:
			data['RandomWord'] = "true"
		result = requests.post(server + "echowash.php", data).text
		return result
	
	def get_object_list(self, server):
		objects = requests.get(server + "found").text.splitlines()
		return objects
	
	def pick_up(self, clothing = None, username = "Hugo", password = "mycock"):
		server = self.choose_server()
		result = requests.post(server + "echowash.php", {'Kleidung': clothing, 'Username': username, 'Password': password, 'TakeAway': "true"}).text
		return result
	
	def locate(self, clothing, case_sensitive = True):
		servers = []
		for server, objects in self.object_lists.iteritems():
			if case_sensitive:
				if server not in servers and clothing in objects:
					servers.append(server)
			else:
				if server not in servers and clothing.lower() in [obj.lower() for obj in objects]:
					servers.append(server)
		return servers