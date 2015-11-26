drop table if exists counter;

create table counter (
    counter int not null default 0,
    increment int not null default 1
);
    
