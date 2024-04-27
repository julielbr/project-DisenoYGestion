import csv

"""Class to transform the data from the annotated vcf file to an csv file"""
def parse_info(info):
    info_dict = {}
    for entry in info.split(';'):
        key_value = entry.split('=')
        if len(key_value) == 2:
            key, value = key_value
            info_dict[key] = value
    return info_dict

# Function that takes a VCF file and transform it to a CSV file
def transform_vcf_to_csv(vcf_filename, csv_filename):
    with open(vcf_filename, 'r') as vcf_file, open(csv_filename, 'w', newline='') as csv_file:
        # Define the column headers for the CSV file
        fieldnames = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'ALLELEID', 'CLNDISDB', 'CLNDN', 'CLNHGVS', 'CLNSIG', 'CLNVI']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        

        for line in vcf_file:
            if not line.startswith('#'):
                columns = line.strip().split('\t')
                info_dict = parse_info(columns[7])
                # Create a dictionary representing the current row of data
                row = {
                    'CHROM': columns[0],
                    'POS': columns[1],
                    'ID': columns[2],
                    'REF': columns[3],
                    'ALT': columns[4],
                    'QUAL': columns[5],
                    'FILTER': columns[6],
                    'ALLELEID': info_dict.get('ALLELEID', ''),
                    'CLNDISDB': info_dict.get('CLNDISDB', ''),
                    'CLNDN': info_dict.get('CLNDN', ''),
                    'CLNHGVS': info_dict.get('CLNHGVS', ''),
                    'CLNSIG': info_dict.get('CLNSIG', ''),
                    'CLNVI': info_dict.get('CLNVI', '')
                }
                
                writer.writerow(row)

#!! remember to cange from the test to the clinvar_annotated.vcf file!
transform_vcf_to_csv('clinvar_annotated.vcf', 'clinvar.csv')

