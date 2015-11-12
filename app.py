from flask import Flask, render_template, redirect, request
from flask.ext.mysql import MySQL
import datetime

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'persons_db'
mysql.init_app(app)


@app.route("/")
def main():
  conn = mysql.connect()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM persons")
  persons = cursor.fetchall()

  conn.commit()
  cursor.close()
  conn.close()
  return render_template('index.html', persons=persons)


@app.route('/submit',methods=['POST'])
def submit():
  conn = mysql.connect()
  cursor = conn.cursor()


  query_str = "INSERT INTO `persons` (`firstname`,`lastname`,`birthdate`,`zip`) VALUES (%s, %s, %s, %s);"
  query_ok = cursor.execute(query_str, (request.form['firstname'],request.form['lastname'],request.form['birthdate_add'],request.form['zip']))

  conn.commit()
  cursor.close()
  conn.close()

  return redirect('/')

@app.route('/submit/<int:id>',methods=['POST'])
def update(id):
  conn = mysql.connect()
  cursor = conn.cursor()

  query_str = "UPDATE `persons` SET `firstname`=%s,`lastname`=%s,`birthdate`=%s,`zip`=%s WHERE `persons_id`=" + str(id) + ";"
  query_ok = cursor.execute(query_str, (request.form['firstname'],request.form['lastname'],request.form['birthdate_edit'],request.form['zip']))

  conn.commit()
  cursor.close()
  conn.close()
  print id

  return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
  conn = mysql.connect()
  cursor = conn.cursor()

  query_str = "DELETE FROM `persons` WHERE `persons_id`=" + str(id) + ";"
  query_ok = cursor.execute(query_str)

  conn.commit()
  cursor.close()
  conn.close()

  return redirect('/')

if __name__ == "__main__":
  app.run()