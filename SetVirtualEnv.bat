@echo off
call virtualenv env
call env\scripts\activate
call pip install -r requirements.txt
