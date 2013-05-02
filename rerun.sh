#!/bin/sh

#echo > imglog.txt
#rm -fR media/*
#./manage.py sqlclear gtdb pybb taggit contenttypes auth galeria | ./manage.py dbshell
#./manage.py syncdb --noinput
#./manage.py importhp --traceback -v 3
#./manage.py rebuild_index --noinput
./manage.py runserver
