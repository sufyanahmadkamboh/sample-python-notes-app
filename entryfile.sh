#!/bin/sh
set -e

# initialize DB
python -c "import app; app.init_db()"

# then run gunicorn
exec gunicorn -w 2 -b 0.0.0.0:5000 app:app
