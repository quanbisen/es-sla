create database if not exists elasticsearch CHARACTER SET utf8 COLLATE utf8_general_ci;
create user elastic identified by '123456';
grant all privileges on elasticsearch.* to elastic;
create table es_sla
(
    id bigint(20) unsigned primary key auto_increment,
    from_time datetime,
    from_timestamp int unsigned,
    to_time datetime,
    to_timestamp int unsigned,
    status_code smallint unsigned,
    count smallint unsigned,
    es_index varchar(100)
);