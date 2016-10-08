class Group():
	def __init__(self, name, data1=None, data2=None, people=None):
		self.name = name
		self.data1 = data1
		self.data2 = data2
		# people is a list of People objects
		# [] convert None into an empty list
		self.people = people or []
	
	def get_name(self):
		"""
		Returns name as a string
		"""
		return self.name
		
	def get_data1(self):
		"""
		Returns data1
		"""
		return self.data1
		
	def get_data2(self):
		"""
		Returns data2
		"""
		return self.data2
		
	def get_people(self):
		"""
		Returns the list of Person objects.
		"""
		return self.people
		
	def add_person(self, person):
		"""
		Adds a Person object to the people list.
		"""
		self.people.append(person)
		
	def delete_person_by_name(self, name):
		"""
		Deletes the first person with the same name as the supplied variable.
		
		All names must be unique for this to work correctly.
		"""
		for person in self.people:
			if person.get_name() == name:
				self.people.remove(person)
				break
				
	def replace_person(self, position_in_list, updated_person):
		"""
		This replaces a person object with a new one,
		in the same position within the people list.
		"""
		self.people[position_in_list] = updated_person
		
		
class Person():
	def __init__(self, name, data1=None, data2=None):
		self.name = name
		self.data1 = data1
		self.data2 = data2
		
	def get_name(self):
		"""
		Returns person's name as string
		"""
		return self.name
		
	def get_data1(self):
		"""
		Returns data1
		"""
		return self.data1
		
	def get_data2(self):
		"""
		Returns data2
		"""
		return self.data2
