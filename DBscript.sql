create table Event(
    EventID INTEGER PRIMARY KEY AUTOINCREMENT,
    Place varchar NOT NULL,
    HostID int NOT NULL,
    Content varchar NOT NULL,
    Name varchar NOT NULL,
    datetime DATETIME NOT NULL,
    FOREIGN KEY(hostID)REFERENCES Host(HOSTid)
    );

create table Invitation(
    InvitationID INTEGER PRIMARY KEY AUTOINCREMENT,
    GuestUserID int NOT NULL,
    EventID int NOT NULL,
    FOREIGN KEY(EventID)REFERENCES Event(EventID),
    FOREIGN KEY(GuestUserID)REFERENCES User(UserID)
    );

create table User(
    UserID varchar NOT NULL,
    Name varchar NOT NULL,
    Email varchar NOT NULL UNIQUE,
    PhoneNumber int NOT NULL UNIQUE,
    PRIMARY KEY(UserID));

create table Contact(
    ContactID INTEGER PRIMARY KEY AUTOINCREMENT, 
    HOSTid int NOT NULL,
    CONTACTuserID int NOT NULL,
    FOREIGN KEY(CONTACTuserID)REFERENCES User(UserID),
    FOREIGN KEY(hostID)REFERENCES Host(hostID));

create table Host(
    hostID varchar PRIMARY KEY,
    Name varchar NOT NULL UNIQUE,
    Email varchar NOT NULL UNIQUE,
    Password varchar
);
