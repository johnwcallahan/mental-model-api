from app import db

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

  def __init__(self):
    self.id = id
    self.title = title
    self.description = description
    self.url = url
    self.category = category

  @property
  def serialize(self):
    return {
      'id': self.id,
      'title': self.title,
      'description': self.description,
      'url': self.url,
      'category': self.category,
    }


  def __repr__(self):
    return '<Mental_Model: {}>'.format(self.title)
