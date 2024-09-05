#!/usr/bin/env python3
import pymysql
import math
import cgitb
cgitb.enable()
import sys
import copy
from operator import itemgetter
import os
import re
import hashlib
from subprocess import Popen, PIPE, STDOUT
import random
import string
from datetime import date
from datetime import timedelta
# # import Cookie

def connect_db():
        # PURPOSE: connect to database
        connection = pymysql.connect()
        cursor = connection.cursor()

        return cursor, connection

cursor, connection = connect_db()

print("Content-type: text/json\n\n")
print("hello worm")