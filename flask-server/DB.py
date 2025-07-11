from flask_sqlalchemy import SQLAlchemy
import json


db = SQLAlchemy()


class Users(db.Model):
    username = db.Column(db.String(80), primary_key=True, nullable=False)


    def __repr__(self):
        return "<User %r>" % self.username

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, new_data):
        self.username = new_data.username
        db.session.commit()


class Requests(db.Model):
    # Define columns for the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey("users.username"), nullable=False)
    request_data = db.Column(db.Text, nullable=False)
    request_language = db.Column(db.String(10), nullable=False)
    request_data_extra = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<Request {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, new_data):
        self.request_data = new_data.request_data
        self.request_data_extra = json.dumps(
            new_data.request_data_extra
        )  # Serialize JSON object to string
        db.session.commit()

    def get_request_data_extra_as_json(self):
        self.request_data_extra = str(self.request_data_extra).replace("'", '"')
        print(self.request_data_extra)
        return json.loads(self.request_data_extra)  # Deserialize string to JSON object
