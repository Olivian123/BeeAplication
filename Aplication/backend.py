import re
import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

import pyodbc

app = Flask(__name__)

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-A793I28\SQLEXPRESS;'
    'DATABASE=ferma;'
    'Trusted_Connection=yes;'
)

@app.route('/familii_de_albine', methods=['GET'])
def get_familii_de_albine():
    cursor = conn.cursor()
    cursor.execute("{CALL GetFamiliiDeAlbine}")
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows])


@app.route('/familii_de_albine', methods=['POST'])
def add_familii_de_albine():
    data = request.json

    id_regina = data.get('id_regina')
    id_stup = data.get('id_stup')

    # Check if the data is complete
    if not all([id_regina, id_stup]):
        return jsonify({'error': 'All fields required!'}), 400

    try:
        cursor = conn.cursor()

        # Execute the stored procedure
        cursor.execute("{CALL AddFamilieDeAlbine (?, ?, ?)}", (id_regina, id_stup, 'activa'))

        # Check for any error messages from SQL Server
        if cursor.messages:
            raise Exception(cursor.messages)

        # Commit transaction if all operations succeed
        conn.commit()

        return jsonify({'message': 'Familie de Albine added successfully!'}), 201

    except Exception as e:
        # Handle SQL errors raised by RAISERROR in the SQL procedure
        clean_message = str(e).split('[SQL Server]')[1].split('(')[0].strip()

        return jsonify({
            'error': clean_message
        }), 400

# GET method for Regina table
@app.route('/regine', methods=['GET'])
def get_regine():
    cursor = conn.cursor()
    cursor.execute("{CALL GetRegine}")
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows])

# POST method for Regina table
@app.route('/regina', methods=['POST'])
def add_regina():
    data = request.get_json()

    tip_regina = data['tip_regina']
    data_imperechere = data['data_imperechere']
    status = data['status']
    varsta = data['varsta']
    provenienta = data['provenienta']
    
    # Check if the data is complete
    if not all([tip_regina, data_imperechere, status, varsta, provenienta]):
        return jsonify({'error': 'All fields required!'}), 400

    cursor = conn.cursor()
    cursor.execute("INSERT INTO Regina (tip_regina, data_imperechere, status_, varsta, provenienta) "
                   "OUTPUT INSERTED.id_regina VALUES (?, ?, ?, ?, ?)",
                   (tip_regina, data_imperechere, status, varsta, provenienta))
    
    # Fetch the id_regina of the newly inserted row
    id_regina = cursor.fetchone()[0]
    
    conn.commit()

    return jsonify({"message": "Regina added successfully!", "id_regina": id_regina}), 201


# GET method for Stup table
@app.route('/stupi', methods=['GET'])
def get_stupi():
    cursor = conn.cursor()
    cursor.execute('{CALL GetStupi}')
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows])

# POST method for Stup table
@app.route('/stup', methods=['POST'])
def add_stup():
    data = request.get_json()
    tip = data['tip']
    numar_rame = data['numar_rame']
    dimensiuni = data['dimensiuni']
    material = data['material']
    cantitate = data['cantitate']

    cursor = conn.cursor()

    cursor.execute("""
        EXEC AddStup ?, ?, ?, ?, ?;
    """, (tip, numar_rame, dimensiuni, material, cantitate))

    conn.commit()

    return jsonify({"message": "Stup added successfully!"}), 20

# GET method for Stup table
@app.route('/stup', methods=['GET'])
def get_stup():
    data = request.json
    tip = data.get('tip')

    if not tip:
        return jsonify({'error': 'All fields required!'}), 400

    cursor = conn.cursor()
    cursor.execute(
                    'SELECT id_stup FROM Stup WHERE tip = ?',
                    (tip)
                  )
    rows = cursor.fetchall()

    if not rows:
        return jsonify({'error': 'Nothing found!'}), 400

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows]), 201



@app.route('/apicultori', methods=['GET'])
def get_apicultori():
    cursor = conn.cursor()
    cursor.execute("{CALL GetAllApicultori}")
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows]), 201

@app.route('/apicultori', methods=['POST'])
def add_apicultor():
    data = request.json

    nume = data.get('nume')
    prenume = data.get('prenume')
    rol = data.get('rol')
    id_maestru = data.get('id_maestru')

    # Check if the data is complete
    if not all([nume, prenume, rol, id_maestru]):
        return jsonify({'error': 'All fields required!'}), 400

    cursor = conn.cursor()
    
    cursor.execute("{CALL AddApicultor (?, ?, ?, ?)}", (nume, prenume, rol, id_maestru))

    conn.commit()

    return jsonify({'message': 'Beekeper added successfuly!'}), 201


# GET method for Recipient table
@app.route('/recipient', methods=['GET'])
def get_recipient():
    cursor = conn.cursor()
    cursor.execute('{CALL GetRecipient}')
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows]), 201

# POST method for Recipient table
@app.route('/recipient', methods=['POST'])
def add_recipient():
    data = request.get_json()
    nume_recipient = data['nume_recipient']
    numar_unitati = data['numar_unitati']
    cantitate = data['cantitate']
    unitate_cantitate = data['unitate_cantitate']
    
    cursor = conn.cursor()

    cursor.execute("""
        EXEC AddRecipient ?, ?, ?, ?;
    """, (nume_recipient, numar_unitati, cantitate, unitate_cantitate))

    if cursor.messages:
        return cursor.messages[0][0], 400

    conn.commit()
    
    return jsonify({"message": "Recipient added successfully!"}), 201


# GET method for Miere table
@app.route('/miere', methods=['GET'])
def get_miere():
    cursor = conn.cursor()
    cursor.execute('{CALL GetMiere}')
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows]), 201


@app.route('/pack_honey', methods=['POST'])
def pack_honey():
    data = request.json

    tip_miere = data.get('tip_miere')
    vechime_maxima = data.get('vechime_maxima')
    nume_recipient = data.get('nume_recipient')
    numar_unitati = data.get('numar_unitati')
    pret = data.get('pret')

    cursor = conn.cursor()

    # Validate required fields
    if not all([tip_miere, vechime_maxima, nume_recipient, numar_unitati]):
        return jsonify({'error': 'All fields required!'}), 400

    try:
        cursor.execute("""
            EXEC PackHoney ?, ?, ?, ?, ?;
        """, (tip_miere, vechime_maxima, nume_recipient, numar_unitati, pret))

        if cursor.messages:
            raise Exception(cursor.messages)

        conn.commit()

        return jsonify({'success': 'Honey packed successfully!'}), 200

    except Exception as e:
        # Handle SQL errors raised by RAISERROR in the SQL procedure
        clean_message = str(e).split('[SQL Server]')[1].split('(')[0].strip()

        return jsonify({
            'error': clean_message
        }), 400

@app.route('/produs', methods=['GET'])
def get_produs():
    cursor = conn.cursor()
    cursor.execute('{CALL GetProduse}')
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows]), 201


@app.route('/add_interventie', methods=['POST'])
def add_interventie():
    """
        Main endpoint to handle different types of operations (interventie).
        Based on the 'detalii' field, routes to the appropriate operation function.
    """
    data = request.json
    cursor = conn.cursor()

    # Extract basic intervention data
    id_apicultor = data.get("id_apicultor")
    data_interventie = data.get("data_interventie", datetime.now().date())
    observatii = data.get("observatii")
    id_familie = data.get("id_familie")
    detalii = data.get("detalii")

    # Validate required fields
    if not all([id_apicultor, data_interventie, id_familie, detalii]):
        return jsonify({'error': 'All fields required!'}), 400

    # Convert data to a JSON string
    json_data = json.dumps(data)

    try:
        # Execute the stored procedure
        cursor.execute("""
            EXEC add_interventie_from_json @json_data = ?
        """, (json_data,))

        # Check for any error messages from SQL Server
        if cursor.messages:
            raise Exception(cursor.messages)

        # Commit transaction if all operations succeed
        conn.commit()

        return jsonify({"message": "Operation successful"}), 201

    except Exception as e:
        # Handle SQL errors raised by RAISERROR in the SQL procedure
        clean_message = str(e).split('[SQL Server]')[1].split('(')[0].strip()

        return jsonify({
            'error': clean_message
        }), 400


@app.route('/vanzare', methods=['POST'])
def vanzare():
    data = request.json

    nume_produs = data.get("nume_produs")
    cantitate_ceruta = data.get("cantitate_ceruta")

    # Validate required fields
    if not all([nume_produs, cantitate_ceruta]):
        return jsonify({'error': 'All fields required for vanzare!'}), 400

    try:
        cursor = conn.cursor()

        cursor.execute("""
            EXEC VanzareProcedura @nume_produs = ?, @cantitate_ceruta = ?
        """, (nume_produs, cantitate_ceruta))

        if cursor.messages:
            raise Exception(cursor.messages)

        conn.commit()

        return jsonify({'success': 'Operation vanzare complete!'}), 201

    except Exception as e:
        # Handle SQL errors raised by RAISERROR in the SQL procedure
        clean_message = str(e).split('[SQL Server]')[1].split('(')[0].strip()

        return jsonify({
            'error': clean_message
        }), 400


@app.route('/get_interventii', methods=['GET'])
def get_interventii():
    cursor = conn.cursor()
    cursor.execute('{CALL GetInterventii}')
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows]), 201

@app.route('/get_data_fam_albine', methods=['GET'])
def get_data_fam_albine():
    cursor = conn.cursor()
    cursor.execute('{CALL GetDataFamAlbine}')
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows]), 201 


@app.route('/get_total_vanzari_produs', methods=['GET'])
def get_total_vanzari_produs():
    cursor = conn.cursor()
    cursor.execute('{CALL GET_Total_Vanzari_Produs}')
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows])


@app.route('/get_statistici_stupi', methods=['GET'])
def get_statistici_stupi():
    cursor = conn.cursor()
    cursor.execute('{CALL GET_ZV_Statistici_Operatiuni_Per_Stup_Rasa}')
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows])


@app.route('/get_data_apicultori', methods=['GET'])
def get_data_apicultori():
    cursor = conn.cursor()
    cursor.execute('{CALL GET_ZV_Experienta_Maestru_Apicultori}')
    rows = cursor.fetchall()

    conn.commit()

    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in rows])


if __name__ == '__main__':
    app.run(debug=True)