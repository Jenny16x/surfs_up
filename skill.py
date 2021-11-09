from flask import Flask

skill = Flask(__name__)

@skill.route('/')


def greet():
    return  ('Hello Jenny')



