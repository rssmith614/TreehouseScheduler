from flask import Flask
import sqlite3

app = Flask(__name__)

db = sqlite3.connect('Scheduler/instance/data.sqlite', check_same_thread=False)

import Scheduler.studentviews
import Scheduler.tutorviews