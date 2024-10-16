

import json
import base64

def generate_structure(path,rules, structure=None):
	levels = path.split('.')

	if structure is None:
		structure = {}

	temp = structure

	for i, level in enumerate(levels):
		if i == len(levels) - 1:
			temp[level] = rules
		else:
			if level not in temp:
				temp[level] = {}
			temp = temp[level]

	return structure

def map_options(path,options, structure=None):

	levels = path.split('.')

	if structure is None:
		structure = {}

	temp = structure

	for i, level in enumerate(levels):
		if i == len(levels) - 1:
			temp[level] = options
		else:
			if level not in temp:
				temp[level] = {}
			temp = temp[level]

	return structure


def validate_schema(variable, schema,messages=None,options=None):

	if messages is None:
		messages = []

	if isinstance(schema, str):
		schema = json.loads(schema)

	for item in schema:
		if isinstance(schema[item],str):
	
			if item in variable:
				if not check.rules(variable[item],schema[item]):
					messages.append('{} is not valid'.format(item))
				
				if options is not None:
					if schema[item].find('options') != -1:
						if not variable[item] in options[item]:
							messages.append('{} is not valid'.format(item))


			else:
				if schema[item].find('required') != -1:
					messages.append('{} is required'.format(item))
			
		elif isinstance(schema[item],dict):
			if options is not None and item in options:
				messages = validate_schema(variable[item],schema[item],messages,options=options[item])
			else:
				messages = validate_schema(variable[item],schema[item],messages)

	return messages

def apply_filters_schema(variable, schema,messages=None):

	if isinstance(schema, str):
		schema = json.loads(schema)

	for item in schema:
		if isinstance(schema[item],str):
			if item in variable:
				variable[item] = filter(variable[item],schema[item])
			
		elif isinstance(schema[item],dict):
			apply_filters_schema(variable[item],schema[item])

	return variable

# Limpiar self.__data de valores que no esten en el schema
def clean_data(variable, schema):

	if isinstance(schema, str):
		schema = json.loads(schema)
	if isinstance(variable, str):
		variable = json.loads(variable)

	keys_to_delete = []

	for item in variable:
		if item not in schema:
			keys_to_delete.append(item)
		elif isinstance(variable[item], dict) and isinstance(schema[item], dict):
			variable[item] = clean_data(variable[item], schema[item])

	for key in keys_to_delete:
		del variable[key]

	return variable


def getValue(path,schema,absolute=''):
	levels = path.split('.')

	if absolute=='':
		absolute = schema

	for i, level in enumerate(levels):
		if i == len(levels) - 1:
			return absolute[level]
		else:
			if level not in absolute:
				return False
			absolute = absolute[level]

	return False


class InputRules:

	__data_struct = None
	__data_filters = None
	__data = None
	__errors = []
	__options = {}
	__options_struct = {}

	def __init__(self,data):
		self.__data = data

	def rules(self,field,rules,filters=None,options=None):

		if options is not None:
			self.__options[field] = options
			self.__options_struct = map_options(field,options)

		self.__data_struct = generate_structure(field,rules,self.__data_struct)
	
		if filters is not None:
			self.__data_filters = generate_structure(field,filters,self.__data_filters)

	def errors(self):
		return self.__errors

	def data(self):
		self.__data = apply_filters_schema(self.__data,self.__data_filters)
		return self.__data

	def schema(self):
		return jsontools.convertToJson(self.__data_struct)
	
	def verify(self):
		#print(jsontools.convertToJson(self.__data_struct))
		#print(jsontools.convertToJson(self.__data))

		if self.__options is not None:
			self.__errors = validate_schema(self.__data,self.__data_struct,options=self.__options_struct)
		else:
			self.__errors = validate_schema(self.__data,self.__data_struct)

		#Limpiar self.__data de valores que no esten en el schema
		self.__data = clean_data(self.__data,self.__data_struct)

		print("data...")
		print(jsontools.convertToJson(self.__data))
		print("data...")
		
		if len(self.__errors)>0:
			return False
		else:
			return True
		

class check:

	def rules(value,rules):

		rules_list = [
			'required',
			'options',
			'empty',
			'!empty',
			'!none',
			'none',
			'domain',
			'ip',
			'mail',
			'integer',
			'float',
			'numeric',
			'string',
			'uuid'

		]

		_check= True

		explode_rules = rules.split(',')

		for rule in explode_rules:

			if rule not in rules_list:
				raise ValueError('Rule {} not found'.format(rule))

			if rule=='uuid':
				if not check.uuid(value):
					_check= False

			if rule=='required' or rule=='options':
				continue

			if rule=='empty':
				if not check.empty(value):
					_check= False

			if rule=='!empty':
				if check.empty(value):
					_check= False

			if rule=='!none':
				if not check.notnone(value):
					_check= False

			if rule=='none':
				if not check.none(value):
					_check= False

			if rule=='domain':
				if not check.domain(value):
					_check= False

			if rule=='ip':
				if not check.ip(value):
					_check= False

			if rule=='mail':
				if not check.mail(value):
					_check= False

			if rule=='integer':
				if not check.integer(value):
					_check= False

			if rule=='float':
				if not check.float(value):
					_check= False

			if rule=='numeric':
				if not check.numeric(value):
					_check= False

			if rule=='string':
				if not check.string(value):
					_check= False

		return _check


	def sanitize_sql(user_input):
		user_input = re.sub(r"[\'\";--]", "", user_input)
		user_input = re.sub(r"\s+", " ", user_input)
		return user_input.strip()

	def notnone(value):
		if value is None:
			return False
		else:
			return True

	def none(value):
		if value is None:
			return True
		else:
			return False

	def uuid(value):
		if re.match(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", value):
			return True
		else:
			return False

	#Arrays
	def options(value,options):
		if value in options:
			return True
		else:
			return False

	#Contents
	def domain(value):
		return bool(re.match(r"^(?=.{1,255}$)[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z]{2,})+$", value))

	def ip(value):
		valid = bool(re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",value))

		if not valid:
			return False
		else:
			parts = value.split('.')
			for part in parts:
				if int(part)>255:
					return False

		return True

	def mail(value):
		# Improved regex for email validation
		if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
			return True
		else:
			return False

	'''
	def filename(value):
		return re.match("^[A-Za-z0-9\_\-\.]+$",value)
	'''

	#States

	def empty(value):

		if value is None:
			return True

		if value=='':
			return True

		elif check.numeric(value):
			value = filter(value,'int')
			if value < 1:
				return True
			else:
				return False
		elif check.string(value):
			if value=='':
				return True
			else:
				return False


	#types
	def string(value):
		if isinstance(value,str):
			return True
		else:
			return False

	def integer(value):
		if isinstance(value,int):
			return True
		else:
			return False

	def float(value):
		if isinstance(value,float):
			return True
		else:
			return False

	def numeric(value):
		if check.integer(value) or check.float(value):
			return True
		else:
			return False


def filter(value,rules):
	rules_list = [
		'xss',
		'sql',
		'str',
		'float',
		'int',
		'trim',
		'md5',
		'base64',
		'b64encode',
		'b64decode',
		'lower',
		'upper',
		'ucfirst',
		'ucwords',
		'json',
		'serialize',
		'unserialize',
		'urldecode',
		'urlencode',
		'htmlentities',
		'htmlspecialchars',
		'striptags',
		'strip',
		'stripslashes',
		'addslashes',
		'nl2br',
		'br2nl'

	]

	tmp = rules.split(',')

	for rule in tmp:

		if rule not in rules_list:
			raise ValueError('Filter {} not found'.format(rule))

		if rule=='int' or rule=='integer':
			try:
				value = int(value)
			except:
				raise ValueError('Value is not integer')
			continue

		if rule=='str' or rule=='string':
			if value is None:
				value = ''
				continue

			if isinstance(value,dict) or isinstance(value,list):
				raise ValueError('Value is not string')

			try:
				value = str(value)
			except:
				raise ValueError('Value is not string')
			continue

		if rule=='float':
			try:
				value = float(value)
			except:
				raise ValueError('Value is not float')
			continue

		if rule=='trim' or rule=='strip':
			value = value.strip()
			continue

		if rule=='md5':
			value = hashlib.md5(value.encode()).hexdigest()
			continue

		if rule=='base64' or rule=='b64encode':
			value = base64.b64encode(value.encode()).decode()
			continue

		if rule=='b64decode':
			value = base64.b64decode(value).decode()
			continue

		if rule=='lower':
			value = value.lower()
			continue

		if rule=='upper':
			value = value.upper()
			continue

		if rule=='ucfirst':
			value = value.capitalize()
			continue

		if rule=='ucwords':
			value = value.title()
			continue

		if rule=='json':
			value = json.dumps(value)
			continue

		if rule=='serialize':
			value = pickle.dumps(value)
			continue

		if rule=='unserialize':
			value = pickle.loads(value)
			continue

		if rule=='urldecode':
			value = urllib.parse.unquote(value)
			continue

		if rule=='urlencode':
			value = urllib.parse.quote(value)
			continue

		if rule=='htmlentities':
			value = html.escape(value)
			continue

		if rule=='htmlspecialchars':
			value = html.escape(value)
			continue

		if rule=='striptags':
			value = re.sub('<[^<]+?>', '', value)
			continue

		if rule=='stripslashes':
			value = value.replace('\\','')
			continue

		if rule=='addslashes':
			value = value.replace('"','\\"')
			continue

		if rule=='nl2br':
			value = value.replace('\n','<br>')
			continue

		if rule=='br2nl':
			value = value.replace('<br>','\n')
			continue
		if rule=='xss' or rule=="escape":
			value = html.escape(value)
			continue

		if rule=='sql':
			value = check.sanitize_sql(value)
			continue

	return value


class jsontools:

	def get(path,schema):
		levels = path.split('.')

		for i, level in enumerate(levels):
			if i == len(levels) - 1:
				return schema[level]
			else:
				if level not in schema:
					raise ValueError('Path not found')
				schema = schema[level]

		raise ValueError('Path not found')
				
	def get2(path,schema,absolute=''):
		levels = path.split('.')

		if absolute=='':
			absolute = schema

		for i, level in enumerate(levels):
			if i == len(levels) - 1:
				return absolute[level]
			else:
				if level not in absolute:
					return False
				absolute = absolute[level]

		return False
				
		
	def pretty(data):
		try:
			return json.dumps(json.loads(data),indent=1)
		except:
			return False

	def validate(data):
		try:
			json.loads(data)
		except ValueError as err:
			print(err)
			return False
		return True

	def convertJsonToList(data):
		try:
			return json.loads(data)
		except:
			return False

	def convertToJson(data):

		if isinstance(data,dict):

			for k, v in data.items():
				if k.find("'") !=-1 :
					k = k.replace("'","### single quote ###")

				if isinstance(v,str) and v.find("'") !=-1 :
					v = v.replace("'","### single quote ###")

				data[k]=v

			data = str(data)
			data = data.replace("'",'"')
			data = data.replace("### single quote ###","'")
			#data = data.replace('\\',"")

		try:
			return json.dumps(json.loads(data),indent=1)
		except ValueError as err:
			return False

	def open(filename):
		f = open(filename,"r")
		content = f.read()
		f.close()
		return jsontools.convertToJson(content)

	def save(content,filename):
		f = open(filename, "w")
		f.write(jsontools.pretty(content) +"\n")
		f.close()
