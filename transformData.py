import csv
"Class to transform the data from the annotated vcf file to an csv file"
def parse_info(info):
    info_dict = {}
    for entry in info.split(';'):
        key_value = entry.split('=')
        if len(key_value) == 2:
            key, value = key_value
            info_dict[key] = value
    return info_dict

def transform_vcf_to_csv(vcf_filename, csv_filename):
    with open(vcf_filename, 'r') as vcf_file, open(csv_filename, 'w', newline='') as csv_file:
        fieldnames = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'ALLELEID', 'CLNDISDB', 'CLNDN', 'CLNHGVS', 'CLNSIG', 'CLNVI']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        

        for line in vcf_file:
            if not line.startswith('#'):
                columns = line.strip().split('\t')
                info_dict = parse_info(columns[7])
                
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


transform_vcf_to_csv('clinvar_annotated.vcf', 'clinvar.csv')

