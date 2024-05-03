import csv
import mysql.connector
import os

# Set the database credentials
os.environ['MYSQL_ADDON_HOST'] = 'bushwrafohbfd3asxkvx-mysql.services.clever-cloud.com'
os.environ['MYSQL_ADDON_DB'] = 'bushwrafohbfd3asxkvx'
os.environ['MYSQL_ADDON_USER'] = 'ubgpw6ztfjpo94xf'
os.environ['MYSQL_ADDON_PASSWORD'] = 'fwlcozfw83vQQ3XGgFjW'
os.environ['MYSQL_ADDON_PORT'] = '3306'


def connect_to_db():
    """Establishes connection to the database."""
    try:
        conn = mysql.connector.connect(
            host=os.environ['MYSQL_ADDON_HOST'],
            user=os.environ['MYSQL_ADDON_USER'],
            password=os.environ['MYSQL_ADDON_PASSWORD'],
            database=os.environ['MYSQL_ADDON_DB'],
            port=int(os.environ['MYSQL_ADDON_PORT'])
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Failed to connect to database: {err}")
        exit(1)


def create_tables(cursor):
    """Creates database tables if they do not exist."""
    commands = [
        """CREATE TABLE IF NOT EXISTS ChromosomeSequence (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chromosome VARCHAR(255),
            assembly VARCHAR(255)
        )""",
        """CREATE TABLE IF NOT EXISTS LocationInfo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pos INT,
            ref VARCHAR(255),
            chromosome_id INT,
            FOREIGN KEY (chromosome_id) REFERENCES ChromosomeSequence(id)
        )""",
        """CREATE TABLE IF NOT EXISTS Variant (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rs_id VARCHAR(255),
            alt VARCHAR(255),
            variant_type VARCHAR(255),
            location_info_id INT,
            FOREIGN KEY (location_info_id) REFERENCES LocationInfo(id)
        )""",
        """CREATE TABLE IF NOT EXISTS Annotation (
            id INT AUTO_INCREMENT PRIMARY KEY,
            impact VARCHAR(255),
            consequence VARCHAR(255),
            allele VARCHAR(255),
            variant_id INT,
            FOREIGN KEY (variant_id) REFERENCES Variant(id)
        )""",
        """CREATE TABLE IF NOT EXISTS HGVSExpression (
            id INT AUTO_INCREMENT PRIMARY KEY,
            hgvs VARCHAR(255),
            variant_id INT,
            FOREIGN KEY (variant_id) REFERENCES Variant(id)
        )""",
        """CREATE TABLE IF NOT EXISTS Interpretation (
            id INT AUTO_INCREMENT PRIMARY KEY,
            clinical_significance VARCHAR(255),
            method VARCHAR(255),
            variant_origin VARCHAR(255),
            review_status VARCHAR(255),
            submitter VARCHAR(255),
            variant_id INT,
            FOREIGN KEY (variant_id) REFERENCES Variant(id)
        )""",
        """CREATE TABLE IF NOT EXISTS Disease (
            id INT AUTO_INCREMENT PRIMARY KEY,
            preferred_name VARCHAR(255)
        )""",
        """CREATE TABLE IF NOT EXISTS DiseaseVariantLink (
            disease_id INT,
            variant_id INT,
            FOREIGN KEY (disease_id) REFERENCES Disease(id),
            FOREIGN KEY (variant_id) REFERENCES Variant(id),
            PRIMARY KEY (disease_id, variant_id)
        )""",
        """CREATE TABLE IF NOT EXISTS `Database` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            URL VARCHAR(255),
            interpretation_id INT,
            FOREIGN KEY (interpretation_id) REFERENCES Interpretation(id)
        )"""
    ]

    for command in commands:
        try:
            cursor.execute(command)
        except mysql.connector.Error as err:
            print(f"An error occurred creating table: {err}")


def insert_data_from_csv(cursor, csv_file, table_name):
    """Inserts data from a CSV file into the specified table."""
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Assuming the first row is headers
            placeholders = ', '.join(['%s'] * len(headers))
            query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"
            for row in csv_reader:
                if len(row) == len(headers):
                    cursor.execute(query, tuple(row))
                else:
                    print(f"Skipping row due to column mismatch: {row}")
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
    except mysql.connector.Error as err:
        print(f"Error inserting data into {table_name}: {err}")



def main():
    conn = connect_to_db()
    if conn.is_connected():
        cursor = conn.cursor()
        create_tables(cursor)
        base_dir = '/Users/julielervagbreivik/DSG'
        try:
            # Start transaction
            conn.start_transaction()

            # Insert data for all tables
            insert_data_from_csv(cursor, f'{base_dir}/Variant.csv', 'Variant')
            insert_data_from_csv(cursor, f'{base_dir}/ChromosomeSequence.csv', 'ChromosomeSequence')
            insert_data_from_csv(cursor, f'{base_dir}/LocationInfo.csv', 'LocationInfo')
            insert_data_from_csv(cursor, f'{base_dir}/Annotation.csv', 'Annotation')
            insert_data_from_csv(cursor, f'{base_dir}/HGVSExpression.csv', 'HGVSExpression')
            insert_data_from_csv(cursor, f'{base_dir}/Interpretation.csv', 'Interpretation')
            insert_data_from_csv(cursor, f'{base_dir}/Disease.csv', 'Disease')
            insert_data_from_csv(cursor, f'{base_dir}/DiseaseVariantLink.csv', 'DiseaseVariantLink')

            # Commit all changes
            conn.commit()
            print("Data insertion completed successfully.")
        except mysql.connector.Error as err:
            print(f"Transaction failed: {err}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database!")


if __name__ == "__main__":
    main()





