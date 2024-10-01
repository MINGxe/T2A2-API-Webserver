from flask import Flask, g, jsonify, request
import sqlite3
import re

app = Flask(__name__)

#-----------------------------DATABASE FUNCTION------------------------------

DATABASE = 'PrimaryDB.db'

def get_db():
    try:
        db = getattr(g,'_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            db.execute('PRAGMA foreign_keys = ON;')
            db.row_factory = sqlite3.Row
        return db
    except sqlite3.Error as e:
        return jsonify({"error": "Database connection failed", "details": str(e)}), 500

def query_db(query, args=(), one=False):
    try:
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.Error as e:
        return jsonify({"error": "Database query failed", "details": str(e)}), 500

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#-----------------------------VALIDATION FUNCTIONS------------------------------

def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

def is_valid_phone(phonenumber):
    return len(phonenumber) >= 10 and phonenumber.isdigit()

#-----------------------------USER ROUTE------------------------------

@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        userid = email
        phonenumber = data.get('phonenumber')

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        if phonenumber and not is_valid_phone(phonenumber):
            return jsonify({"error": "Invalid phone number"}), 400

        db = get_db()
        db.execute('INSERT INTO User(UserID, Name, Email, PhoneNumber) VALUES (?,?,?,?)', (userid, name, email, phonenumber))
        db.commit()
        return jsonify({"message": "User added successfully"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to add user", "details": str(e)}), 500

@app.route('/user/<string:userid>', methods=['PUT'])
def edit_user(userid):
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        phonenumber = data.get('phonenumber')

        if not name or not email:
            return jsonify({"error": "Name and email are required fields"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        if phonenumber and not is_valid_phone(phonenumber):
            return jsonify({"error": "Invalid phone number"}), 400

        db = get_db()
        db.execute('''
            UPDATE User
            SET Name = ?, Email = ?, PhoneNumber = ?
            WHERE UserID = ?
        ''', (name, email, phonenumber, userid))
        db.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to update user", "details": str(e)}), 500

@app.route('/user/<string:userid>', methods=['DELETE'])
def delete_user(userid):
    try:
        db = get_db()

        # Check if the user exists
        user = query_db('SELECT * FROM User WHERE UserID = ?', [userid], one=True)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.execute('DELETE FROM User WHERE UserID = ?', [userid])
        db.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to delete user", "details": str(e)}), 500


        

#-----------------------------CONTACT ROUTE------------------------------

@app.route('/contact', methods=['POST'])
def create_contact():
    try:
        data = request.get_json()

        ownerid = data.get('OwnerID')
        userid = data.get('CONTACTuserID')

        if not ownerid or not userid:
            return jsonify({"error": "OwnerID and ContactUserID are required"}), 400

        if ownerid == userid:
            return jsonify({"error": "OwnerID and ContactUserID cannot be the same"}), 400

        db = get_db()
        db.execute('INSERT INTO Contact(OwnerID, CONTACTuserID) VALUES (?,?)', (ownerid, userid))
        db.commit()
        return jsonify({"message": "Contact created successfully"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to create contact", "details": str(e)}), 500

@app.route('/contacts/<string:CONTACTuserID>', methods=['DELETE'])
def delete_contact(CONTACTuserID):
    try:
        db = get_db()
        db.execute('DELETE FROM Contact WHERE CONTACTuserID = ?', [CONTACTuserID])
        db.commit()
        return jsonify({"message": "Contact deleted successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to delete contact", "details": str(e)}), 500
    

@app.route('/getmycontact/<string:ownerid>', methods=['GET'])
def get_my_contact(ownerid):
    try:
        # Validate if the owner exists
        owner = query_db('SELECT * FROM User WHERE UserID = ?', [ownerid], one=True)
        if not owner:
            return jsonify({"error": "Owner not found"}), 404

        contacts = query_db('SELECT * FROM Contact WHERE OwnerID = ?', [ownerid])
        if not contacts:
            return jsonify({"message": "No contacts found for this owner"}), 200

        return jsonify([dict(contact) for contact in contacts]), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to retrieve contacts", "details": str(e)}), 500

#-----------------------------EVENT ROUTE------------------------------

@app.route('/events', methods=['POST'])
def create_events():
    try:
        data = request.get_json()
        
        # Validating that all required fields are present
        if not all(event.get('place') and event.get('hostid') and event.get('content') and event.get('name') and event.get('datetime') for event in data):
            return jsonify({"error": "All fields (place, hostid, content, name, datetime) are required for every event"}), 400

        events_values = [(event['place'], event['hostid'], event['content'], event['name'], event['datetime']) for event in data]

        query = 'INSERT INTO Event(Place, HostID, Content, Name, datetime) VALUES (?,?,?,?,?)'
        db = get_db()
        db.executemany(query, events_values)
        db.commit()
        return jsonify({"message": "Events added successfully"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to create events", "details": str(e)}), 500

@app.route('/events/<int:eventid>', methods=['GET'])
def get_event(eventid):
    try:
        event = query_db('SELECT eventid, Place, HostID, Content, Name, datetime FROM Event WHERE eventid = ?', [eventid], one=True)
        if not event:
            return jsonify({"error": "Event not found"}), 404

        return jsonify({
            "event_id": event['eventid'],
            "name": event['Name'],
            "content": event['Content'],
            "hostid": event['HostID'],
            "datetime": event['datetime'],
            "place": event['Place']
        }), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to retrieve event", "details": str(e)}), 500

@app.route('/events/<int:eventid>', methods=['DELETE'])
def delete_event(eventid):
    try:
        db = get_db()

        # Check if the event exists
        event = query_db('SELECT * FROM Event WHERE eventid = ?', [eventid], one=True)
        if not event:
            return jsonify({"error": "Event not found"}), 404

        db.execute('DELETE FROM Event WHERE eventid = ?', [eventid])
        db.commit()

        return jsonify({"message": "Event deleted successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to delete event", "details": str(e)}), 500

@app.route('/events/<int:eventid>', methods=['PUT'])
def update_event(eventid):
    try:
        data = request.get_json()

        place = data.get('place')
        hostid = data.get('hostid')
        content = data.get('content')
        name = data.get('name')
        datetime = data.get('datetime')

        if not place or not hostid or not content or not name or not datetime:
            return jsonify({"error": "All fields (place, hostid, content, name, datetime) are required"}), 400

        db = get_db()
        db.execute('''
            UPDATE Event
            SET Place = ?, HostID = ?, Content = ?, Name = ?, datetime = ?
            WHERE eventid = ?
        ''', (place, hostid, content, name, datetime, eventid))
        db.commit()
        return jsonify({"message": "Event updated successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to update event", "details": str(e)}), 500


#-----------------------------END ROUTE------------------------------

#-----------------------------INVITATION ROUTE------------------------------

@app.route('/invitation', methods=['POST'])
def create_invitation():
    try:
        data = request.get_json()

        eventid = data.get('eventid')
        guestuserid = data.get('guestuserid')

        if not eventid or not guestuserid:
            return jsonify({"error": "EventID and GuestUserID are required"}), 400

        db = get_db()
        db.execute('INSERT INTO Invitation(eventid, GuestUserID) VALUES (?,?)', (eventid, guestuserid))
        db.commit()
        return jsonify({"message": "Invitation created successfully"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to create invitation", "details": str(e)}), 500

@app.route('/invitations/<int:invitationid>', methods=['DELETE'])
def delete_invitation(invitationid):
    try:
        db = get_db()

        # Check if the invitation exists
        invitation = query_db('SELECT * FROM Invitation WHERE invitationid = ?', [invitationid], one=True)
        if not invitation:
            return jsonify({"error": "Invitation not found"}), 404

        db.execute('DELETE FROM Invitation WHERE invitationid = ?', [invitationid])
        db.commit()

        return jsonify({"message": "Invitation deleted successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to delete invitation", "details": str(e)}), 500

@app.route('/invitations/<int:invitationid>', methods=['GET'])
def get_invitation(invitationid):
    try:
        invitation = query_db('SELECT * FROM Invitation WHERE invitationid = ?', [invitationid], one=True)
        if not invitation:
            return jsonify({"error": "Invitation not found"}), 404

        return jsonify(dict(invitation)), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to retrieve invitation", "details": str(e)}), 500

#-----------------------------END ROUTE------------------------------





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
