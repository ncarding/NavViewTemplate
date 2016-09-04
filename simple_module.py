class Group():
	def __init__(self, name, people = []):
		self.name = name
		# people is a list of People objects
		self.people = people
	
	def get_name(self):
		"""
		Returns name as a string
		"""
		return self.name
		
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
		
		
class Person():
	def __init__(self, name):
		self.name = name
		
	def get_name(self):
		"""
		Returns person's name as string
		"""
		return self.name
