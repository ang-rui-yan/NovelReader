# Read and split by =
def read_config(file_location):
	file_to_read = open(file_location, 'r')
	lines = file_to_read.readlines()
	no_blank_lines = [l for l in (line.strip() for line in lines) if l]
	
	config_dict = {}
	for line in no_blank_lines:
		if line:
			formatted_line = line.split("|")
			config_dict[formatted_line[0]] = formatted_line[1]
		
	return config_dict

# Write to Config
def update_config(file_location, updated_dict):
	dict_string = ""
	for key, value in updated_dict.items():
		dict_string += '{0}|{1}\n'.format(key, value)
	
	file_to_write = open(file_location, 'w')
	file_to_write.write(dict_string)
	file_to_write.close()

# Read line by line
def read_line_data(file_location):
	file_to_read = open(file_location, 'r')
	lines = file_to_read.readlines()
	no_blank_lines = [l for l in (line.strip() for line in lines) if l]
		
	line_list = []
	for line in no_blank_lines:
		if line:
			formatted_line = line.strip()
			line_list.append(formatted_line)
		
	return line_list
	