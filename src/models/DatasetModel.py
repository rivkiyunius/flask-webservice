from marshmallow import fields, Schema
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DatasetModel(db.Model):
    __tablename__ = 'dataset'

    id = db.Column(db.Integer, primary_key=True)
    number_of_pregnancy = db.Column(db.Integer, nullable=False)
    plasma_glucose_concentration = db.Column(db.Integer, nullable=False)
    diastolic_blood_pressure = db.Column(db.Integer, nullable=False)
    triceps_skin_thickness = db.Column(db.Integer, nullable=False)
    serum_insulin = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    diabetes_pedigree_function = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    test_result = db.Column(db.Integer)

    def __init__(self, data):
        self.id = data.get('id')
        self.number_of_pregnancy = data.get('number_of_pregnancy')
        self.plasma_glucose_concentration = data.get('plasma_glucose_concentration')
        self.diastolic_blood_pressure = data.get('diastolic_blood_pressure')
        self.triceps_skin_thickness = data.get('triceps_skin_thickness')
        self.serum_insulin = data.get('serum_insulin')
        self.bmi = data.get('bmi')
        self.diabetes_pedigree_function = data.get('diabetes_pedigree_function')
        self.age = data.get('age')
        self.test_result = data.get('test_result')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    @staticmethod
    def get_all_dataset():
        return DatasetModel.query.all()

    @staticmethod
    def get_one_dataset():
        return DatasetModel.query.get(id)

    @staticmethod
    def get_x_dataset():
        return db.engine.execute(
            'select number_of_pregnancy, plasma_glucose_concentration, diastolic_blood_pressure, triceps_skin_thickness, serum_insulin, bmi, diabetes_pedigree_function, age from dataset')
        # return db.query.all()

    @staticmethod
    def get_y_dataset():
        return db.engine.execute('select test_result from dataset')

    def __repr__(self):
        return '<id {}>'.format(self.id)


# for migrating db
class DatasetSchema(Schema):
    id = fields.Int(dump_only=True)
    number_of_pregnancy = fields.Int(required=True)
    plasma_glucose_concentration = fields.Int(required=True)
    diastolic_blood_pressure = fields.Int(required=True)
    triceps_skin_thickness = fields.Int(required=True)
    serum_insulin = fields.Float(required=True)
    bmi = fields.Float(required=True)
    diabetes_pedigree_function = fields.Float(required=True)
    age = fields.Int(required=True)
    test_result = fields.Int(required=False)
