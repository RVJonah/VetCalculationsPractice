from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from passwords import databaseURL, secret_key

secret_Key = secret_key

def initiate_ORM():
    db_URL = databaseURL
    engine = create_engine(db_URL)
    metadata = MetaData()
    students = Table('students', metadata,
                Column( 'id', Integer(), primary_key=True),
                Column('firstname', String(255), nullable=False),
                Column('lastname', String(255), nullable=False),
                Column('hash', String(512), nullable=False),
                Column('college', String(255),nullable=True),
                Column('email', String(512), nullable=False),
                Column('username', String(255), nullable=False),
            )

    class Students(object):
        def __init__(self, id, firstname, lastname, hash, college, email, username):
            self.id = id
            self.firstname = firstname
            self.lastname = lastname 
            self.hash = hash 
            self.college = college 
            self.email = email
            self.username = username
        def __repr__(self):
            return "<students(id='%i', firstname='%s', lastname='%s', hash='%s, college='%s, email='%s, username='%s)>" % (
            self.id, self.firstname, self.lastname, self.hash, self.college, self.email, self.username,)

    results = Table('results', metadata,
                Column('id', Integer(), nullable=False, primary_key=True),
                Column('result', Integer(), nullable=False),
                Column('test_type', String(10), nullable=False),
            )

    class Results(object):
        def __init__(self, id, result, test_type):
            self.id = id
            self.result = result
            self.test_type = test_type
        def __repr__(self):
            return "<results(id='%i', result='%i', test_type='%s')>" % (
            self.id, self.result, self.test_type)
    
    answers = Table('test_answers', metadata,
                Column('id', Integer(), nullable=False, primary_key=True),
                Column('a0', Float(), nullable=True),
                Column('a0min', Float(), nullable=True),
                Column('a1', Float(), nullable=True),
                Column('a1min', Float(), nullable=True),
                Column('a2', Float(), nullable=True),
                Column('a2min', Float(), nullable=True),
                Column('a3', Float(), nullable=True),
                Column('a3min', Float(), nullable=True),
                Column('a4', Float(), nullable=True),
                Column('a4min', Float(), nullable=True),
                Column('a5', Float(), nullable=True),
                Column('a5min', Float(), nullable=True),
                Column('a6', Float(), nullable=True),
                Column('a6min', Float(), nullable=True),
                Column('a7', Float(), nullable=True),
                Column('a7min', Float(), nullable=True),
                Column('a8', Float(), nullable=True),
                Column('a8min', Float(), nullable=True),
                Column('a9', Float(), nullable=True),
                Column('a9min', Float(), nullable=True),
            )

    class Test_answers(object):
        def __init__(self, id=0, a0=0, a0min=0, a1=0, a1min=0, a2=0, a2min=0, a3=0, a3min=0, a4=0, a4min=0,
            a5=0, a5min=0, a6=0, a6min=0, a7=0, a7min=0, a8=0, a8min=0, a9=0, a9min=0):
            self.id = id
            self.a0 = a0
            self.a0min = a0min
            self.a1 = a1
            self.a1min = a1min
            self.a2 = a2
            self.a2min = a2min
            self.a3 = a3
            self.a3min = a3min
            self.a4 = a4
            self.a4min = a4min
            self.a5 = a5
            self.a5min = a5min
            self.a6 = a6
            self.a6min = a6min
            self.a7 = a7
            self.a7min = a7min
            self.a8 = a8
            self.a8min = a8min
            self.a9 = a9
            self.a9min = a9min
        def __repr__(self):
            return ("<test_answers(self.id='%i'a0='%f',a0min ='%f',a1='%f',a1min='%f',a2='%f',a2min='%f',a3='%f',a3min='%f'," 
            "a4='%f',a4min='%f',a5=a5 '%f',a5min='%f',a6='%f',a6min='%f',a7='%f',a7min='%f',a8 ='%f',a8min='%f',a9='%f'"
            ",a9min='%f')>") % (
            self.id, self.a0, self.a0min, self.a1, self.a1min, self.a2, self.a2min, self.a3, self.a3min, self.a4, self.a4min,
            self.a5, self.a5min,self.a6, self.a6min, self.a7, self.a7min, self.a8, self.a8min, self.a9, self.a9min)
    
    nulldict = {'a0': None, 'a0min': None, 'a1': None, 'a1min': None,'a2': None, 'a2min': None, 'a3': None, 'a3min': None,
            'a4': None, 'a4min': None, 'a5': None, 'a5min': None, 'a6': None, 'a6min': None, 'a7': None, 'a7min': None,
            'a8': None, 'a8min': None, 'a9': None, 'a9min': None
    }

    mapper(Test_answers, answers)
    mapper(Results, results)
    mapper(Students, students)

    metadata.create_all(engine)
    return ({
        'engine': engine,
        'tables': {
            "test_answers": Test_answers,
            "results": Results,
            "students": Students
        },
        'nulldict': nulldict,
    })