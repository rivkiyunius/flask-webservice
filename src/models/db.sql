CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    name varchar (128),
    email varchar (128),
    password varchar (128),
    create_at date,
    modified_at date
);

CREATE TABLE blogposts(
    id SERIAL PRIMARY KEY NOT NULL,
    title varchar (128),
    contents varchar (128),
    create_at date,
    modified_at date,
    owner_id int not null,
    foreign key (owner_id) references users(id)
);