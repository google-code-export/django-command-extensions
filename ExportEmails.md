Most Django sites include a registered user base. There are times when you would like to import these e-mail addresses into other systems (generic mail program, GMail, google docs _invites, give edit permissions_, LinkedLn Group pre-approved listing). The export\_emails command extension gives you this ability. The users exported can be filtered by Group name association.

## Example Usage ##

```
# Export all the addresses in the '"First Last" <my@addr.com>;' format.
$ ./manage.py export_emails > addresses.txt
```
```
# Export users from the group 'Attendees' in the linked in pre-approve Group csv format.
$ ./manage.py export_emails -g Attendees -f linkedin pycon08.csv
```
```
# Create a csv file importable by GMail or Google Docs
$ ./manage.py export_emails --format=google google.csv
```

## Current Supported Formats ##

### address ###
This is the default basic text format. Each entry is on its own line in the format:
```
"First Last" <user@host.com>;
```

This can be used with all known mail programs (that I know about anyway).

### google ###
A CSV (comma separated value) format which google applications can import. This can be used to import directly into GMail, a GMail mailing group, Google Docs invite (to read), Google Docs grant edit permissions, Google Calendar invites, etc, etc, etc.

Only two columns are supplied. One for the persons name and the e-mail address.
This is also nice for importing into spreadsheets.

### outlook ###
A CSV (comma separated value) format which outlook can parse and import.

Supplies all the columns that Outlook 'requires', but only the name and e-mail address are supplied.

### linkedin ###
A CSV (comma separated value) format which can be imported by [LinkedIn Groups](http://www.linkedin.com/static?key=groups_info) to pre-approve a list of people for joining the group.

This supplies 3 columns: First name, last name, and e-mail address. This is the best generic csv file for importing into spreadsheets as well.

### vcard ###
A vCard format which Apple Address Book can parse and import.