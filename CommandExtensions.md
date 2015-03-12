# Current Command Extensions #

  * **create\_app** - creates an application directory structure for the specified app name.  This command allows you to specify the --template option where you can indicate a template directory structure to use as your default.

  * **create\_command** - creates a command extension directory structure within the specified application.  This makes it easy to get started with adding a command extension to your application.

  * **create\_jobs** - Creates a Django jobs command directory structure for the given app name in the current directory.  This is part of the impressive jobs system.

  * **create\_superuser** - makes it easy to create a superuser for the django.contrib.auth.

  * **describe\_form** - used to display a form definition for a model.  Copy and paste the contents into your forms.py and you're ready to go.

  * **[dumpscript](Dumpscript.md)** - Generates a Python script that will repopulate the database using objects. The advantage of this approach is that it is easy to understand, and more flexible than directly populating the database, or using XML.

  * **[export\_emails](ExportEmails.md)** - export the email addresses for your users in one of many formats.  Currently supports Address, Google, Outlook, LinkedIn, and VCard formats.

  * **generate\_secret\_key** - creates a new secret key that you can put in your settings.py module.

  * **[graph\_models](GraphModels.md)** - creates a [GraphViz](http://www.graphviz.org/) dot file.  You need to send this output to a file yourself.  Great for graphing your models. Pass multiple application names to combine all the models into a single dot file.

  * **mail\_debug** - starts a mail server which echos out the contents of the email instead of sending it.

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

  * **[sync\_media\_s3](sync_media_s3.md)** - copies files found in settings.MEDIA\_ROOT to S3.  Optionally can also gzip CSS and Javascript files and set the Content-Encoding header, and also set a far future expires header for browser caching.