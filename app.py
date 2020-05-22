from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///milkPacket.db"
dataBase = SQLAlchemy(app)

class Login(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    username = dataBase.Column(dataBase.String(200), nullable=False)
    password = dataBase.Column(dataBase.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Task %r>' % self.id

class UsersDetails(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    username = dataBase.Column(dataBase.String(200), nullable=False)
    gmailId = dataBase.Column(dataBase.String(200), nullable=True)
    address = dataBase.Column(dataBase.String(300), nullable=False)
    startDate = dataBase.Column(dataBase.DateTime, default=datetime.utcnow)
    number_of_packets = dataBase.Column(dataBase.Integer, default=0)
    number_of_liters = dataBase.Column(dataBase.Integer, default=0)

    def __init__(self, username, gmailId, address):
        self.username = username
        self.gmailId = gmailId
        self.address = address

    def __repr__(self):
        return '<Task %r>' % self.id


class EachDay(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    day = dataBase.Column(dataBase.DateTime, default=datetime.utcnow)
    amount_on_that_day = dataBase.Column(dataBase.Integer, default=0)
    liters_on_that_day = dataBase.Column(dataBase.Integer, default=0)
    eachId = dataBase.Column(dataBase.Integer, default=0)

    def __init__(self, amount_on_that_day, liters_on_that_day, eachId):
        self.amount_on_that_day = amount_on_that_day
        self.liters_on_that_day = liters_on_that_day
        self.eachId = eachId

    def __repr__(self):
        return "<Task %r>" % self.id

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/Submit', methods=['POST', 'GET'])
def Submition():
    if request.method == 'POST':
        Username = request.form['username']
        Password = request.form['password']
        Gmail = request.form['email']
        Address = request.form['address']
        if len(Username) >= 4 and len(Password) >= 8:
            new_login_model = Login(Username, Password)
            new_user_details = UsersDetails(Username, Gmail, Address)
            try:
                dataBase.session.add(new_login_model)
                dataBase.session.add(new_user_details)
                dataBase.session.commit()
                return redirect('/')
            except:
                return 'Error Occurred while data storage.'
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/Enter', methods=['POST', 'GET'])
def enterForm():
    if request.method == 'POST':
        dataOfUser = Login.query.order_by(Login.username).all()
        Username = request.form['username']
        Password = request.form['password']
        for data in dataOfUser:
            if Username == data.username and Password == data.password:
                userDetails = UsersDetails.query.order_by(UsersDetails.username).all()
                for user in userDetails:
                    if Username == user.username:
                        return render_template('profile.html', data=[user])
        return redirect('/')
    else:
        return redirect('/Login')

@app.route('/Login', methods=['POST', 'GET'])
def loginForm():
    if request.method == 'POST':
        return render_template('login.html')
    else:
        return redirect('/Register')

@app.route('/Register', methods=['POST', 'GET'])
def registerationForm():
    if request.method == 'POST':
        return render_template('register.html')
    else:
        return redirect('/Login')

@app.route('/StoreData/<int:id>', methods=['POST', 'GET'])
def storeData(id):
    if request.method == 'POST':
        userData = UsersDetails.query.get_or_404(id)
        return render_template('storeData.html', data=userData)
    else:
        return render_template('login.html')


@app.route('/Store/<int:id>', methods=['POST', 'GET'])
def store(id):
    userData = UsersDetails.query.get_or_404(id)
    if request.method == 'POST':
        userData.number_of_packets += 50*(int(request.form['liters']))
        userData.number_of_liters += int(request.form['liters'])
        new_Each_Day_of_the_User = EachDay(20*(int(request.form['liters'])), int(request.form['liters']), id)
        try:
            dataBase.session.add(new_Each_Day_of_the_User)
            dataBase.session.commit()
            return render_template('profile.html', data=[userData])
        except:
            return 'Error occurred while storing the data'
    else:
        return render_template('storeData.html', data=userData)


@app.route('/GetData/<int:id>', methods=['POST', 'GET'])
def getData(id):
    if request.method == 'POST':
        userData = UsersDetails.query.get_or_404(id)
        each_day_list = []
        each_day_details = EachDay.query.order_by(EachDay.id).all()
        for each_day in each_day_details:
            if each_day.eachId == id:
                each_day_list.append(each_day)
        return render_template('profile.html', data=[userData, each_day_list])
    else:
        return render_template('login.html')

@app.route('/Logout', methods=['POST', 'GET'])
def logout():
    if request.method == 'POST':
        return render_template('login.html')
    else:
        return 'Not Able to Logout Please try again'

@app.route('/ResetAccount/<int:id>')
def resetAccount(id):
    userDetails = UsersDetails.query.get_or_404(id)
    userDetails.number_of_packets = 0
    userDetails.number_of_liters = 0
    try:
        each_day_data = EachDay.query.order_by(EachDay.id).all()
        for eachDateData in each_day_data:
            if eachDateData.eachId == id:
                dataBase.session.delete(eachDateData)
        dataBase.session.commit()
        return render_template('profile.html', data=[userDetails])
    except:
        return render_template('profile.html', data=[userDetails])


if __name__ == '__main__':
    data = UsersDetails.query.order_by(UsersDetails.startDate).all()
    for d in data:
        print(str(d.id) + " | " + d.username + ' | ' + d.gmailId + ' | ' + d.address + ' | ' + str(d.startDate.date()) + ' | ' + str(d.number_of_packets) + ' | ' + str(d.number_of_liters))
    app.run(host='0.0.0.0',debug=True)
