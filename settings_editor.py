import ast
import sys
import argparse

from flask import Flask
from flask_admin import Admin
from flask_basicauth import BasicAuth
from wtforms.fields import TextAreaField
from flask_admin.babel import lazy_gettext
from flask_admin.contrib.fileadmin import FileAdmin
from wtforms.validators import required, StopValidation


def configure_app(app):
    app.config.from_envvar('SETTINGS_EDITOR_SETTINGS')
    for setting_name in ('BASIC_AUTH_USERNAME', 'BASIC_AUTH_PASSWORD', 'DIR_PATH', 'SECRET_KEY'):
        assert app.config.get(setting_name), 'You must set up {}'.format(setting_name)
    app.config['EDIT_EXTENSIONS'] = app.config.get('EDIT_EXTENSIONS', ('py',))
    app.config['BASIC_AUTH_FORCE'] = True
    app.secret_key = app.config['SECRET_KEY']


def create_app():
    app = Flask(__name__)
    configure_app(app)

    BasicAuth(app)
    file_admin_view = FileAdminView(app.config['EDIT_EXTENSIONS'], app.config['DIR_PATH'],
                                    '/static/', name='Files', url='/')
    Admin(app, index_view=file_admin_view, name='Settings editor', template_mode='bootstrap3')
    return app


def parse_args():
    parser = argparse.ArgumentParser()
    for arg_name, arg_params in (['--port', {'type': int, 'default': 5005, 'dest': 'port'}],
                                 ['--host', {'type': str, 'default': '127.0.0.1', 'dest': 'host'}],
                                 ['--debug', {'type': bool, 'default': False, 'dest': 'debug'}]):
        parser.add_argument(arg_name, **arg_params)
    args = parser.parse_args()
    return args


class FileAdminView(FileAdmin):

    def __init__(self, editable_extensions, *args, **kwargs):
        self.editable_extensions = editable_extensions
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'
        self.endpoint = 'admin'

    def get_edit_form(self):
        class EditForm(self.form_base_class):
            content = TextAreaField(lazy_gettext('Content'), (required(),), render_kw={'rows': 40})

            def validate_content(self, field):
                try:
                    ast.parse(field.data)
                except SyntaxError:
                    raise StopValidation('You have an error in syntax')

        return EditForm


if __name__ == '__main__':
    args = parse_args()
    sys.exit(create_app().run(debug=args.debug, port=args.port, host=args.host))
