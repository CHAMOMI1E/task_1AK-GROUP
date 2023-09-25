from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TestModel(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    some = db.Column(db.String)

    def __init__(self, some):
        self.some = some


# main page
@app.route("/")
def main():
    return "It's work"
