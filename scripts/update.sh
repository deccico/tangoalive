cd /home/adrian/tangoalive/src/tangoalive
git pull origin master  >> /home/adrian/updatelogs.txt
python manage.py migrate >> /home/adrian/model_updatelogs.txt
python manage.py collectstatic --noinput >> /home/adrian/static_files_update.txt
touch /home/adrian/tangoalive/src/tangoalive/tangoalive_uwsgi.ini