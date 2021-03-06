create database socialNetwork;
USE socialNetwork;

drop table if exists Account;
drop table if exists user_group;
drop table if exists Follower;
drop table if exists Post_Tag;
drop table if exists User_post;
drop table if exists Follow_Tag;
drop table if exists Group_members;

create table Account(
    account_ID int(11) AUTO_INCREMENT primary key, 
    account_Name varchar(100), 
    password varchar(100),
    firstName varchar(100),
    lastName varchar(100), 
    sex varchar(20), 
    birthdate date,
    lastLoginTime timestamp DEFAULT CURRENT_TIMESTAMP
);
create table user_group(
    group_ID int(11) AUTO_INCREMENT primary key, 
    group_Name varchar(100), 
    description varchar(100)
);
create table Follower(
    account_ID int(11),
    account_Name varchar(100),
    follower_ID int(11),
    follower_Name varchar(100)
);
create table Post_Tag(
    tag_Name varchar(100), 
    post_ID int(11)
);
create table User_post(
    post_ID int(11) AUTO_INCREMENT primary key, 
    post_timestamp timestamp DEFAULT CURRENT_TIMESTAMP,
    account_ID int(11),
    message varchar(186), 
    thumbs int(11) DEFAULT 0, 
    is_read int(11) DEFAULT 0,
    parent_ID int(11) DEFAULT 0
);
create table Follow_Tag(
    tag_Name varchar(100),
    account_ID int(11)
);
create table Group_members(
    group_ID int(11),
    account_ID int(11)
);

SOURCE populate sample data
-- import Sample Tweets Data
-- use socialNetwork;
-- INSERT INTO `Account`(account_Name,password) VALUES('Jond1','ps1'),('bawang','sad1'),('r269zhang','ps123'),('bawang2','12345');
-- INSERT INTO `Follow_Tag`(tag_Name,account_ID) VALUES('tag_test',6);
-- delete from Follower;
-- INSERT INTO `Follower`(account_ID, account_Name, follower_ID, follower_Name) VALUES(5,'bawang',7,'bawang2')



