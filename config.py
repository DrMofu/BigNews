#encoding: utf-8
import os
from datetime import timedelta

DEBUG = False
SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(days=5)