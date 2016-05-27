from socket import gethostname
from hawkers import app

if 'liveconsole' not in gethostname() :
    app.run(debug=True, use_reloader=True)
