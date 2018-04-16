-- API definition
-- This is exposed by PostgREST
create schema api;
create table api.todos (
  id serial primary key,
  done boolean not null default false,
  task text not null,
  due timestamptz
);

-- Anonymous user
create role web_anon nologin;
grant web_anon to postgres;

grant usage on schema api to web_anon;
grant select on api.todos to web_anon;

create role todo_user nologin;
grant todo_user to postgres;

grant usage on schema api to todo_user;
grant all on api.todos to todo_user;
grant usage, select on sequence api.todos_id_seq to todo_user;

-- Authentication schema
create schema auth;
-- Both web_anon and todo_user can user the authentication schema
grant usage on schema auth to web_anon, todo_user;

create or replace function auth.check_token() returns void
  language plpgsql
  as $$
begin
  if current_setting('request.jwt.claim.email', true) =
     'disgruntled@mycompany.com' then
    raise insufficient_privilege
      using hint = 'Nope, we are on to you';
  end if;
end
$$;

create schema backend;
create table backend.users (
  id serial primary key,
  uname text not null,
  pw text not null,
  role text not null
);

CREATE TYPE jwt_token AS (
  token text
);

CREATE EXTENSION pgjwt CASCADE;

ALTER DATABASE postgres SET "app.jwt_secret" TO '3jPpMqZaBRpVOJsME54DtzLGclCAw7d0';

grant usage on schema backend to web_anon;
grant select on table backend.users to web_anon;
CREATE FUNCTION api.login(username text, password text) RETURNS public.jwt_token
    LANGUAGE sql
    AS $$
  SELECT sign(
    row_to_json(r), '3jPpMqZaBRpVOJsME54DtzLGclCAw7d0' --current_setting('app.jwt_secret')
  ) AS token
  FROM (
    SELECT
      users.role as role,
      users.uname as username,
      extract(epoch from now())::integer + 300 AS exp
      FROM backend.users as users
      WHERE users.uname = username AND users.pw = password
      LIMIT 1
  ) r;
$$;

