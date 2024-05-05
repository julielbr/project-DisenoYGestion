import csv
from itertools import count

id_gen = count(1)

# Headers based on the database schema-
headers = {
    "HGVSExpression": ["id", "hgvs", "variant_id"],
    "Interpretation": ["id", "clinical_significance", "method", "variant_origin", "review_status", "submitter", "variant_id"],
    "LocationInfo": ["id", "pos", "ref", "chromosome_id"],
    "LocationInfoVariantLink": ["location_info_id", "variant_id"],
    "Variant": ["id", "chrom", "pos", "rs_id", "ref", "alt"],
    "Annotation": ["id", "impact", "consequence", "allele", "variant_id"],
    "ChromosomeSequence": ["id", "chromosome", "assembly"],
    "Disease": ["id", "preferred_name"],
    "DiseaseVariantLink": ["disease_id", "variant_id"]
}

# Create and open CSV files for writing
csv_files = {key: open(f"{key}.csv", 'w', newline='') for key in headers}
csv_writers = {key: csv.writer(file) for key, file in csv_files.items()}


for key, writer in csv_writers.items():
    writer.writerow(headers[key])

# Dictionary to store chromosome IDs and a set to avoid duplicate location-variant links
chromosome_ids = {}
unique_loc_var_links = set()

try:
    # Open and process the VCF file
    with open("test_annotated.vcf", "r") as vcf:
        for line in vcf:
            if line.startswith('#'):
                continue   
            parts = line.strip().split('\t')
            chrom, pos, rs_id, ref, alt = parts[:5]
            info = parts[7]  

            # Ensure unique chromosome IDs
            if chrom not in chromosome_ids:
                chromosome_ids[chrom] = next(id_gen)

            chrom_id = chromosome_ids[chrom]

            loc_id = next(id_gen)
            csv_writers["LocationInfo"].writerow([loc_id, pos, ref, chrom_id])
            if (chrom_id, chrom, "GRCh37") not in unique_loc_var_links:
                csv_writers["ChromosomeSequence"].writerow([chrom_id, chrom, "GRCh37"])
                unique_loc_var_links.add((chrom_id, chrom, "GRCh37"))

            var_id = next(id_gen)
            csv_writers["Variant"].writerow([var_id, chrom, pos, rs_id, ref, alt])

            # Avoid duplicate location-variant- was 4 times all
            loc_var_key = (loc_id, var_id)
            if loc_var_key not in unique_loc_var_links:
                csv_writers["LocationInfoVariantLink"].writerow([loc_id, var_id])
                unique_loc_var_links.add(loc_var_key)

            # Extract annotations from the INFO field and proceed with other entries
            ann_entries = info.split('ANN=')[1].split(';')[0].split(',')
            for entry in ann_entries:
                fields = entry.split('|')
                hgvs_c = fields[9]
                hgvs_p = fields[10]
                impact = fields[2]
                hgvs_expression = f"{hgvs_c}|{hgvs_p}"
                csv_writers["HGVSExpression"].writerow([next(id_gen), hgvs_expression, var_id])
                csv_writers["Interpretation"].writerow([next(id_gen), impact, "Method-Placeholder", "Origin-Placeholder", "Review-Status-Placeholder", "Submitter-Placeholder", var_id])
                csv_writers["Annotation"].writerow([next(id_gen), impact, "Consequence-Placeholder", "Allele-Placeholder", var_id])
                csv_writers["Disease"].writerow([next(id_gen), "Preferred-Name-Placeholder"])
                csv_writers["DiseaseVariantLink"].writerow([next(id_gen), var_id])
finally:
    for file in csv_files.values():
        file.close()
