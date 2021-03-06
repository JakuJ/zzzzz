USER=***REMOVED***
SERVER=***REMOVED***
HTTP_PORT=5001
SSH_PORT=22

.PHONY: install fetcher server rename sync 

install:
	pip3 install --upgrade -r requirements.txt
	mypy *.py

fetcher:
	until python3 fetcher.py; do echo "Fetcher crashed with exit code $?.  Respawning..." >&2; sleep 1; done

server:
	gunicorn -w 2 --log-level debug --bind 0.0.0.0:${HTTP_PORT} wsgi

backup:
	rsync --progress --rsh="ssh -p ${SSH_PORT}" -aruzhv ${USER}@${SERVER}:~/Desktop/Stalky/data_backup.db .
	mv data_backup.db data.db
