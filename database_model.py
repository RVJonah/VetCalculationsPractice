class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    Hash = db.Column(db.String(512), nullable=False)
    College = db.Column(db.String(255),nullable=True)
    Email = LastName = db.Column(db.String(512), nullable=False)
    Username = db.Column(db.String(255), nullable=False)

    def __init__(self, id, FirstName, LastName, Hash, College, Email, Username):
        self.id = id
        self.FirstName = FirstName
        self.LastName = LastName
        self.Hash = Hash
        self.College = College
        self.Email = Email
        self.Username = Username

class Results(db.Model):
    id = db.Column(db.Integer, nullable=False)
    Result = db.Column(db.Integer, nullable=False)
    Test_Type = db.Column(db.String(10))

    def __init__(self, id, Result, Test_Type):
        self.Result = Result
        self.Test_Type = Test_Type

class Test_Answers(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    A1 = db.Column(db.Float, nullable=True)
    A1min = db.Column(db.Float, nullable=True)
    A2 = db.Column(db.Float, nullable=True)
    A2min = db.Column(db.Float, nullable=True)
    A3 = db.Column(db.Float, nullable=True)
    A3min = db.Column(db.Float, nullable=True)
    A4 = db.Column(db.Float, nullable=True)
    A4min = db.Column(db.Float, nullable=True)
    A5 = db.Column(db.Float, nullable=True)
    A5min = db.Column(db.Float, nullable=True)
    A6 = db.Column(db.Float, nullable=True)
    A6min = db.Column(db.Float, nullable=True)
    A7 = db.Column(db.Float, nullable=True)
    A7min = db.Column(db.Float, nullable=True)
    A8 = db.Column(db.Float, nullable=True)
    A8min = db.Column(db.Float, nullable=True)
    A9 = db.Column(db.Float, nullable=True)
    A9min = db.Column(db.Float, nullable=True)
    A0 = db.Column(db.Float, nullable=True)
    A0min = db.Column(db.Float, nullable=True)

    def __init__(self, id, A1, A1min, A2, A2min, A3, A3min, A4, A4min, A5, A5min,
                A6, A6min, A7, A7min, A8, A8min, A9, A9min, A0, A0min):
        self.id = id
        self.A1 = A1
        self.A1min = A1min
        self.A2 = A2
        self.A2min = A2min
        self.A3 = A3
        self.A3min = A3min
        self.A4 = A4
        self.A4min = A4min
        self.A5 = A5
        self.A5min = A5min
        self.A6 = A6
        self.A6min = A6min
        self.A7 = A7
        self.A7min = A7min
        self.A8 = A8
        self.A8min = A8min
        self.A9 = A9
        self.A9min = A9min
        self.A0 = A0
        self.A0min = A0min
