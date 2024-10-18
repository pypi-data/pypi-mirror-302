# """Common Definitions used across project"""
# ------------------------------------------------------------------------------
import yaml
from yaml import UnsafeLoader
import subprocess as sp
import pandas as pd
import os
# ------------------------------------------------------------------------------

### IDENTIFER OF COMMAND LINE ### >
CMD_LINE_START_WITH = "output for command: "

# ------------------------------------------------------------------------------

def remove_domain(hn):
	"""Removes domain suffix from provided hostname string

	Args:
		hn (str): fully qualified dns hostname

	Returns:
		str: hostname left by removing domain suffix
	"""
	return hn.split(".")[0]

def read_file(file):
	"""read the provided text file and retuns output in list format

	Args:
		file (str): text file name

	Returns:
		list: output converted to list (separated by lines)
	"""    	
	with open(file, 'r') as f:
		file_lines = f.readlines()
	return file_lines

def read_yaml_mode_us(file):
	try:
		with open(file, 'r') as f:
			return  yaml.load(f, Loader=UnsafeLoader)
	except Exception as e:
		raise Exception(f"Unable to Read the file, or invalid data \n{e}")


# ------------------------------------------------------------------------------

def get_op(file, cmd):
	"""filter the command output from given captured file.  
	Note: output should be taken from capture_it utility or it should be in the format
	derived by it.

	Args:
		file (str): capture file
		cmd (str): show command for which output to capture

	Returns:
		list: filtered command output in list format
	"""    	
	file_lines = read_file(file)
	toggle, op_lst = False, []
	for l in file_lines:
		if l.find(CMD_LINE_START_WITH)>0:
			toggle = l.find(cmd)>0
			continue
		if toggle:
			op_lst.append(l.strip())
	return op_lst

def get_ops(file, cmd_startswith):
	"""filter the command outputs from given captured file.  
	Note: output should be taken from capture_it utility or it should be in the format
	derived by it.

	Args:
		file (str): capture file
		cmd_startswith (str): show command start string

	Returns:
		dict: filtered command output in dict format
	"""    	
	file_lines = read_file(file)
	toggle, op_lst, op_dict = False, [], {}
	for l in file_lines:
		if toggle and l.find(CMD_LINE_START_WITH)>0:
			op_dict[cmd] = op_lst
			op_lst = []
			toggle=False
		if l.find(CMD_LINE_START_WITH)>0:
			toggle = l.find(cmd_startswith)>0
			cmd = l[l.find(cmd_startswith):].strip()
			continue
		if toggle:
			op_lst.append(l.rstrip())
	return op_dict
# ------------------------------------------------------------------------------

def blank_line(line): 
	"""checks if provided line is blank line or not.

	Args:
		line (str): input line

	Returns:
		bool: is line blank or not
	"""	
	return not line.strip()

def get_device_manufacturar(file):
	"""finds out manufacturer (cisco/juniper) from given capture file.
	in case if not found, it will return as Unidentified.

	Args:
		file (str): input capture file

	Returns:
		str: Either one from - Cisco, Juniper, Unidentified
	"""    	
	file_lines = read_file(file)
	for l in file_lines:
		if l.startswith("!"): return "Cisco"
		if l.startswith("#"): return "Juniper"
	return "Unidentified"

def verifid_output(cmd_op):
	"""vefifies if command output is in valid state.  Multiline string are splits with
	CR. and retuns as list. if input is a list, it will be returned as is.
	any other input will throw error.

	Args:
		cmd_op (list, str): Either list or Multiline string of output

	Raises:
		TypeError: Raise error if input is other than string or list.

	Returns:
		list: output in list format
	"""    	
	if isinstance(cmd_op, str):
		cmd_op = cmd_op.split("\n")
	if not isinstance(cmd_op, list):
		raise TypeError("Invalid Command Output Received.\n"
			f"Expected either multiline-string or list, received {type(cmd_op)}.")
	return cmd_op
# ------------------------------------------------------------------------------

def get_string_part(line, begin, end):
	"""get the sub-string out of provided long string(line)

	Args:
		line (str): string line
		begin (int): sub-str start point
		end (int): sub-str end point

	Raises:
		TypeError: Raise error if input is invalid or sub-string falls outside

	Returns:
		str: sub-string
	"""    	
	try: return line[begin: end].strip()
	except: raise TypeError("Unrecognized Input")

def get_string_trailing(line, begin_at):
	"""get the training part of sub-string starting from provided index

	Args:
		line (str): string line
		begin_at (int): sub-str start point

	Raises:
		TypeError: Raise error if input is invalid or sub-string falls outside

	Returns:
		str: sub-string
	"""    	
	try: return line[begin_at:].strip()
	except: raise TypeError("Unrecognized Input")
# ------------------------------------------------------------------------------

def standardize_mac(mac):
	"""removes . or : from mac address and make it a standard

	Args:
		mac (str): mac address

	Returns:
		str: standard format of mac address
	"""    	
	return mac.replace(":","").replace(".","")

def mac_2digit_separated(mac):
	"""converts input mac to 2 digit separated mac format, separator=`:`

	Args:
		mac (str): mac address

	Returns:
		str: 2 digit separated format of mac address
	"""    	
	mac = standardize_mac(mac)
	for x in range(6):
		if x == 0:  s = mac[:2]
		else: s += ":" + mac[x*2:(x*2)+2]
	return s

def mac_4digit_separated(mac):
	"""converts input mac to 4 digit separated mac format, separator=`.`

	Args:
		mac (str): mac address

	Returns:
		str: 4 digit separated format of mac address
	"""    	
	mac = standardize_mac(mac)
	for x in range(3):
		if x == 0:   s  =       mac[:4]
		elif x == 1: s += "." + mac[4:8]
		elif x == 2: s += "." + mac[8:]
	return s

# ------------------------------------------------------------------------------
try:
	from collections import MutableMapping
except:
	from collections.abc import MutableMapping

def flatten(d, parent_key='', sep='_'):
	"""flattens the dictionary

	Args:
		d (dict): input can be multi-nested dictionary.
		parent_key (str, optional): key from previous dictionary to be prefixed with current keys. Defaults to ''.
		sep (str, optional): keys separator. Defaults to '_'.

	Returns:
		dict, list: dictionary of lists if input is dictinoary,  list with input dictionary if input is anything else
	"""    	
	items = []
	if isinstance(d, dict):
		for k, v in d.items():
			new_key = parent_key + sep + k if parent_key else k
			if isinstance(v, MutableMapping):
				items.extend(flatten(v, new_key, sep=sep).items())
			else:
				items.append((new_key, v))
		return dict(items)
	else: return [d]

def dataframe_generate(d):
	"""convert dicationary to dataframe. multi-level dictionary will be converted flattened first 
	inorder to convert to DataFrame.

	Args:
		d (dict): input can be multi-nested dictionary.

	Returns:
		DataFrame: pandas DataFrame
	"""    	
	new_d = {}
	for k, v in d.items():
		new_d[k] = flatten(v, "")
	return pd.DataFrame(new_d).fillna("").T
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------
def printmsg(pre=None, *, post=None, pre_ends="\n", justify_pre=True, justification_len=80):
	def outer(func):
		def inner(*args, **kwargs):
			if pre: 
				if justify_pre:
					print(pre.ljust(justification_len), end=pre_ends)
				else:
					print(pre, end=pre_ends)
			#
			fo = func(*args, **kwargs)
			#
			if post: 
				print(post)
			return fo
		return inner
	return outer

# ------------------------------------------------------------------------

def create_folders(folders, *, silent=True):
	"""Creates Folders

	Args:
		folders (list,str): folder(s)
		silent (bool, optional): Create without prompt. Defaults to True.

	Returns:
		bool: Success/Fail
	"""    	
	cf = 1
	if isinstance(folders, str):
		folders = [folders,]
	for folder in folders:
		if not os.path.exists(folder):
			if not silent: print(f"Creating: {folder}", end="\t")
			try:
				os.makedirs(folder)
				print("OK.")
			except:
				print("Failed.")
				cf = 0
	return bool(cf)


def open_text_file(file):
	"""Open Text file in Notepad.exe

	Args:
		file (str): file name
	"""    	
	sp.Popen(["notepad.exe", file])

def open_excel_file(file):
	"""Open Excel file in MS-Excel (excel.exe)

	Args:
		file (str): file

	Raises:
		Exception: Raise exception if unable to open excel.
	"""    	
	try:
		sp.Popen(["C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE", file])
	except:
		try:
			sp.Popen(["C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE", file])
		except Exception as e:
			raise Exception(f"Unable to Open file {file} in excel\n{e}")


def open_folder(folder):
	"""Open folder

	Args:
		file (str): file name
	"""    	
	path = os.path.realpath(folder)
	os.startfile(path)
