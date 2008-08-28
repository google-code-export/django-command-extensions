"""
sqldiff.py - Prints the (approximated) difference between models and database

TODO:
 - seperate out PostgreSQL specific introspection hacks, to facilitate easier
   writing backend specific code. (like the constrains check's)
 - general cleanup
 - better support for relations
 - test with other backends then postgresql.
"""

from django.core.management.base import AppCommand
from django.db import transaction
from optparse import make_option

MESSAGE = """# Following is a list of differences between installed models and the database.
# It indicates how columns in the database are different from sql generated
# by Django for commands like syncdb, sql, sqlreset, etc.
#
# This list is an indication only and not meant to be fully complete
# or correct! Finding differences 'automaticly' is by no means easy and
# experience may very greatly between database backends."""

class Command(AppCommand):
    option_list = AppCommand.option_list + (
        make_option('--all-applications', '-a', action='store_true', dest='all_applications',
                    help="Automaticly include all application from INSTALLED_APPS."),
        make_option('--not-only-existing', '-e', action='store_false', dest='only_existing',
                    help="Check all tables that exist in the database, not only tables that should exist based on models."),
        make_option('--dense-output', '-d', action='store_true', dest='dense_output',
                    help="Shows the output in dense format, normally output is spreaded over multiple lines."),
        make_option('--output_sql', '-s', action='store_true', dest='sql',
                    help="Outputs the differences as SQL when available"),
    )
    
    help = "Prints the (approximated) difference between models and SQL fields in the database for the given app name(s)."

    output_transaction = False

    def handle(self, *app_labels, **options):
        if options.get('all_applications', False) and not app_labels:
            from django.db import models
            app_labels = [app.__name__.split('.')[-2] for app in models.get_apps()]
        print self.style.ERROR_OUTPUT(MESSAGE)
        super(Command, self).handle(*app_labels, **options)

    def handle_app(self, app, **options):
        from django.conf import settings
        self.is_pgsql = settings.DATABASE_ENGINE.startswith("postgresql")
        self.is_sqlite = settings.DATABASE_ENGINE.startswith("sqlite")
        self.handle_diff(app, **options)
    
    @transaction.commit_manually
    def handle_diff(self, app, **options):
        from django.db import models, connection
        from django.core.management import sql as _sql
        
        app_name = app.__name__.split('.')[-2]
        
	try:
	    django_tables = connection.introspection.django_table_names(only_existing=options.get('only_existing', True))
	except AttributeError:
	    # backwards compatibility for before introspection refactoring (r8296)
    	    try:
        	django_tables = _sql.django_table_names(only_existing=options.get('only_existing', True))
    	    except AttributeError:
        	# backwards compatibility for before svn r7568 
    	        django_tables = _sql.django_table_list(only_existing=options.get('only_existing', True))
        django_tables = [django_table for django_table in django_tables if django_table.startswith(app_name)]
        
        app_models = models.get_models(app)
        if not app_models:
            return
        
	try:
	    from django.db import get_introspection_module
            introspection_module = get_introspection_module()
	except ImportError:
	    introspection_module = connection.introspection
	
        cursor = connection.cursor()
        model_diffs = []
        for app_model in app_models:
            _constraints = None
            _meta = app_model._meta
            table_name = _meta.db_table
            
            table_indexes = introspection_module.get_indexes(cursor, table_name)

            
            fieldmap = dict([(field.get_attname(), field) for field in _meta.fields])
            try:
                table_description = introspection_module.get_table_description(cursor, table_name)
            except Exception, e:
                model_diffs.append((app_model.__name__, [str(e).strip()]))
                transaction.rollback() # reset transaction
                continue
            diffs = []
            for i, row in enumerate(table_description):
                att_name = row[0].lower()
		try:
        	    db_field_reverse_type = introspection_module.data_types_reverse[row[1]]
		except AttributeError:
		    # backwards compatibility for before introspection refactoring (r8296)
		    db_field_reverse_type = introspection_module.DATA_TYPES_REVERSE.get(row[1])
                kwargs = {}
		if isinstance(db_field_reverse_type, tuple):
		    kwargs.update(db_field_reverse_type[1])
		    db_field_reverse_type = db_field_reverse_type[0]
                
                if row[3]:
                    kwargs['max_length'] = row[3]
                if row[4]:
                    kwargs['max_digits'] = row[4]
                if row[5]:
                    kwargs['decimal_places'] = row[5]
                if row[6]:
                    kwargs['blank'] = True
                    if not db_field_reverse_type in ('TextField', 'CharField'):
                        kwargs['null'] = True
                if fieldmap.has_key(att_name):
                    field = fieldmap.pop(att_name)
                    # check type
                    def clean(s):
                        s = s.split(" ")[0]
                        s = s.split("(")[0]
                        return s
                    def cmp_or_serialcmp(x, y):
                        result = x==y
                        if result:
                            return result
                        is_serial = lambda x,y: x.startswith("serial") and y.startswith("integer")
                        strip_serial = lambda x: x.lstrip("serial").lstrip("integer")
                        serial_logic = is_serial(x, y) or is_serial(y, x)
                        if result==False and serial_logic:
                            # use alternate serial logic
                            result = strip_serial(x)==strip_serial(y)
                        return result
                    db_field_type = getattr(models, db_field_reverse_type)(**kwargs).db_type()
                    model_type = field.db_type()
                    # check if we can for constraints (only enabled on postgresql atm)
                    if self.is_pgsql:
                        if _constraints==None:
                            sql = """
                            SELECT
                                pg_constraint.conname, pg_get_constraintdef(pg_constraint.oid)
                            FROM
                                pg_constraint, pg_attribute
                            WHERE
                                pg_constraint.conrelid = pg_attribute.attrelid
                                AND pg_attribute.attnum = any(pg_constraint.conkey)
                                AND pg_constraint.conname ~ %s"""
                            cursor.execute(sql, [table_name])
                            _constraints = [r for r in cursor.fetchall() if r[0].endswith("_check")]
                        for r_name, r_check in _constraints:
                            if table_name+"_"+att_name==r_name.rsplit("_check")[0]:
                                r_check = r_check.replace("((", "(").replace("))", ")")
                                pos = r_check.find("(")
                                r_check = "%s\"%s" % (r_check[:pos+1], r_check[pos+1:])
                                pos = pos+r_check[pos:].find(" ")
                                r_check = "%s\" %s" % (r_check[:pos], r_check[pos+1:])
                                db_field_type += " "+r_check
                    else:
                        # remove constraints
                        model_type = model_type.split("CHECK")[0].strip()
                    c_db_field_type = clean(db_field_type)
                    c_model_type = clean(model_type)
                    if not cmp_or_serialcmp(c_model_type, c_db_field_type):
                        diffs.append({
                            'text' : "field '%s' not of same type: db=%s, model=%s" % (att_name, c_db_field_type, c_model_type),
                            'type' : 'type',
                            'data' : (table_name, att_name, c_db_field_type, c_model_type)
                        })
                        continue
                    if not cmp_or_serialcmp(db_field_type, model_type):
                        diffs.append({
                            'text' : "field '%s' parameters differ: db=%s, model=%s" % (att_name, db_field_type, model_type),
                            'type' : 'param',
                            'data' : (table_name, att_name, db_field_type, model_type)
                        })
                        continue
                else:
                    diffs.append({
                        'text' : "field '%s' missing in model field" % att_name,
                        'type' : 'missing-in-model',
                        'data' : (table_name, att_name, db_field_type, model_type)
                    })
            for field in _meta.fields:
                if field.db_index:
                    if not field.attname in table_indexes and not field.unique:
                        diffs.append({
                            'text' : "field '%s' INDEX defined in model missing in database" % (field.attname),
                        })
            if fieldmap:
                for att_name, field in fieldmap.items():
                    diffs.append({
                        'text' : "field '%s' missing in database" % att_name,
                        'type' : 'missing-in-db',
                        'data' : (table_name, att_name, field.db_type())
                    })
            if diffs:
                model_diffs.append((app_model.__name__, diffs))
        if model_diffs:
            NOTICE = self.style.NOTICE
            ERROR_OUTPUT = self.style.ERROR_OUTPUT
            SQL_TABLE = self.style.SQL_TABLE
            SQL_FIELD = self.style.SQL_FIELD
            SQL_COLTYPE = self.style.SQL_COLTYPE
            SQL_KEYWORD = self.style.SQL_KEYWORD
            modify_command = self.is_pgsql and "TYPE" or "MODIFY"
            
            if options.get('sql', False):
                lines = ["", SQL_KEYWORD("BEGIN;")]
                
                for model_name, diffs in model_diffs:
                    for diff in diffs:
                        if not diff: continue
                        if not diff.get('data', False): continue
                        
                        if self.is_sqlite and diff['type'] == 'param':
                                lines.append(NOTICE('-- %s' % diff['text']))
                                lines.append(NOTICE('-- SQLite does not feature type alteration on columns'))
                                continue
                        lines.append('%s %s' % (SQL_KEYWORD('ALTER TABLE'), SQL_TABLE(diff['data'][0])) )
                        if diff['type'] == 'missing-in-db':
                            lines.append('\t%s %s %s;' %  (SQL_KEYWORD('ADD'), SQL_FIELD(diff['data'][1]), SQL_COLTYPE(diff['data'][2]),) )
                        if diff['type'] == 'missing-in-model':
                            lines.append('\t%s %s;' % (SQL_KEYWORD('DROP COLUMN') , SQL_FIELD(diff['data'][1]) ))
                        if diff['type'] in ['type', 'param']:
                            lines.append('\t%s %s %s %s;' % (SQL_KEYWORD('ALTER'), SQL_FIELD(diff['data'][1]), SQL_KEYWORD(modify_command), SQL_COLTYPE(diff['data'][3])))                  
                lines.append(SQL_KEYWORD("COMMIT;"))
                
                print "\n".join(lines)
            else:
                dense = options.get('dense_output', False)
                if not dense:
                    print ""
                    print NOTICE("+ Application:"), SQL_TABLE(app_name)
                for model_name, diffs in model_diffs:
                    if not diffs: continue
                    if not dense:
                        print NOTICE("|-+ Differences for model:"), SQL_TABLE(model_name)
                    for diff in diffs:
                        if not dense:
                            print NOTICE("|--+"), ERROR_OUTPUT(diff['text'])
                        else:
                            print NOTICE("App"), SQL_TABLE(app_name), NOTICE('Model'), SQL_TABLE(model_name), ERROR_OUTPUT(diff['text'])
