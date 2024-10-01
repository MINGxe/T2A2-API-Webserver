# T2A2-API-Webserver
Create API Webserver application to Host different event and invite other people. 

Define the Event: Determine its purpose (e.g., networking, workshop) and set a theme. This will shape your audience and activities.

Choose Date & place: Pick a convenient time for your guests in any place/

Create invitation: Tailor the list to the event's purpose. Keep it small for intimate events or larger for public events.

Send Invitations: Use email or sms, Include details like date, time, location, and RSVP instructions.

By planning well, you can create a seamless experience for your guests.



Requirements

Python 3.x
SQLite3
Flask
Installation and Setup Instructions

1. Unpack the Zip File
First, unpack the provided zip file (containing the application code and database script) to your desired directory. You can use the following command:

bash
Copy code
unzip yourfile.zip -d /your/directory
Make sure that the server.py file (or the appropriate file name) and the SQLite script (e.g., DBscript.sql) are in the same directory.

2. Install Flask
Install Flask if it's not already installed on your system:

bash
Copy code
pip install Flask
3. Set Up the SQLite Database
To set up your SQLite database, run the following command in your terminal. Make sure that DatabaseDB.db and DBscript.sql are in the same directory as your terminal session.

bash
Copy code
sqlite3 DatabaseDB.db < DBscript.sql
This command will create the SQLite database and apply the schema defined in the DBscript.sql file.

4. Run the Flask Application
Now, it's time to start your Flask application. Use the following command in the directory where your server file is located (let's assume it's named server.py):

bash
Copy code
flask --app server run
The default port is 5000. If you want to run the server on a different port, use:

bash
Copy code
flask --app server run --port 5100
5. Access the Application
Once the Flask server is running, open your web browser and go to the following URL to interact with the app:

bash
Copy code
http://127.0.0.1:5000
(If you changed the port in step 4, replace 5000 with the new port number.)






Belows are Request manual

POST - Create User
Description: This endpoint creates a new user in the system.
URL: http://127.0.0.1:5100/user
Method: POST
Body:
json
Copy code
{
    "name": "9",
    "email": "9@apple.com",
    "phonenumber": "0412124535"
}
Usage: Send a POST request with the user’s name, email, and phone number to create a new user.




PUT - Edit User
Description: Updates an existing user's details.
URL: http://127.0.0.1:5100/user/:userid
Method: PUT
Path Variables:
userid: The email address of the user to edit (e.g., 4@apple.com).
Body:
json
Copy code
{
    "name": "4a",
    "email": "4a@apple.com",
    "phonenumber": "44444aaaaaa"
}
Usage: Modify the details of a specific user by providing their userid (email) and the updated information in the request body.





DELETE - Delete User
Description: Deletes a user from the system based on their email.
URL: http://127.0.0.1:5100/users/:userid
Method: DELETE
Path Variables:
userid: The email address of the user to delete (e.g., 7@apple.com).
Usage: Send a DELETE request with the userid to remove that user from the database.





POST - Create User Contact
Description: Creates a contact relationship between two users.
URL: http://127.0.0.1:5100/contact
Method: POST
Body:
json
Copy code
{
    "OwnerID": "test",
    "CONTACTuserID": "6@apple.com"
}
Usage: Establishes a contact between the owner (OwnerID) and another user (CONTACTuserID).





GET - Get My Contact
Description: Retrieves a list of contacts for a specific user.
URL: http://127.0.0.1:5100/getmycontact/:ownerid
Method: GET
Path Variables:
ownerid: The ID of the owner whose contacts should be retrieved (e.g., test).
Usage: Retrieves all contacts for a specific owner by sending a GET request with their ownerid.




POST - Create Events
Description: Creates a new event.
URL: http://127.0.0.1:5100/events
Method: POST
Body:
json
Copy code
[
    {
        "place": "qld",
        "hostid": "test",
        "content": "live here",
        "name": "trl",
        "datetime": "11_11_2024"
    }
]
Usage: Send a POST request with event details like place, host ID, content, name, and date/time to create a new event.




GET - Get Event
Description: Retrieves the details of a specific event based on its ID.
URL: http://127.0.0.1:5100/events/:eventid
Method: GET
Path Variables:
eventid: The ID of the event you want to retrieve (e.g., 2).
Usage: Retrieves event details by sending a GET request with the eventid.




GET - Search Events
Description: Searches for events based on a query string (content search).
URL: http://127.0.0.1:5100/events?q=here
Method: GET
Query Params:
q: Search keyword for event content (e.g., here).
Usage: Search for events where the content matches the query string by sending a GET request with a query parameter.




PUT - Edit Event
Description: Updates the details of an existing event.
URL: http://127.0.0.1:5100/events/:eventid
Method: PUT
Path Variables:
eventid: The ID of the event to update (e.g., 2).
Body:
json
Copy code
{
    "place": "Sydney Opera House",
    "hostid": "test",
    "content": "New Event Content",
    "name": "New Event Name",
    "datetime": "2024-10-05T12:00:00"
}
Usage: Update the event details using the event ID and providing new details in the request body.






DELETE - Delete Event
Description: Deletes a specific event from the system based on its ID.
URL: http://127.0.0.1:5100/event/:eventid
Method: DELETE
Path Variables:
eventid: The ID of the event to delete (e.g., 3).
Usage: Send a DELETE request with the event ID to remove that event from the system.





POST - Create Invitation
Description: Creates an invitation for an event for a specific guest user.
URL: http://127.0.0.1:5100/invitation
Method: POST
Body:
json
Copy code
{
    "eventid": 3,
    "guestuserid": "8@apple.com"
}
Usage: Send a POST request with the eventid and guestuserid to create an invitation.




GET - Get Invitation
Description: Retrieves the details of a specific invitation by its ID.
URL: http://127.0.0.1:5100/invitations/:invitationid
Method: GET
Path Variables:
invitationid: The ID of the invitation to retrieve (e.g., 4).
Usage: Retrieves invitation details by sending a GET request with the invitation ID.




DELETE - Delete Invitation
Description: Deletes an invitation by its ID.
URL: http://127.0.0.1:5100/invitations/:invitationid
Method: DELETE
Path Variables:
invitationid: The ID of the invitation to delete (e.g., 2).
Usage: Send a DELETE request with the invitation ID to remove that invitation from the system.









Module 

1. User Module
Primary Key: user_id
Attributes:
name (not null)
email (not null)
phone_number
This module manages users, storing personal information like their name, email, and phone number. It serves as the central module for all user-related data and relationships.


2. Event Module
Primary Key: event_id
Foreign Key: host_user_id (links to User)
Attributes:
place (not null)
content
name (not null)
datetime (not null)
This module contains all event-related data, such as the event’s name, place, content, and datetime. Each event is linked to a host_user_id, meaning one user is designated as the host of the event.


3. Invitation Module
Primary Key: invitation_id
Foreign Keys:
guest_user_id (links to User)
event_id (links to Event)
Attributes: None (just foreign key references)
This module manages invitations. Each invitation is a record of which user (guest_user_id) has been invited to which event (event_id). It is a junction table between users and events.


4. Contact Module
Primary Key: contact_id
Foreign Keys:
contact_owner_id (links to User)
contact_user_id (links to User)
Attributes: None (just foreign key references)
The contact module maintains a list of contacts for each user, acting as a relationship tracker between contact_owner_id and contact_user_id.





Module Relationships

1. User to Event (1
)

A user can host many events, but an event can have only one host.
Relationship: One-to-Many
User (1) ↔ Event (M)
Implementation: In the Event table, there is a foreign key host_user_id that references the user_id in the User table.



2. User to Invitation (M
)

A user can be invited to many events, and each event can invite many users.
Relationship: Many-to-Many
User (M) ↔ Invitation (M)
Event (M) ↔ Invitation (M)
Implementation: This M
relationship is resolved through the Invitation table, where each record represents a user invited to a specific event.



3. User to Contact (1
, Self-Join)

Each user can have many contacts, and each contact is another user.
Relationship: Self-referential One-to-Many
User (1) ↔ Contact (M)
Implementation: The Contact table has two foreign keys: contact_owner_id and contact_user_id, both linking to the User table. This allows each user to maintain a list of other users as contacts.




Normalization Breakdown

1st Normal Form (1NF):

.Ensure that all tables have atomic (indivisible) values, unique rows, and primary keys.

.The ERD already fulfills this requirement, with primary keys like user_id, event_id, invitation_id, and contact_id.


2nd Normal Form (2NF):

.Remove partial dependencies; ensure that all non-key attributes depend entirely on the primary key.

.Each table adheres to this rule:
In the Event table, place, name, content, and datetime depend fully on event_id.
In the User table, name, email, and phone_number depend fully on user_id.



3rd Normal Form (3NF):

.Remove transitive dependencies; non-key attributes must not depend on other non-key attributes.

.The design avoids transitive dependencies, as non-key attributes in each table depend solely on the primary key of their respective table. For example, in the Event table, no non-key attribute (like place or content) depends on another non-key attribute.





Final Design:

The modules (tables) in the ERD already align with normalized design principles up to 3NF. Here’s a final outline of the normalized table structure and relationships:

Tables:
.User (user_id, name, email, phone_number)
.Event (event_id, place, content, name, datetime, host_user_id)
.Invitation (invitation_id, guest_user_id, event_id)
.Contact (contact_id, contact_owner_id, contact_user_id)



Relationships:

.User ↔ Event: 1
(A user hosts many events)

.User ↔ Invitation ↔ Event: M
(Many users can be invited to many events)

.User ↔ Contact: Self-referential 1
(Users can have contacts who are also users)

This normalized structure ensures minimal redundancy, efficient data storage, and consistent relationships across the modules.