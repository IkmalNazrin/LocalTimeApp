import os

class Config:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'dpg-cq4c2jdds78s73chu1n0-a.singapore-postgres.render.com')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'local_time_project')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'local_time_project_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'hq66YiC5TBxamPoxdvCS67hR8wnFFsk1')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
