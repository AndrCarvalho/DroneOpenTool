#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from WebInterface import app

CGIHandler().run(app)