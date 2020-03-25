create table robot(
serial_number	varchar(7)	PRIMARY KEY
);

create table session(
id	SERIAL	PRIMARY KEY,
date	DATE	not null,
start_position	POINT	not null,
begin_hour	TIME	null,
end_hour	TIME	null,
robot	varchar(7)		REFERENCES robot(serial_number)
);

create table resultat(
id	SERIAL	PRIMARY KEY,
angle	FLOAT (8)	not null,
coordinates	POINT	not null,
timer_hour	TIME	not null,
weather	VARCHAR (255)	not null,
humidity	INTEGER	not null,
temperature	float (4)	not null,
session	INTEGER	REFERENCES	session(id)
);