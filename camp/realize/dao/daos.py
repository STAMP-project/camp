import os

class FileContentCommiter(object):

	def __init__(self, *args, **kwargs):
		self.search_dir = kwargs.get('search_dir') or "./"
		self.read_file_path = kwargs.get('read_file_path') or ""
		self.write_file_path = kwargs.get('write_file_path') or self.read_file_path
	
	def set_read_file(self, _file_path):
		self.read_file_path = _file_path

	def set_write_file(self, _file_path):
		self.write_file_path = _file_path

	def read_content(self):
		self.read_file_path = os.path.join(self.search_dir, self.read_file_path)
		contents = ""
		with open(self.read_file_path, "r") as file:
			contents = file.read()
		return contents

	def write_content(self, content):
		self.write_file_path = os.path.join(self.search_dir, self.write_file_path)
		dirname = os.path.dirname(self.write_file_path)
		if not os.path.exists(dirname):
			os.makedirs(dirname)

		with open(self.write_file_path, "w") as file:
			file.write(content)