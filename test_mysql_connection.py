import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://local_time_project_user:hq66YiC5TBxamPoxdvCS67hR8wnFFsk1@dpg-cq4c2jdds78s73chu1n0-a/local_time_project')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

