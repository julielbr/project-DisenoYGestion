import csv
import mysql.connector
import os

#Database credentials as environment variables for security - move when pushing to GIThub
"""
CREDENTIALS
"""

# Connect to the database by use the environment variables
conn = mysql.connector.connect(
    host=os.environ['MYSQL_ADDON_HOST'],
    user=os.environ['MYSQL_ADDON_USER'],
    password=os.environ['MYSQL_ADDON_PASSWORD'],
    database=os.environ['MYSQL_ADDON_DB'],
    port=os.environ['MYSQL_ADDON_PORT']
)
cursor = conn.cursor()


# SQL to create tables 
create_tables_sql = """
CREATE TABLE IF NOT EXISTS ChromosomeSequence (
    chromosome VARCHAR(20),   
    assembly VARCHAR(50),    
    PRIMARY KEY (chromosome)
);
CREATE TABLE IF NOT EXISTS LocationInfo (
    pos INTEGER,
    ref VARCHAR(100),         
    chrom VARCHAR(20) REFERENCES ChromosomeSequence(chromosome),
    PRIMARY KEY (pos, ref, chrom)
);
CREATE TABLE IF NOT EXISTS Disease (
    chromosome VARCHAR,
    assembly VARCHAR,
    PRIMARY KEY (chromosome)
);
CREATE TABLE IF NOT EXISTS Interpretention(
    pos INTEGER,
    ref VARCHAR,
    chrom VARCHAR REFERENCES ChromosomeSequence(chromosome),
    PRIMARY KEY (pos, ref, chrom)
);

CREATE TABLE IF NOT EXISTS Variant (
    chromosome VARCHAR,
    assembly VARCHAR,
    PRIMARY KEY (chromosome)
);
CREATE TABLE IF NOT EXISTS Annotation (
    pos INTEGER,
    ref VARCHAR,
    chrom VARCHAR REFERENCES ChromosomeSequence(chromosome),
    PRIMARY KEY (pos, ref, chrom)
);

CREATE TABLE IF NOT EXISTS HGVSExpression (
    chromosome VARCHAR,
    assembly VARCHAR,
    PRIMARY KEY (chromosome)
);
CREATE TABLE IF NOT EXISTS Database (
    pos INTEGER,
    ref VARCHAR,
    chrom VARCHAR REFERENCES ChromosomeSequence(chromosome),
    PRIMARY KEY (pos, ref, chrom)
);
"""

# Execute the SQL to create tables
cursor.execute(create_tables_sql)

# Getting my data from the CSV file
with open('clinvar.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extract data from the CSV row
        chrom = row['CHROM']
        pos = int(row['POS'])
        ref = row['REF']
        alt = row['ALT']

        cursor.execute("INSERT INTO LocationInfo (chrom, pos, ref, alt) VALUES (%s, %s, %s, %s)", (chrom, pos, ref, alt))

conn.commit()
cursor.close()
conn.close()

conn.commit()

