create database contacts

use contacts

create table tbuser
(
uid int not null auto_increment,
uname varchar(20) not null,
utel char(11),
uaddr varchar(100),
uemail varchar(100),
primary key (uid)
);
