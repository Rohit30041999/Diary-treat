# Diary-treat
This application is to store and access the day to day data of the milk in terms of liters.

1) Made use of Python backend web framework called flask to build this application 
   and also used sqlite3 as a database to store the data and flask_sqlalchemy to make 
   connections between flask and sqlite3 with the help of Models..
   
   
# Requirements:

1) Python3 (recommended python 3.5+)

2) pip3 or pip (Python Package manager)


# Steps To run a flask app:

1) virtual envirement required so that you can develop applications even if the versions are not matching install virtualenv from          pip(Python package manager) i.e, 
	
	$ pip install virtualenv

2) Create a virutal envirment as follows 

	$ virtualenv envirmentName

3) Activate virtual envirment as follows 
	
	$ envirmentName\Scripts\activate
	
  from pip install flask, flask-sqlalchemy(for database connection) as follows
   
   (envirmentName) $ pip install flask, flask-sqlalchemy

4) After everything is successfull you can clone the Diary-treat repository and execute the following command 
	
	$ python app.py (Server starts after executing this command)
	
5) You must also required to download the sqlite3 database from the browzer to store the data.
