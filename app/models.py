from app import db

from marshmallow_sqlalchemy import ModelSchema


class Mental_Model(db.Model):
    """
    Create Mental_Model table
    """

    __tablename__ = 'Mental_Models'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), index=True, unique=True)
    description = db.Column(db.Text())
    url = db.Column(db.String(255))
    category = db.Column(db.String(45))

    def update(self, **kwargs):
        for key, value in  kwargs.items():
            if key != 'title':
                print('setting {}'.format(key))
                setattr(self, key, value)

    def __repr__(self):
        return '<Mental_Model: {}>'.format(self.title)


class Mental_Model_Schema(ModelSchema):
    class Meta:
        model = Mental_Model
