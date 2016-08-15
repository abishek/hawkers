from socket import gethostname
from hawkers import app
from jinja2 import FileSystemBytecodeCache

if 'liveconsole' not in gethostname() :
    extra_dirs = ['./hawkers/templates', './hawkers/vendor_templates']
    import os
    import os.path as path
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    app.jinja_env.bytecode_cache = FileSystemBytecodeCache('jinja_cache')
    app.run(debug=True, use_reloader=True, extra_files=extra_files)