from flask import Flask

app = Flask(__name__)

# if not os.path.exists(app.config['CONTENT_DIR']):
#     print('content directory not exist, Toki will make it for u')
#     work_dir = os.path.abspath(os.curdir)
#     os.mkdir(app.config['CONTENT_DIR'])
#     os.chdir(app.config['CONTENT_DIR'])
#     os.chdir(work_dir)
#
#
# def clear_time(time):
#     return '%s-%s-%s %s:%s' % (time.year, time.month, time.day, time.hour, time.minute)
#
#
# def format_float(value):
#     return "{:,.1f}".format(value)
#
# app.jinja_env.globals.update(clear_time=clear_time)
# app.jinja_env.globals.update(format_float=format_float)
from app import routes
