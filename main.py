from email.policy import default
from sqlite3 import IntegrityError
from flask import Flask,render_template,redirect, request, url_for,flash,session
from form import Login
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import exc

Myapp = Flask(__name__)
Myapp.config['SECRET_KEY'] = '661e3b1083fafb5545d4cb0d1f75327806cc81101084e57478db55'
Myapp.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db = SQLAlchemy(Myapp)
class School(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    roll = db.Column(db.String(20),unique=True,nullable=False)
    atten = db.relationship('Attendance',backref='author',lazy=True)

    def __repr__(self):
        return f"School('{self.name}','{self.roll}')"

class Attendance(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('school.id'),nullable=False)
    Date = db.Column(db.String(20),nullable=False)
    attendance_value = db.Column(db.String(20))
    

@Myapp.route("/",methods=['GET','POST'])
def home():
    session['isvaliduser'] = False
    form = Login()
    if form.validate_on_submit():
        if form.adminname.data=='admin' and form.password.data=='1234':
            session['isvaliduser'] = True
            return redirect(url_for('info'))
        else:
            flash('Login Creentials are incorect','danger')
    return render_template('layout.html',form=form)

@Myapp.route("/info",methods=['GET','POST'])
def info():
    if session['isvaliduser']==True:
        details = School.query.all()
        global count
        count = {}
        for i in details:
            st = Attendance.query.filter_by(user_id=i.id).all()
            temp=0
            for j in st:
                if j.attendance_value == 'Present':
                    temp+=1
            count.update({i.id:temp})
        return render_template('info.html',details=details,count=count,flash_message=False)
    return redirect(url_for('home'))

@Myapp.route("/attendance")
def attendance():
    if session['isvaliduser']==True:
        details = School.query.all()
        return render_template('attendance.html',details=details)

    return redirect(url_for('info'))

@Myapp.route("/new_student",methods=['GET','POST'])
def new_student():
    details = School.query.all()
    if request.method == "POST":
        new_name = request.form.get("fname")
        new_roll = request.form.get("froll")
        u1 = School(name=new_name,roll=new_roll)
        try:
            db.session.add(u1)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return render_template('info.html',details=details,count=count,flash_message=True)
        return redirect(url_for('info'))
    return render_template('home.html',details=details)

@Myapp.route("/attendance",methods=['GET','POST'])
def student_attendance():
    details = School.query.all()
    if request.method=='POST':
        for i in details:
            at_value = request.form.get(f'{ i.id }')
            now = datetime.now()
            date = str(now.strftime("%d-%m-%Y"))
            u2 = Attendance(user_id=i.id, Date=date, attendance_value=at_value)
            db.session.add(u2)
        db.session.commit()
        return redirect(url_for('info'))
    return render_template('layout.html',details=details)

if __name__=='__main__':
    Myapp.run(debug=True)