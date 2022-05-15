{
	kill -9 $(ps -elf | pgrep uwsgi | grep -v grep)
} || {
	echo "Failed to kill uwsgi"
}

{
	kill -9 $(ps -elf | pgrep :3001 | grep -v grep)
} || {
	echo "Failed to kill process for port 3001"
}

{
	deactivate
	source ~/Cision/mrpoc/venv/bin/activate
	export cision_SERVER=dev
	export cision_PRINT=False
	export cisionDB_HOST=localhost
	export cisionDB_PORT=3306
	export cisionDB_USER=admin1
	export cisionDB_PASSWORD=P@ssw0rd1234
	export cisionDB_NAME=cision
	~/Cision/mrpoc/venv/bin/uwsgi --ini ~/Cision/mrpoc/cisionPOC/cision/uwsgi/dev.ini  > /dev/null 2>&1 &
} || {
	echo "Failed to start uwsgi server"
}




												
{
        kill -9 $(ps -elf | pgrep celery | grep -v grep)
} || {
        echo "Failed to kill celery"
}


{
	deactivate
	source ~/Cision/mrpoc/venv/bin/activate
	celery -A cision purge -f &
} || {
	echo "Failed to purge celery"
}


{
	export cision_SERVER=dev
	export cision_PRINT=False
	export cisionDB_HOST=localhost
	export cisionDB_PORT=3306
	export cisionDB_USER=admin1
	export cisionDB_PASSWORD=P@ssw0rd1234
	export cisionDB_NAME=cision

	cd ~/Cision/mrpoc/cisionPOC/cision
	~/Cision/mrpoc/venv/bin/celery -A cision worker -c 4 -l info --logfile ~/Cision/mrpoc/cisionPOC/cision/logs/celery.log  > /dev/null 2>&1 &
} || {
	echo "Failed to start celery"
}		


