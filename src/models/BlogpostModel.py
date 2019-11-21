from marshmallow import fields, Schema
from . import db
import datetime


class BlogpostModel(db.Model):
    __tablename__ = "blogposts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    contents = db.Column(db.String, nullable=False)
    create_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, data):
        self.title = data.get('title')
        self.contents = data.get('contents')
        self.create_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.owner_id = data.get('owner_id')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_blogposts():
        return db.engine.execute("SELECT * FROM blogposts")
        # return BlogpostModel.query.all()

    @staticmethod
    def get_one_blogposts(id):
        return BlogpostModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class BlogpostSchemas(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    contents = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
