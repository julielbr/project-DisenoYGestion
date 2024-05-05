import mysql.connector
import pandas as pd
import os

# database credentials 
os.environ['MYSQL_ADDON_HOST'] = 'bushwrafohbfd3asxkvx-mysql.services.clever-cloud.com'
os.environ['MYSQL_ADDON_DB'] = 'bushwrafohbfd3asxkvx'
os.environ['MYSQL_ADDON_USER'] = 'ubgpw6ztfjpo94xf'
os.environ['MYSQL_ADDON_PASSWORD'] = 'fwlcozfw83vQQ3XGgFjW'
os.environ['MYSQL_ADDON_PORT'] = '3306'


db_config = {
    'host': os.getenv('MYSQL_ADDON_HOST'),
    'user': os.getenv('MYSQL_ADDON_USER'),
    'password': os.getenv('MYSQL_ADDON_PASSWORD'),
    'database': os.getenv('MYSQL_ADDON_DB'),
    'port': os.getenv('MYSQL_ADDON_PORT')
}



host = os.getenv('MYSQL_ADDON_HOST')
dbname = os.getenv('MYSQL_ADDON_DB')
user = os.getenv('MYSQL_ADDON_USER')
password = os.getenv('MYSQL_ADDON_PASSWORD')
port = os.getenv('MYSQL_ADDON_PORT')

# Establish connection with the database
conn = mysql.connector.connect(
    host=host,
    database=dbname,
    user=user,
    password=password,
    port=port
)
cursor = conn.cursor()

# create the tables
def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS Variant (
            id INT PRIMARY KEY,
            chrom INT,
            pos BIGINT,
            rs_id INT,
            ref VARCHAR(10),
            alt VARCHAR(10)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Annotation (
            id INT PRIMARY KEY,
            impact VARCHAR(50),
            consequence VARCHAR(255),
            allele VARCHAR(100),
            variant_id INT,
            FOREIGN KEY (variant_id) REFERENCES Variant(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ChromosomeSequence (
            id INT PRIMARY KEY,
            chromosome INT,
            assembly VARCHAR(10)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Disease (
            id INT PRIMARY KEY,
            preferred_name VARCHAR(255)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS HGVSExpression (
            id INT PRIMARY KEY,
            hgvs VARCHAR(255),
            variant_id INT,
            FOREIGN KEY (variant_id) REFERENCES Variant(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Interpretation (
            id INT PRIMARY KEY,
            clinical_significance VARCHAR(50),
            method VARCHAR(100),
            variant_origin VARCHAR(100),
            review_status VARCHAR(100),
            submitter VARCHAR(100),
            variant_id INT,
            FOREIGN KEY (variant_id) REFERENCES Variant(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS LocationInfo (
            id INT PRIMARY KEY,
            pos BIGINT,
            ref VARCHAR(10),
            chromosome_id INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS LocationInfoVariantLink (
            location_info_id INT,
            variant_id INT,
            FOREIGN KEY (location_info_id) REFERENCES LocationInfo(id),
            FOREIGN KEY (variant_id) REFERENCES Variant(id)
        );
        """
    ]
    for command in commands:
        cursor.execute(command)
    conn.commit()

# Function to load data from CSV to table
def load_data_from_csv(file_path, table_name):
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))
    conn.commit()

# Create tables
create_tables()

# Load data into tables
load_data_from_csv('/Users/julielervagbreivik/DSG/Variant.csv', 'Variant')
load_data_from_csv('/Users/julielervagbreivik/DSG/Annotation.csv', 'Annotation')
load_data_from_csv('/Users/julielervagbreivik/DSG/ChromosomeSequence.csv', 'ChromosomeSequence')
load_data_from_csv('/Users/julielervagbreivik/DSG/Disease.csv', 'Disease')
load_data_from_csv('/Users/julielervagbreivik/DSG/HGVSExpression.csv', 'HGVSExpression')
load_data_from_csv('/Users/julielervagbreivik/DSG/Interpretation.csv', 'Interpretation')
load_data_from_csv('/Users/julielervagbreivik/DSG/LocationInfo.csv', 'LocationInfo')
load_data_from_csv('/Users/julielervagbreivik/DSG/LocationInfoVariantLink.csv', 'LocationInfoVariantLink')

# Close communication with the database
cursor.close()
conn.close()






