# coding: utf-8
"""
This is a simple template for a Pythonista UI NavView app.
It includes an object orientated module that enables you to collate, store,
populate and manipulate whatever data you care to collect.
"""
# Code by Neil Carding https://github.com/ncarding/NavViewTemplate/
# Initially based on code by the Tutorial Doctor 1/29/16

import dialogs
import os
import ui

try:
	# Python 2
	import cPickle as pickle
except ImportError:
	# Python 3
	import pickle

import simple_module


class User_Interface():
	def __init__(self):
		self.groups_list = []
		self.selected_group_row = -1
		self.selected_accessory_row = -1
		self.settings = {'setting_01': True}
		self.setup()
	
	def setup(self):
		"""
		This extracts saved (persistence) data from pickle files.
		Then it creates all the different Views ready to be called.
		And then it creates the initial user interface.
		"""
		# IMPLEMENT PERSISTANCE
		# Open saved file and extract Group objects.
		# THIS MUST BE CALLED BEFORE THE TABLE ITEMS ARE EXTRACTED!!
		# File path is hard coded for iOS version).
		# This creates a 'generator'.
		saved_items = self.read_file('ios_persistance.pkl')
		# Iterate through saved_items generator and add the contents to the
		# groups_list.
		for item in saved_items:
			self.groups_list.append(item)
		# Do the same for Settings
		# This is a slight duplicate of code but self.read_file didn't quite work.
		if os.path.isfile('settings.pkl'):
			with open('settings.pkl', 'rb') as output:
				self.settings = pickle.load(output)
			
		# SETUP ROOT VIEW (Groups)
		self.root_view = ui.View()
		self.root_view.name = 'Groups'
		self.root_view.background_color = 'white'
		self.root_table = ui.TableView()
		self.root_table.flex = 'WH'
		# Define content items list
		table_items = []
		# Extract items from groups_list
		for group in self.groups_list:
			group_name = group.get_name()
			table_items.append({
				'title': group_name,
				'accessory_type': 'detail_disclosure_button'})
		self.groups_listsource = ui.ListDataSource(table_items)
		self.root_table.data_source = self.groups_listsource
		self.root_table.delegate = self.groups_listsource
		self.groups_listsource.action = self.group_list_action
		self.groups_listsource.edit_action = self.groups_edit_action
		self.groups_listsource.accessory_action = self.group_accessory_action
		self.root_view.add_subview(self.root_table)
		
		# SETUP PEOPLE VIEW
		self.people_pushed_view = ui.load_view('people_view')
		self.people_table = self.people_pushed_view['tableview1']
		
		# IMPLEMENT UI
		# Create button objects with the format
		edit_group_btn = ui.ButtonItem('Settings', None, self.groups_btn_action)
		add_group_btn = ui.ButtonItem('Add', None, self.groups_btn_action)
		# Apply buttons to view
		self.root_view.left_button_items = [edit_group_btn]
		self.root_view.right_button_items = [add_group_btn]
		# Create and present NavigationView
		nav_view = ui.NavigationView(self.root_view)
		nav_view.present()

	# FUNCTIONS
	def read_file(self, filename):
		"""
		Reads Pickle file and extracts all the objects into a list
		"""
		if os.path.isfile(filename):
			with open(filename, "rb") as input:
				while True:
					try:
						yield pickle.load(input)
					except EOFError:
						break
	
	def save_file(self, filename, object_list):
		"""
		Saves the  list of objects to a Pickle file
		"""
		with open(filename, 'wb') as output:
			for object in object_list:
				pickle.dump(object, output, pickle.HIGHEST_PROTOCOL)
	
	def connect_btns(self, sender, title, view_name):
		"""
		Connects ui buttons in xxx_btn_action methods to the relevant view.
		"""
		if sender.title == title:
			view_to_present = view_name
			view = ui.load_view(view_to_present)
			if title == 'Settings':
				# Default values for Settings View.
				self.settings_values(view)
			view.present()
			
	def selected_group_obj(self, index):
		"""
		Returns the Group object for the currently selected group.
		"""
		return self.groups_list[index]
		
	def selected_person_obj(self):
		"""
		Returns the person object for the currently selected person.
		"""
		people = self.selected_group_obj(self.selected_group_row).get_people()
		return people[self.selected_accessory_row]
	
	def groups_btn_action(self, sender):
		"""
		Called when a button in the Group view is selected.
		"""
		self.connect_btns(sender, 'Settings', 'settings_group')
		self.connect_btns(sender, 'Add', 'group')
		
	def people_btn_action(self, sender):
		"""
		Called when a button in the People view is selected.
		"""
		self.connect_btns(sender, 'Add', 'person')

	def set_group_values(self, view, index):
		"""
		Populates the fields in the Group form ui ready for editing.
		"""
		group = self.selected_group_obj(index)
		name = group.get_name()
		data1 = group.get_data1()
		data2 = group.get_data2()
		view['name_textfield'].text = name
		if data1:
			view['data1_textfield'].text = data1
		if data2:
			view['data2_textfield'].text = data2
		
	def set_person_values(self, view):
		"""
		Populates the fields in the person form ui ready for editing.
		"""
		person = self.selected_person_obj()
		name = person.get_name()
		data1 = person.get_data1()
		data2 = person.get_data2()
		view['name_textfield'].text = name
		if data1:
			view['data1_textfield'].text = data1
		if data2:
			view['data2_textfield'].text = data2
	
	def get_group_values(self, view):
		"""
		Extracts values from the Group form fields and returns them as a tuple.
		"""
		name = view['name_textfield'].text
		data1 = view['data1_textfield'].text
		data2 = view['data2_textfield'].text
		return name, data1, data2
		
	def get_person_values(self, view):
		"""
		Extracts values from the person form fields and returns them as a tuple.
		"""
		name = view['name_textfield'].text
		data1 = view['data1_textfield'].text
		data2 = view['data2_textfield'].text
		return name, data1, data2

	def settings_values(self, view):
		"""
		Populates the form fields in the Settings view with their current values.
		"""
		# Set setting_01 state from self.settings dict
		setting_01 = self.settings['setting_01']
		view['setting_01_switch'].value = setting_01
				
	def unique_name(self, name, origin):
		"""
		Checks to see if supplied name is already used in origin list.
		If it is an alert dialog box is displayed.
		
		This is required as the method of deleting objects when a list item
		is deleted only works if all the list titles are unique.
		"""
		if origin == 'people':
			object_list = self.groups_list[self.selected_group_row].get_people()
		elif origin == 'group':
			object_list = self.groups_list
			
		for object in object_list:
			if name == object.get_name():
				dialogs.alert('Please use a unique name')
		
	def group_save_action(self, sender, update=False):
		"""
		Adds a new group to the listsource and creates a new
		simple_module Group object.
		Also saves the Group list to a pickle file.
		"""
		view = sender.superview
		name, data1, data2 = self.get_group_values(view)
		# check name is unique. This is essential because of the way i have
		# had to implement the deleting of a list item from the object list.
		self.unique_name(name, 'group')
		# check name_textfield contains a value
		if name:
			# Create a new Group object
			new_group = simple_module.Group(name, data1, data2)
			# Check to see if this is a new person or an updated group
			if update is True:
				# If it's updated replace existing group with new one.
				self.groups_list[self.selected_accessory_row] = new_group
			else:
				# Add item to the listsource
				self.groups_listsource.items.append({
					'title': name,
					'accessory_type': 'detail_disclosure_button'})
				# create a new Group object and add it to the group object list
				self.groups_list.append(
					simple_module.Group(name, data1, data2)
					)
			self.save_file('ios_persistance.pkl', self.groups_list)
			view.close()
		else:
			dialogs.alert('Please enter a unique name')
			
	def person_save_action(self, sender, update=False):
		"""
		Adds a new person to the listsource and creates a new MS Person object.
		Also saves the Group list to a pickle file.
		"""
		view = sender.superview
		name, data1, data2 = self.get_person_values(view)
		# Check name is unique. This is essential because of the way I have
		# had to implement the deleting of a list item from the object list.
		self.unique_name(name, 'people')
		# check name_textfield contains a value
		if name:
			# Create a new Person object and add it to the people list
			# of the selected group
			new_person = simple_module.Person(name, data1, data2)
			# Check to see if this is a new person or an updated person
			if update is True:
				self.selected_group_obj(self.selected_group_row).replace_person(
					self.selected_accessory_row, new_person)
			else:
				# Add item to the listsource
				self.people_listsource.items.append({
					'title': name,
					'accessory_type': 'detail_button'})
				self.selected_group_obj(self.selected_group_row).add_person(new_person)
			self.save_file('ios_persistance.pkl', self.groups_list)
			view.close()
		else:
			# If name field has been left blank open dialog box.
			dialogs.alert('Please enter a unique name')
		
	def settings_save_action(self, sender):
		"""
		Saves the usees Settings preferences to a pickle file.
		"""
		view = sender.superview
		setting_01 = view['setting_01_switch'].value
		# replace setting's dict
		self.settings = {'setting_01': setting_01}
		with open('settings.pkl', 'wb') as output:
			pickle.dump(self.settings, output, pickle.HIGHEST_PROTOCOL)
		view.close()
		
	def group_update_action(self, sender):
		"""
		Called when Group view is saved after editing.
		"""
		view = sender.superview
		group = self.selected_group_obj(self.selected_group_row)
		original_name = group.get_name()
		# Set variables for each field in the group form
		name, data1, data2 = self.get_group_values(view)
		# If it hadn't changed we can skip checking if it exists or is
		# unique, which is done in person_save_action()
		if name == original_name:
			
			# Create a new Group object and replace the old one.
			# Need to include existing People list.
			people_list = group.get_people()
			new_group = simple_module.Group(name, data1, data2, people_list)
			self.groups_list[self.selected_accessory_row] = new_group
			self.save_file('ios_persistance.pkl', self.groups_list)
			view.close()
		else:
			# If the name has changed update the groups_listsource
			# and let person_save_action() do the rest.
			self.groups_listsource.items[self.selected_accessory_row]['title'] = name
			self.groups_listsource.reload()
			self.group_save_action(sender, update=True)
	
	def person_update_action(self, sender):
		"""
		Called when 'person' view is saved after editing.
		"""
		view = sender.superview
		person = self.selected_person_obj()
		original_name = person.get_name()
		# Set variables for each field in the person form
		name, data1, data2 = self.get_person_values(view)
		# If it hadn't changed we can skip checking if it exists or is
		# unique, which is done in person_save_action()
		if name == original_name:
			
			# Create a new Person object and replace the old one with it
			# for the selected group.
			new_person = simple_module.Person(name, data1, data2)
			self.selected_group_obj(self.selected_group_row).replace_person(
				self.selected_accessory_row, new_person)
			self.save_file('ios_persistance.pkl', self.groups_list)
			view.close()
		else:
			# If the name has changed update the people_listsource
			# and let person_save_action() do the rest.
			self.people_listsource.items[self.selected_accessory_row]['title'] = name
			self.people_listsource.reload()
			self.person_save_action(sender, update=True)
	
	def cancel_action(self, sender):
		"""
		Closes the current view.
		"""
		view = sender.superview
		view.close()
		
	def group_list_action(self, sender):
		"""
		Executes when a list item is selected  in the Group list view.
		"""
		self.selected_group_row = sender.selected_row
		self.root_view.navigation_view.push_view(self.people_pushed_view)
		# add buttons to Nav View
		add_person_btn = ui.ButtonItem('Add', None, self.people_btn_action)
		self.people_pushed_view.right_button_items = [add_person_btn]
		
		people_list = self.groups_list[self.selected_group_row].get_people()
		people_items = []
		for person in people_list:
			name = person.get_name()
			people_items.append({
					'title': name,
					'accessory_type': 'detail_button'})
		# You can use a list or a class as the data source for the tableview
		self.people_listsource = ui.ListDataSource(people_items)
		self.people_table.data_source = self.people_listsource
		self.people_table.delegate = self.people_listsource
		self.people_listsource.edit_action = self.people_edit_action
		self.people_listsource.accessory_action = self.people_accessory_action
		self.people_table.reload()
	
	def groups_edit_action(self, sender):
		"""
		Called when the Groups list view is edited.
		This would be if a list item is deleted or moved up or down the list.
		"""
		# Check to see if edit action is a deleted row (as opposed to reordering)
		# Because listdatasource doesn't return the deleted row index we have
		# to do a bit of work to find out which item has been deleted.
		# THIS ONLY WORKS IF THE ITEM TITLES ARE UNIQUE.
		# SET UP FOR GROUP LIST ONLY. ADAPT FOR ANY LIST
		if len(sender.items) == len(self.groups_list) - 1:
			item_titles = [item['title'] for item in sender.items]
			for group in self.groups_list:
				if group.get_name() not in item_titles:
					self.groups_list.remove(group)
					break
		self.save_file('ios_persistance.pkl', self.groups_list)
	
	def people_edit_action(self, sender):
		"""
		Called when the People list view is edited.
		This would be if a list item is deleted or moved up or down the list.
		"""
		# check to see if edit action is a deleted row (as opposed to reordering)
		# Because listdatasource doesn't return the deleted row index we have
		# to do a bit of work to find out which item has been deleted.
		# THIS ONLY WORKS IF THE ITEM TITLES ARE UNIQUE.
		# SET UP FOR PEOPLE LIST ONLY. ADAPT FOR ANY LIST
		selected_group = self.groups_list[self.selected_group_row]
		local_people_list = selected_group.get_people()
		
		if len(sender.items) == len(local_people_list) - 1:
			item_titles = [item['title'] for item in sender.items]
			for person in local_people_list:
				persons_name = person.get_name()
				if persons_name not in item_titles:
					selected_group.delete_person_by_name(persons_name)
		self.save_file('ios_persistance.pkl', self.groups_list)
		
	def group_accessory_action(self, sender):
		"""
		Called when an info button is tapped in one of the group list cells.
		Sender is the ListDataSource object.
		"""
		# Define selected_accessory_row for later use.
		self.selected_accessory_row = sender.tapped_accessory_row
		# Open the 'person' ui view
		view = ui.load_view('group')
		# Populate view data fields
		self.set_group_values(view, self.selected_accessory_row)
		# Override the save button action. Default is self.person_save_action
		view['save_button'].action = self.group_update_action
		view.present()
	
	def people_accessory_action(self, sender):
		"""
		Called when an info button is tapped in one of the people list cells.
		Sender is the ListDataSource object.
		"""
		# Define selected_accessory_row for later use.
		self.selected_accessory_row = sender.tapped_accessory_row
		# Open the 'person' ui view
		view = ui.load_view('person')
		# Populate view data fields
		self.set_person_values(view)
		# Override the save button action. Default is self.person_save_action
		view['save_button'].action = self.person_update_action
		view.present()
	

User_Interface()
