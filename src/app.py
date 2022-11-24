from ast import dump
from random import getstate
import re
from typing import final
from flask import Flask, render_template,request, url_for, flash, redirect,current_app
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class State(FlaskForm):
    statename = StringField(label=('Enter state Name:'), validators=[DataRequired()])
    stateab = StringField(label=('Enter state Ab:'), validators=[DataRequired()])
    submit = SubmitField(label=('Submit'))


app = Flask(__name__)
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'artgallery'
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
mysql = MySQL(app)
def getCustomers(state):
    query = '''select c.cID, c.name, c.street, c.city, c.stateAb,s.stateName, c.zipcode
from customer c
join state s
on s.stateAb = c.stateAb
where s.stateAb like %s or s.stateName like %s '''
    cur = mysql.connection.cursor()
    cur.execute(query, (state,state))
    rv = cur.fetchall()
    print(cur._executed)
    cur.close()
    return rv

def getStates():
        query = '''select * from state'''
        cur = mysql.connection.cursor()
        cur.execute(query)
        rv = cur.fetchall()   
        print(rv)
        flash(cur._executed)
        cur.close() 
        return rv

def createState(statename,stateab):
    try:
        query = '''insert into state(statename,stateab) values(%s,%s)'''
        cur = mysql.connection.cursor()
        cur.execute(query,(statename,stateab))
        mysql.connection.commit()
        cur.close()
    except:
        print('exception')
        mysql.connection.rollback()
    # finally:
        # mysql.connection.close()

def updateState(oldstatename,statename,stateab):
    try:
        print(oldstatename)
        print(statename)
        print(stateab)
        query = '''update state set statename = %s, stateab= %s where statename = %s'''
        cur = mysql.connection.cursor()
        cur.execute(query,(statename,stateab,oldstatename))
        print(cur._executed)
        mysql.connection.commit()
        cur.close()
    except:
        print('exception')
        mysql.connection.rollback()
    

def removestate(statename):
    try:
        cur = mysql.connection.cursor()
        cur.execute('''delete from state where statename like %s''',(statename,))
        mysql.connection.commit()
        cur.close()
    except:
        flash('cannot delete foreign key ')
    # finally:
        # mysql.connection.close()
        
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/arts', methods = ('GET', 'POST'))
def listArts():
    # data     
     if request.method == 'GET':
        return render_template('arts.html',result=getCustomers('texas') )
     else:
        state = request.form['state']
        if not state:
            flash('state is required!')
        else:
            return render_template('arts.html',result=getCustomers(state))

@app.route('/add')
def addArt():
    return render_template('add.html')

@app.route('/states', methods = ('GET', 'POST'))
def states():
    form = State()
    if request.method == 'POST' and form.validate_on_submit():
        print('valid form')
        statename = request.form['statename']
        stateab = request.form['stateab']
        createState(statename,stateab)
        return redirect('/states')
    if request.method == 'GET':
        return render_template('states.html',result=getStates(),form=form)

@app.route('/deletestate/<id>')
def deletestate(id):
    removestate(id)
    return redirect('/states')


@app.route('/updatestate', methods = ['POST'])
def updatestate():
    form = State()
    if request.method == 'POST' and form.validate_on_submit():
        print('valid form')
        oldstatename = request.form['oldstatename']
        statename = request.form['statename']
        stateab = request.form['stateab']
        updateState(oldstatename,statename,stateab)
        return redirect('/states')