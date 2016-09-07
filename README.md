# NavViewTemplate
Template for a Pythonista Navigation View app

The purpose of this app is to provide a simple template for any NavView style app using the iOS python app Pythonista.

As it stands the NavView has two levels: Groups and People. You can create as many Groups as you like and have as many People in each group as you like.

There is also a dumbie Settings page. This setting option is saved for persistence but does not control anything.

The UI is built with Pythonista's ui module. The logic uses a custom object orientated module called simple_module. The objects that are created are saved and loaded (for persistence) using the pickle module. 

# Known Issue
The People lists should be independent of the Group lists, but at the moment they are not.

If you add a new Group then add one or more People to that group and then add a second Group, the People from the first Group are automatically added to the second and any additional Groups. 

I can't tell where the bug is but it only effects Groups created with each launch of the app. E.g. If you create three Groups they will all contain the same People. If you then quit the app and relaunch it those people will still be in each Group but if you create more Groups they will not contain the original list of People. These new Groups will however all share any new People added to any of the Groups created in this session.
