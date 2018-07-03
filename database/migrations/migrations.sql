-- API definition
-- This is exposed by PostgREST
CREATE SCHEMA api;
CREATE TABLE api.todos (
  id SERIAL PRIMARY KEY,
  done BOOLEAN NOT NULL DEFAULT FALSE,
  task TEXT NOT NULL,
  due TIMESTAMPTZ
);

-- Anonymous user
CREATE ROLE web_anon NOLOGIN;
GRANT web_anon TO postgres;

GRANT USAGE ON SCHEMA api TO web_anon;
GRANT SELECT ON api.todos TO web_anon;

CREATE ROLE todo_user NOLOGIN;
GRANT todo_user TO postgres;

GRANT USAGE ON SCHEMA api TO todo_user;
GRANT ALL ON api.todos TO todo_user;
GRANT USAGE, SELECT ON SEQUENCE api.todos_id_seq TO todo_user;

-- Authentication schema
CREATE SCHEMA auth;
-- Both web_anon and todo_user can user the authentication schema
GRANT USAGE ON SCHEMA auth TO web_anon, todo_user;

CREATE OR REPLACE FUNCTION auth.check_token() RETURNS VOID
  LANGUAGE plpgsql
  AS $$
BEGIN
  IF current_setting('request.jwt.claim.email', true) =
     'disgruntled@mycompany.com' THEN
    RAISE insufficient_privilege
      USING hint = 'Nope, we are on to you';
  END IF;
END
$$;

CREATE SCHEMA backend;
CREATE TABLE backend.users (
  id SERIAL PRIMARY KEY,
  uname TEXT NOT NULL,
  pw TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TYPE jwt_token AS (
  token TEXT
);

CREATE EXTENSION pgjwt CASCADE;

GRANT USAGE ON SCHEMA backend TO web_anon;
GRANT SELECT ON TABLE backend.users TO web_anon;
CREATE FUNCTION api.login(username TEXT, password TEXT) RETURNS public.jwt_token
    LANGUAGE sql
    SECURITY DEFINER
    SET search_path = public
    AS $$
  SELECT public.sign(
    row_to_json(r),
    configuration.get_config('app.jwt_secret')
    )
  AS token
  FROM (
    SELECT
      users.role AS role,
      users.uname AS username,
      extract(epoch FROM NOW())::integer + 300 AS exp
      FROM backend.users AS users
      WHERE users.uname = username AND users.pw = password
      LIMIT 1
  ) r;
$$;

grant execute on function api.login(text, text) to web_anon;
