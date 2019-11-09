import configparser


# CONFIG file gets all the required parameters and their values in the config object 
config = configparser.ConfigParser()
config.read('food_warehouse.cfg')

# DROP TABLES will clean if there are any existing tables with the names 
food_desert_table_drop = "DROP TABLE IF EXISTS foods_desert CASCADE"
store_location_table_drop = "DROP TABLE IF EXISTS store_loc"
license_table_drop = "DROP TABLE IF EXISTS license"
vland_location_table_drop = "DROP TABLE IF EXISTS vland_loc"
vacant_land_table_drop = "DROP TABLE IF EXISTS vland"
staging_vland_table_drop = "DROP TABLE IF EXISTS staging_vland"
staging_foodesert_table_drop = "DROP TABLE IF EXISTS staging_foods_desert"


# Fact Table (Food Desert)
food_desert_table_create= (""" 
                                CREATE TABLE foods_desert (
                                   license_number INTEGER PRIMARY KEY, 
                                   city VARCHAR, 
                                   county VARCHAR,
                                   state VARCHAR,
                                   zip_code INTEGER NOT NULL,
                                   dba_name VARCHAR NOT NULL, 
                                   square_footage INTEGER);
""")

# dimensional table (store location)
store_location_table_create = ( """
                                   CREATE TABLE store_loc ( 
                                       zip_code INTEGER PRIMARY KEY,
                                       location VARCHAR,
                                       longitude NUMERIC,
                                       latitude NUMERIC);
""")

# dimensional table (license)
license_table_create = ("""CREATE TABLE IF NOT EXISTS license(
                                license_number INTEGER,
                                operation_type VARCHAR,
                                establishment_type VARCHAR,
                                entity_name VARCHAR NOT NULL, 
                                FOREIGN KEY (license_number) REFERENCES foods_desert (license_number));
""")

# dimensional table (vacant land location)
vland_location_table_create = ("""CREATE TABLE IF NOT EXISTS vland_loc(
                                       zip_code INTEGER PRIMARY KEY,
                                       address VARCHAR,
                                       longitude NUMERIC,
                                       latitude NUMERIC);
""")

# dimensional table (vacant land)
vacant_land_table_create = ("""CREATE TABLE IF NOT EXISTS vland(
                                    property_class INTEGER PRIMARY KEY,
                                    city VARCHAR,
                                    state VARCHAR,
                                    address VARCHAR, 
                                    property_class_description VARCHAR,
                                    owner1 VARCHAR);
""")

# in order to load the data of csv to the new database in redshift, we need to create tables which will hold the analysis 
staging_vacant_land_table_create = ("""CREATE TABLE IF NOT EXISTS staging_vland(
                                    property_class INTEGER,
                                    city VARCHAR,
                                    state VARCHAR,
                                    property_class_description VARCHAR,
                                    owner1 VARCHAR,
                                    zip_code INTEGER,
                                    address VARCHAR,
                                    longitude NUMERIC,
                                    latitude NUMERIC);
""")

staging_food_desert_table_create= (""" 
                                CREATE TABLE staging_foods_desert (
                                   license_number INTEGER, 
                                   city VARCHAR, 
                                   county VARCHAR,
                                   state VARCHAR,
                                   zip_code INTEGER,
                                   dba_name VARCHAR, 
                                   square_footage INTEGER,
                                   operation_type VARCHAR,
                                   establishment_type VARCHAR,
                                   entity_name VARCHAR,
                                   location VARCHAR,
                                   longitude NUMERIC,
                                   latitude NUMERIC);
""")

# Here copy command is used to copy all the data from csv files located on s3 to redshift tables

food_desert_copy = ("""COPY staging_foods_desert FROM {}
                           iam_role  '{}'
                          FORMAT AS CSV {};""").format(config.get("S3","FOOD_DESERT_DATA"), config.get("IAM_ROLE","ARN"), config.get("S3","FOOD_PATH"))


vacant_land_copy = ("""COPY staging_vland FROM {}
                         iam_role  '{}'
                         FORMAT AS CSV 'auto';""").format(config.get("S3","FOOD_DESERT_ANALYZED_DATA"), config.get("IAM_ROLE","ARN"), config.get("S3","VLAND_PATH"))

                        
# All the query paremeters are placed in the QUERY LISTS and are being called in the etl script which executes corresponding sql statements.

create_table_queries = [food_desert_table_create, store_location_table_create,  license_table_create, 
vland_location_table_create, vacant_land_table_create, staging_vacant_land_table_create, staging_food_desert_table_create]

drop_table_queries = [food_desert_table_drop, store_location_table_drop, license_table_drop, vland_location_table_drop, vacant_land_table_drop, staging_vland_table_drop, staging_foodesert_table_drop]

copy_table_queries = [food_desert_copy, vacant_land_copy]
