from flask import Flask,jsonify
from flask_mongoengine import MongoEngine
import mongoengine as db
from api_constants import mongodb_password

app=Flask(__name__)

database_name = "API"
DB_URI = "mongodb+srv://aditi:{}@cluster0.kqbkxio.mongodb.net/{}?retryWrites=true&w=majority".format(
 mongodb_password,database_name
)

app.config["MONGODB_HOST"] = DB_URI

db=MongoEngine()
db.init_app(app)

class Student(db.Document):
    student_id = db.IntField()
    student_name = db.StringField()
    student_email = db.StringField()
    student_gender = db.StringField()
    student_age = db.IntField()
    
    def to_json(self):                 # to convert this document into json
        return {
            "student_id": self.student_id,
            "student_name":self.student_name,
            "student_email":self.student_email,
            "student_gender":self.student_gender,
            "student_age":self.student_age
        }
        
@app.route('/')
def add_records():
    stud1=Student(student_id=1, student_name="aditi", student_email='aditi@gmail.com',student_gender="female", student_age=22)
    stud2=Student(student_id=2, student_name="aisha", student_email='aisha@gmail.com',
                     student_gender="female", student_age=23)
    stud1.save()
    stud2.save()
    return jsonify(stud1.to_json(),stud2.to_json())

@app.route('/update')
def update_records():
    student_name='aditi'
    stud1=Student.objects(student_name=student_name).first()
    if not stud1:
        return jsonify({'error':'data not found'})
    else:
        stud1.update(student_email='updateemail@gmail.com')
        return jsonify(stud1.to_json())
    
@app.route('/delete')
def delete_record():
    student_name='aditi'
    user=Student.objects(student_name=student_name).first()
    if not user:
        return jsonify({'error':'data not found'})
    else:
        user.delete()
        return jsonify(user.to_json())

if __name__=="__main__":
    app.run(debug=True)