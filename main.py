# coding: utf-8
# Initially based on code by the Tutorial Doctor 1/29/16

import ui
import simple_module
import cPickle as pickle
import dialogs
import os


class User_Interface():
	def __init__(self):
		self.groups_list = []
		self.selected_group_row = -1
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
		saved_items = self.open_file('ios_persistance.pkl')
		# Iterate through saved_items generator and add the contents to the
		# groups_list.
		for item in saved_items:
			self.groups_list.append(item)
		# Do the same for Settings
		# This is a slight duplicate of code but self.open_file didn't quite work.
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
				'accessory_type': 'disclosure_indicator'})
		self.groups_listsource = ui.ListDataSource(table_items)
		self.root_table.data_source = self.groups_listsource
		self.root_table.delegate = self.groups_listsource
		self.groups_listsource.action = self.group_list_action
		self.groups_listsource.edit_action = self.groups_edit_action
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
	def open_file(self, filename):
		"""
		Opens Pickle file and extracts all the objects into a list
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
	
	def connect(self, sender, title, view_name):
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
	
	def groups_btn_action(self, sender):
		"""
		Called when a button in the Group view is selected.
		"""
		self.connect(sender, 'Settings', 'settings_group')
		self.connect(sender, 'Add', 'add_group')
		
	def people_btn_action(self, sender):
		"""
		Called when a button in the People view is selected.
		"""
		self.connect(sender, 'Add', 'add_person')
		
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
		
	def group_save_action(self, sender):
		"""
		Adds a new group to the listsource and creates a new
		simple_module Group object.
		Also saves the Group list to a pickle file.
		"""
		v = sender.superview
		name = v['name_textfield'].text
		# check name is unique. This is essential because of the way i have
		# had to implement the deleting of a list item from the object list.
		self.unique_name(name, 'group')
		# Add item to the listsource
		self.groups_listsource.items.append({
			'title': name,
			'accessory_type': 'disclosure_indicator'})
		# create a new Group object and add it to the group object list
		self.groups_list.append(simple_module.Group(name))
		print self.groups_list
		self.save_file('ios_persistance.pkl', self.groups_list)
		v.close()
		
	def people_save_action(self, sender):
		"""
		Adds a new person to the listsource and creates a new
		simple_module Person object.
		Also saves the Group list to a pickle file.
		"""
		v = sender.superview
		name = v['name_textfield'].text
		# Check name is unique. This is essential because of the way I have
		# had to implement the deleting of a list item from the object list.
		self.unique_name(name, 'people')
		# Add item to the listsource
		self.people_listsource.items.append({'title': name})
		# Create a new Person object and add it to the people list
		# of the selected group
		new_person = simple_module.Person(name)
		self.groups_list[self.selected_group_row].add_person(new_person)
		self.save_file('ios_persistance.pkl', self.groups_list)
		v.close()
		
	def settings_save_action(self, sender):
		"""
		Saves the usees Settings preferences to a pickle file.
		"""
		v = sender.superview
		setting_01 = v['setting_01_switch'].value
		# replace setting's dict
		self.settings = {'setting_01': setting_01}
		with open('settings.pkl', 'wb') as output:
			pickle.dump(self.settings, output, pickle.HIGHEST_PROTOCOL)
		v.close()
	
	def cancel_action(self, sender):
		"""
		Closes the current view.
		"""
		v = sender.superview
		v.close()
		
	def group_list_action(self, sender):
		"""
		Executes when a list item is selected  in the Group list view.
		"""
		self.selected_group_row = sender.selected_row
		print self.selected_group_row
		self.root_view.navigation_view.push_view(self.people_pushed_view)
		# add buttons to Nav View
		add_person_btn = ui.ButtonItem('Add', None, self.people_btn_action)
		self.people_pushed_view.right_button_items = [add_person_btn]
		
		people_list = self.groups_list[self.selected_group_row].get_people()
		people_items = []
		for person in people_list:
			name = person.get_name()
			people_items.append({'title': name})
		# You can use a list or a class as the data source for the tableview
		self.people_listsource = ui.ListDataSource(people_items)
		self.people_table.data_source = self.people_listsource
		self.people_table.delegate = self.people_listsource
		self.people_listsource.edit_action = self.people_edit_action
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
			item_titles = []
			for item in sender.items:
				item_titles.append(item['title'])
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
			item_titles = []
			for item in sender.items:
				item_titles.append(item['title'])
			for person in local_people_list:
				persons_name = person.get_name()
				if persons_name not in item_titles:
					selected_group.delete_person_by_name(persons_name)
		self.save_file('ios_persistance.pkl', self.groups_list)
	

User_Interface()
