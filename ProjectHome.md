# We moved to Github please visit us there ! #

https://github.com/django-extensions/django-extensions

# Old Page #


This is a repository for collecting global custom management extensions for the Django Framework.

# Getting Started #
The easiest way to figure out what Django Extensions are all about is to watch the [excellent screencast](http://ericholscher.com/blog/2008/sep/12/screencast-django-command-extensions/) by Eric Holscher.  In a couple minutes Eric walks you through a half a dozen command extensions.

Once you've done that check out our InstallationInstructions. Enjoy.

# Updates #
  * _18-11-2009_: Disabled Issue tracking on code.google.com please use http://github.com/django-extensions/django-extensions/issues If you had issues that you would like to see resolved please open a new ticket for it at Github. Thanks!

  * _22-05-2009_: Release Django Extensions 0.4.1

  * _03-04-2009_: Release Django Extensions 0.4

  * **IMPORTANT** _30-03-2009_: We converted to using GIT for version control on GitHub. You can reach the url at: http://github.com/django-extensions/django-extensions/tree/master you can download a snapshot of the current version at http://github.com/django-extensions/django-extensions/tarball/master

  * **IMPORTANT** django-command-extensions has become django-extensions – We have renamed the project and the import point from extensions to django\_extensions. You will need to change the name **extensions** in your INSTALLED\_APPS to **django\_extensions**. The same goes for every other place that you might have imported from the extensions namespace.

# Current Command Extensions #

  * **create\_app** - creates an application directory structure for the specified app name.  This command allows you to specify the --template option where you can indicate a template directory structure to use as your default.

  * **create\_command** - creates a command extension directory structure within the specified application.  This makes it easy to get started with adding a command extension to your application.

  * **create\_jobs** - Creates a Django jobs command directory structure for the given app name in the current directory.  This is part of the impressive jobs system.

  * **create\_superuser** - makes it easy to create a superuser for the django.contrib.auth.

  * **describe\_form** - used to display a form definition for a model.  Copy and paste the contents into your forms.py and you're ready to go.

  * **dumpscript** - Generates a Python script that will repopulate the database using objects. The advantage of this approach is that it is easy to understand, and more flexible than directly populating the database, or using XML.

  * **[export\_emails](ExportEmails.md)** - export the email addresses for your users in one of many formats.  Currently supports Address, Google, Outlook, LinkedIn, and VCard formats.

  * **generate\_secret\_key** - creates a new secret key that you can put in your settings.py module.

  * **[graph\_models](GraphModels.md)** - creates a [GraphViz](http://www.graphviz.org/) dot file.  You need to send this output to a file yourself.  Great for graphing your models. Pass multiple application names to combine all the models into a single dot file.

  * **passwd** - makes it easy to reset a user's password

  * **print\_user\_for\_session** - print the user information for the provided session key. this is very helpful when trying to track down the person who experienced a site crash.

  * **reset\_db** - Resets a database (currently sqlite3, mysql, postgres).

  * **runjob** - run a single maintenance job.  Part of the jobs system.

  * **runjobs** - runs scheduled maintenance jobs. Specify hourly, daily, weekly, monthly.  Part of the jobs system.

  * **runprofileserver** - starts `runserver` with hotshot/profiling tools enabled.  I haven't had a chance to check this one out, but it looks really cool.

  * **runscript** - Runs a script in django context.

  * **[runserver\_plus](RunServerPlus.md)** - The standard runserver stuff but with the Werkzeug debugger baked in.  Requires Werkzeug (http://werkzeug.pocoo.org/).  This one kicks ass.

  * **set\_fake\_passwords** -  Sets all user passwords to a common value (`password` by default). DEBUG only

  * **shell\_plus** - An enhanced version of the Django shell.  It will autoload all your models making it easy to work with the ORM right away.

  * **show\_urls** - displays the url routes that are defined in your project.  Very crude at this point.

  * **sqldiff** - prints the (approximated) difference between an apps models and what is in the database.  This is very nice, but also very experimental at the moment.  It can not catch everything but it's a great sanity check.

# Current Database Model Field Extensions #

  * **AutoSlugField** - AutoSlugfield will automatically create a unique slug increasing an appended number on the slug until it is unique. Inspired by SmileyChris' Unique Slugify snippet.

  * **CreationDateTimeField** - DateTimeField that will automatically set it's date when the object is first saved to the database. Works in the same way as the deprecated auto\_now\_add keyword.

  * **ModificationDateTimeField** - DateTimeField that will automatically set it's date when an object is saved to the database. Works in the same way as the deprecated auto\_now keyword.

  * **UUIDField** - UUIDField for Django, supports all uuid versions which are natively supported by the uuid python module.

# Current Database Model Extensions #

  * **TimeStampedModel** - TimeStampedModel, An abstract base class model that provides self-managed "created" and "modified" fields.

  * **TitleSlugDescriptionModel** -TitleSlugDescriptionModel, An abstract base class model that has a "title" (CharField), "slug" (AutoSlugField) and a "description" (TextField) field.

# Current Admin Extensions #
  * **ForeignKeyAutocompleteAdmin** - ForeignKeyAutocompleteAdmin will enable the admin app to show ForeignKey fields with an search input field. The search field is rendered by the ForeignKeySearchInput form widget and uses jQuery to do configureable autocompletion.