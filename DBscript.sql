create table Event(
    EventID INTEGER PRIMARY KEY AUTOINCREMENT,
    Place varchar NOT NULL,
    HostID int NOT NULL,
    Content varchar NOT NULL,
    Name varchar NOT NULL,
    datetime DATETIME NOT NULL,
    FOREIGN KEY(HostID)REFERENCES User(UserID)
    );

create table Invitation(
    InvitationID INTEGER PRIMARY KEY AUTOINCREMENT,
    GuestUserID varchar NOT NULL,
    EventID int NOT NULL,
    FOREIGN KEY(EventID)REFERENCES Event(EventID),
    FOREIGN KEY(GuestUserID)REFERENCES User(UserID)
    );

create table User(
    UserID varchar NOT NULL,
    Name varchar NOT NULL,
    Email varchar NOT NULL UNIQUE,
    PhoneNumber varchar NOT NULL UNIQUE,
    PRIMARY KEY(UserID));

create table Contact(
    ContactID INTEGER PRIMARY KEY AUTOINCREMENT, 
    OwnerID varchar NOT NULL,
    CONTACTuserID varchar NOT NULL,
    FOREIGN KEY(CONTACTuserID)REFERENCES User(UserID),
    FOREIGN KEY(OwnerID)REFERENCES User(UserID));




INSERT INTO User (
    UserID, 
    Name,
    Email,
    PhoneNumber
)
VALUES (
    "test",
    "test user",
    "test@example.com",
    "040000000"
);