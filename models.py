CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS volunteers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    birth_date VARCHAR(15),
    profile_url TEXT UNIQUE,
    volunteer_id VARCHAR(20),
    city VARCHAR(100),
    organization VARCHAR(70),
    social_links TEXT[]
);
"""