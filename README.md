# NavViewTemplate
Template for a Pythonista Navigation View app

The purpose of this app is to provide a simple template for any NavView style app using the iOS python app Pythonista.

As it stands the NavView has two levels: Groups and People. You can create as many Groups as you like and have as many People in each group as you like.

There is also a dumbie Settings page. This setting option is saved for persistence but does not control anything.

The UI is built with Pythonista's ui module. The logic uses a custom object orientated module called simple_module. The objects that are created are saved and loaded (for persistence) using the pickle module.

##Compatibility
This code is compatible with Python 2.7 and 3.5. Because of the pickle module protocol differences between the two versions of Python, you can not use the app with Python 3.5 and then switch back to Python 2.7. You can go from Python 2.7 to Python 3.5.


