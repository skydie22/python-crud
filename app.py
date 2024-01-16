import mysql.connector
from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)

#fungsi untuk membuka koneksi ke database
def openDb():
   global db, cursor
   db = mysql.connector.connect(
         host = 'localhost',
         user = 'root',
         password = '',
         database = 'mhsiswa_gunadarma')        
   cursor = db.cursor()
#fungso untuk menutup koneksi database
def closeDb():
   global db, cursor
   cursor.close()
   db.close()
#fungsi untuk menampilkan data dari database
@app.route("/")
def index():
   openDb()
   container = []
   sql = "Select * from mahasiswa"
   cursor.execute(sql)
   result = cursor.fetchall()
   for data in result:
      container.append(data)
   closeDb()
   return render_template('index.html', container=container)
#fungsi untuk menambhkan data ke database
@app.route('/add',  methods=['GET','POST'])
def add():
   if request.method == 'POST':
      nama = request.form['nama']
      npm = request.form['npm']
      kelas = request.form['kelas']
      openDb()
      sql = "insert into mahasiswa (nama, npm, kelas) values (%s, %s, %s)"
      val = (nama, npm, kelas)
      cursor.execute(sql, val)
      db.commit()
      closeDb()
      return redirect(url_for('index'))
   else:
      closeDb()
      return render_template('tambah.html')
#fungsi untuk mengedit data yg ada di database berdasarkan id
@app.route('/edit/<id_mahasiswa>', methods=['GET','POST'])
def edit(id_mahasiswa):
   openDb()
   cursor.execute('SELECT * FROM mahasiswa WHERE id_mahasiswa=%s',(id_mahasiswa,))
   data = cursor.fetchone()
   if request.method == 'POST':
      id_mahasiswa = request.form['id_mahasiswa']
      nama = request.form['nama']
      npm = request.form['npm']
      kelas = request.form['kelas']
      sql = "UPDATE mahasiswa SET nama=%s, npm=%s, kelas=%s WHERE id_mahasiswa=%s"
      val = (nama, npm, kelas, id_mahasiswa)
      cursor.execute(sql, val)
      db.commit()
      closeDb()
      return redirect(url_for('index'))
   else:
      closeDb()
      return render_template('edit.html', data=data)
#fungsi untuk menghapus data yg ada di database berdasarkan id
@app.route('/delete/<id_mahasiswa>', methods=['GET','POST'])
def hapus(id_mahasiswa):
   openDb()
   cursor.execute('DELETE FROM mahasiswa WHERE id_mahasiswa=%s', (id_mahasiswa,))
   db.commit()
   closeDb()
   return redirect(url_for('index'))
   
   
if __name__ == '__main__':
   app.run(debug=True)
      





