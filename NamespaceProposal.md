# Introduction #

Please change / write your proposal for splitting django\_extensions into namespaces here.

# Proposal of a Namespace #

Rough proposal for splitting into functional parts:
  * django\_extensions.commands (20% that everbody uses / production)
  * django\_extensions.commands.development (everything development)
  * django\_extensions.commands.extra (not fitting about category's?)
  * django\_extensions.db
  * django\_extensions.templates
  * django\_extensions.jobs

The db part should be okey where it is right now. Cause it's only used
when somebody explicitly imports:
> from django\_extensions.db.models import something

