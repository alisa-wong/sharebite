from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os 

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'menu.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# sectionItems = db.Table('menu_items',
#     db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
#     db.Column('section_id', db.Integer, db.ForeignKey('section.id'), primary_key=True)
# )

# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     item = db.Column(db.String(200), unique=True)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)

    # items = db.relationship('Item', secondary="menu_items", lazy='joined', backref='section')

    def __init__(self, name):
        self.name = name
        # self.items = items

# class ItemSchema(ma.Schema):
#     class Meta:
#         model = Item

class MenuSchema(ma.Schema):
    # items = ma.Nested(ItemSchema, many=True)
    class Meta:
        fields = ['id', 'name']

section_schema = MenuSchema()
menu_schema = MenuSchema(many=True)

# Get menu section by id
@app.route("/menusection/<id>", methods=['GET'])
def getSectionByID(id):
    section = Section.query.get(id)
    return section_schema.jsonify(section)

# Get all menu sections
@app.route("/menusection", methods=['GET'])
def getSections():
    all_sections = Section.query.all()
    result = menu_schema.dump(all_sections)
    return jsonify(result.data)

# Add new menu section
@app.route("/menusection", methods=['POST'])
def addSection():
    name = request.json['name']
    # items = request.json['items']
    new_section = Section(name)

    db.session.add(new_section)
    db.session.commit()

    return section_schema.jsonify(new_section)

# Edit a menu section
@app.route("/menusection/<id>", methods=["POST"])
def editSection(id):
    section = Section.query.get(id)
    name = request.json['name']

    section.name = name
    db.session.commit()

    return section_schema.jsonify(section)

# Delete a menu section
@app.route("/menusection/<id>", methods=["DELETE"])
def deleteSection(id):
    section = Section.query.get(id)
    db.session.delete(section)
    db.session.commit()

    return section_schema.jsonify(section)

if __name__ == '__main__':
    app.run(debug=True)