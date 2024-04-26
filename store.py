import csv
import mysql.connector
import os

# Set the database credentials to my server 
os.environ['MYSQL_ADDON_HOST'] = 'bizreff5de77axdtjcs2-mysql.services.clever-cloud.com'
os.environ['MYSQL_ADDON_DB'] = 'bizreff5de77axdtjcs2'
os.environ['MYSQL_ADDON_USER'] = 'uuftcemjcreyfh8h'
os.environ['MYSQL_ADDON_PASSWORD'] = 'oXDpPPwWGj6J4ot9CHyK'
os.environ['MYSQL_ADDON_PORT'] = '3306'

try:
    # Connect to the database
    conn = mysql.connector.connect(
        host=os.environ['MYSQL_ADDON_HOST'],
        user=os.environ['MYSQL_ADDON_USER'],
        password=os.environ['MYSQL_ADDON_PASSWORD'],
        database=os.environ['MYSQL_ADDON_DB'],
        port=int(os.environ['MYSQL_ADDON_PORT'])
    )
    cursor = conn.cursor()

    # Create all the tables
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS ChromosomeSequence (
    chromosome VARCHAR(255) NOT NULL, 
    assembly VARCHAR(50), 
    PRIMARY KEY (chromosome)
    );

    CREATE TABLE IF NOT EXISTS LocationInfo (
        pos INT NOT NULL, 
        ref VARCHAR(255) NOT NULL, 
        chrom VARCHAR(255) NOT NULL, 
        PRIMARY KEY (pos, ref, chrom), 
        FOREIGN KEY (chrom) REFERENCES ChromosomeSequence(chromosome)
    );

    CREATE TABLE IF NOT EXISTS Disease (
        preferred_name VARCHAR(255) NOT NULL, 
        PRIMARY KEY (preferred_name)
    );

    CREATE TABLE IF NOT EXISTS Interpretation (
        clinical_significance VARCHAR(255), 
        method VARCHAR(255), 
        variant_origin VARCHAR(255), 
        review_status VARCHAR(255), 
        submitter VARCHAR(255), 
        pos INT NOT NULL, 
        ref VARCHAR(255) NOT NULL, 
        chrom VARCHAR(255) NOT NULL, 
        PRIMARY KEY (clinical_significance, method, variant_origin),
        FOREIGN KEY (pos, ref, chrom) REFERENCES LocationInfo(pos, ref, chrom)
    );

    CREATE TABLE IF NOT EXISTS Variant (
        variant_rs_id VARCHAR(50) NOT NULL, 
        alt VARCHAR(255), 
        variant_type VARCHAR(50), 
        pos INT NOT NULL, 
        ref VARCHAR(255) NOT NULL,  
        chrom VARCHAR(20) NOT NULL, 
        PRIMARY KEY (variant_rs_id),
        FOREIGN KEY (pos, ref, chrom) REFERENCES LocationInfo(pos, ref, chrom)
    );

    CREATE TABLE IF NOT EXISTS Annotation (
        impact VARCHAR(255), 
        consequence VARCHAR(255), 
        allele VARCHAR(255), 
        pos INT NOT NULL, 
        ref VARCHAR(255) NOT NULL, 
        chrom VARCHAR(255) NOT NULL, 
        PRIMARY KEY (impact, consequence, allele),
        FOREIGN KEY (pos, ref, chrom) REFERENCES LocationInfo(pos, ref, chrom)
    );

    CREATE TABLE IF NOT EXISTS HGVSExpression (
        hgvs VARCHAR(255) NOT NULL, 
        variant_rs_id VARCHAR(50) NOT NULL, 
        PRIMARY KEY (hgvs),
        FOREIGN KEY (variant_rs_id) REFERENCES Variant(variant_rs_id)
    );

    CREATE TABLE IF NOT EXISTS DatabaseTable (
        name VARCHAR(255) NOT NULL, 
        URL VARCHAR(255), 
        PRIMARY KEY (name)
    );

    """
    for create_table_query in create_tables_sql.strip().split(';'):
        if create_table_query:
            cursor.execute(create_table_query)
    conn.commit()

    # Insert data into tables from the CSV file
    with open('clinvar.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            chrom = row['CHROM']
            pos = int(row['POS'])
            ref = row['REF']
            alt = row['ALT']
            allele_id = row['ALLELEID']
            rs_id = row['ID']
            clinical_significance = row['CLNSIG']

            cursor.execute("INSERT INTO ChromosomeSequence (chromosome) VALUES (%s) ON DUPLICATE KEY UPDATE chromosome=chromosome", (chrom,))
            cursor.execute("INSERT INTO LocationInfo (pos, ref, chrom) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE pos=pos, ref=ref, chrom=chrom", (pos, ref, chrom))
            cursor.execute("INSERT INTO Variant (variant_rs_id, alt, variant_type, pos, ref, chrom) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE variant_rs_id=variant_rs_id", (rs_id, alt, 'SNP', pos, ref, chrom))
            cursor.execute("INSERT INTO Interpretation (clinical_significance, method, variant_origin, review_status, submitter, pos, ref, chrom) VALUES (%s, 'Not provided', 'Not provided', 'Not provided', 'Not provided', %s, %s, %s) ON DUPLICATE KEY UPDATE clinical_significance=clinical_significance", (clinical_significance, pos, ref, chrom))
            
            conn.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()





