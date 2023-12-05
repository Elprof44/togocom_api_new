from flask import Flask, request, render_template
import sqlite3 as sql
import uuid
import datetime

app = Flask(__name__)
app.secret_key = 'fdjnlfmgsfmccsnkfsjjhhhkkj'


def get_connect():
    conn = sql.connect('basedonne.db')
    conn.row_factory = sql.Row
    return conn

def get_date():
    now = datetime.datetime.now()
    return now.strftime( "%d/%m/%Y, %H:%M")

# insert pdv


@app.route('/insert/pdv/<vm_id>/<pdv_name>/<agent_name>/<number>')
def insertpdv(vm_id, pdv_name, agent_name, number):
    uuid_pdv = str(uuid.uuid4())
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO pdv(pdv_uuid ,vm_uuid, pdv_name, 
                   agent_name, number) VALUES (?,?,?,?,?)
                   """, (uuid_pdv, vm_id, pdv_name, agent_name, number))
    conn.commit()
    return 'true'

# insert vm


@app.route('/', methods=['POST', 'GET'])
def insertvm():
    if request.method == 'POST':
        conn = get_connect()
        cursor = conn.cursor()
        name = request.form.get('name')
        number = request.form.get('number')
        password = request.form.get('password')
        vm_uuid = str(uuid.uuid4())
        cursor.execute("""INSERT INTO vm(vm_uuid, name, number, password) VALUES (?,?,?,?)
                   """, (vm_uuid, name, number, password))
        conn.commit()
        return render_template('index1.html')
    else:
        return render_template('index.html')


# insert historique
@app.route('/insert/historique/<vm_id>/<vm_name>/<vm_number>/<pdv_id>/<pdv_name>/<pdv_number>/<montant>')
def inserthistorique(vm_id, vm_name, vm_number, pdv_id, pdv_name, pdv_number, montant):
    date = get_date
    conn = get_connect()
    cursor = conn.cursor()
    req = """INSERT INTO historique(vm_uuid, vm_name, vm_number,
      pdv_uuid, pdv_name, pdv_number, montant, date, is_padding) VALUES(?,?,?,?,?,?,?,?,?)"""
    cursor.execute(req, (vm_id, vm_name, vm_number, pdv_id,
                   pdv_name, pdv_number, montant, date, 0))
    conn.commit()
    return 'true'
# get all pdv for mv by the vm id


@app.route('/get_pdv/<vm_id>')
def getpdv(vm_id):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pdv WHERE vm_uuid = ?", (vm_id,))
    return [dict(row) for row in cursor.fetchall()]

# get all history for pdv by the vm id


@app.route('/vm_historique/<vm_id>')
def gethistoriquebyvm(vm_id):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM historique WHERE vm_uuid = ?", (vm_id,))
    return [dict(row) for row in cursor.fetchall()]
# get all history for pdv by the pdv id


@app.route('/pdv_historique/<pdv_id>')
def gethistoriquebypdv(pdv_id):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM historique WHERE pdv_uuid = ?", (pdv_id,))
    return [dict(row) for row in cursor.fetchall()]


    #    login systheme call


@app.route('/login/<number>/<password>')
def login(number, password):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT vm_uuid,name,number FROM vm WHERE number = ? AND password = ?", (number, password,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


if __name__ == '__main__':
    app.run(debug=True)
