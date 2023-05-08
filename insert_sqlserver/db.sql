
create table sensor (
	id bigint NOT NULL IDENTITY PRIMARY KEY,
	name text,
 	host text,
	port int,
	unit int,
	machine_id int default 1,
	position text,
);


create table temperature (
	id bigint NOT NULL IDENTITY PRIMARY KEY,
	temp float,
	sensor_id bigint FOREIGN KEY REFERENCES sensor(id),
	status int,
	datetime datetime default CURRENT_TIMESTAMP
);


insert into sensor (name, host, port ,unit, machine_id)
values ('sensor 7', '192.168.1.103', 8883, 7,7),
		('sensor 8', '192.168.1.103', 8883, 8,8),
		('sensor 10', '192.168.1.101', 8881, 10,10),
		('sensor 11', '192.168.1.101', 8881, 11,11),
		('sensor 12', '192.168.1.101', 8881, 12,12),
		('sensor 13', '192.168.1.102', 8882, 13,13),
		('sensor 14', '192.168.1.102', 8882, 14,13),
		('sensor 15', '192.168.1.102', 8882, 15,14),
		('sensor 16', '192.168.1.102', 8882, 16,15)


select*from sensor
select*from temperature
delete from sensor where id = 5
drop table sensor
drop table temperature