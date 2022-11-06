from flask import Flask, render_template , request, url_for,redirect # import Flask class from flask module
from flask_sqlalchemy import SQLAlchemy# flask app and database connector
import json
from flask_mail import Mail
import logging,sys
import pymysql


app = Flask(__name__) # initialize my flask-app

app.logger.addHandler(logging.StreamHandler(sys.stdout))#-------------------#
app.logger.setLevel(logging.ERROR)#-----------------------------------------#

#doing for parameter configuration in config.json
#Taking variables from JSON file in flask app:
with open('config.json','r') as c:
    params = json.load(c)["params"]
app.config['MYSQL_UNIX_SOCKET'] = params['socket'] #...................................#
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri_MySQL'] #...................#
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #.................................#
db = SQLAlchemy(app) # initializing the database connection with flask


# doing for flask mail # gmail smtp server
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params["gmail-user"],
    MAIL_PASSWORD = params["gmail-password"]
)
# using function of Flask-Mail
mail = Mail(app)
#
## now create a classes to define the table of database
## keep the first letter of each class UPPERCASE:
## but the nae of class should be same as the name of table in database
class Contact(db.Model) : # making a class for flask-app to database connection

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    email =  db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(20), nullable = False)
    subject =db.Column(db.String(2000), nullable = True)
    message =db.Column(db.String(2000), nullable=False)
    #date =   db.Column(db.date) #, DEFAULT = current_timestamp(6), db.timestamp(6), nullable = True


@app.route("/", methods = ['GET','POST'])      # End-point of our web-app
def home():

    if (request.method == "POST") :
        '''fetch data from HTML page'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')

#        '''Add fetched data to database'''
#        '''now we puting the aboved fetched data in our made contacts class so that it transfers to datas
#        base'''
        entry = Contact(name= name, email = email, subject = subject, message = message, phone = phone) #date = datetime.date()
        db.session.add(entry)
        db.session.commit()
        # name = "senders name"
        # sender = "sender's email",
        # recipients = "your-email",
        # body = "message"
        mail.send_message('***Email by ' + name + ' +++',
                          sender=email,
                          recipients=[params['gmail-user']],
                          body="Subject = " + subject + "\n" + "message = " + message + "\n" + "cell = " + phone
                          )
        #sent = "Msg sent successfully"
        #return redirect(url_for('MsgSent'))
        return render_template("MsgSent.html", params = params)
    else:
        return render_template("index.html", params = params)#index.html


@app.route("/inner")
def inner():
    return render_template("inner-page.html", params = params)

# @myapp.route("/details")
# def details():
#     return render_template("portfolio-details.html",params=params)
@app.route("/MsgSent")
def details():
     return render_template("MsgSent.html", params = params)

if __name__ == "__main__" :
    app.run(debug=True)
