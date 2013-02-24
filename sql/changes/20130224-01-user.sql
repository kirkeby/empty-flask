create table "user"(
    id serial primary key,
    login varchar not null,
    created timestamp not null default now()
);

create unique index user_login_uniq on "user"(lower(login));
