CREATE SCHEMA configuration;
CREATE TABLE configuration.config (
  key VARCHAR(30) NOT NULL PRIMARY KEY,
  value VARCHAR(100) NOT NULL
);
INSERT INTO configuration.config VALUES ('app.jwt_secret', '4jPpMqZaBRpVOJsME54DtzLGclCAw7d0');

CREATE OR REPLACE FUNCTION configuration.get_config(k TEXT) RETURNS TEXT
  LANGUAGE plpgsql
  AS $$
  DECLARE 
     res TEXT := ''; 
  BEGIN
    SELECT value INTO res
      FROM configuration.config
      WHERE key = k;
    RETURN res;
  END
$$;

GRANT USAGE ON schema configuration TO PUBLIC;
GRANT SELECT ON TABLE configuration.config TO PUBLIC;
GRANT EXECUTE ON FUNCTION configuration.get_config TO PUBLIC;

