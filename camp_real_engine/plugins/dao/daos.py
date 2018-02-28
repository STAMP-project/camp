import os

class FileContentCommiter(object):

	def __init__(self, *args, **kwargs):
		self.search_dir = kwargs.get('search_dir') or "./"
	
	def read_content(self, file_path):
		contents = ""
		with open(file_path, "r") as file:
			contents = file.read()
		return contents

	def write_content(self, file_path, content):
		dirname = os.path.dirname(file_path)
		if not os.path.exists(dirname):
			os.makedirs(dirname)

		with open(file_path, "w") as file:
			file.write(content)