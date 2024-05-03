import csv
from itertools import count

# Initialize an ID generator
id_gen = count(1)

# Headers based on the database schema
headers = {
    "HGVSExpression": ["id", "hgvs", "variant_id"],
    "Interpretation": ["id", "clinical_significance", "method", "variant_origin", "review_status", "submitter", "variant_id"],
    "LocationInfo": ["id", "pos", "ref", "chromosome_id"],
    "LocationInfoVariantLink": ["location_info_id", "variant_id"],
    "Variant": ["id", "chrom", "pos", "rs_id", "ref", "alt"],
}

# Create and open CSV files for writing
csv_files = {key: open(f"{key}.csv", 'w', newline='') for key in headers}
csv_writers = {key: csv.writer(file) for key, file in csv_files.items()}

# Write headers to each file
for key, writer in csv_writers.items():
    writer.writerow(headers[key])

# Open and process the VCF file
with open("test_annotated.vcf", "r") as vcf:
    for line in vcf:
        if line.startswith('#'):
            continue  
        parts = line.strip().split('\t')
        chrom, pos, rs_id, ref, alt = parts[:5]
        info = parts[7]  # The info field with annotations

        # Create entries for LocationInfo and ChromosomeSequence
        loc_id = next(id_gen)
        chrom_id = next(id_gen)  # Simplified example, in reality, chromosome IDs should be consistent for the same chromosome
        csv_writers["LocationInfo"].writerow([loc_id, pos, ref, chrom_id])

        # Create an entry for Variant
        var_id = next(id_gen)
        csv_writers["Variant"].writerow([var_id, chrom, pos, rs_id, ref, alt])

        ann_entries = info.split('ANN=')[1].split(';')[0].split(',')
        for entry in ann_entries:
            fields = entry.split('|')
            hgvs_c = fields[9]
            hgvs_p = fields[10]
            impact = fields[2]
            hgvs_expression = f"{hgvs_c}|{hgvs_p}"
            csv_writers["HGVSExpression"].writerow([next(id_gen), hgvs_expression, var_id])
            csv_writers["Interpretation"].writerow([next(id_gen), impact, "Method-Placeholder", "Origin-Placeholder", "Review-Status-Placeholder", "Submitter-Placeholder", var_id])
            csv_writers["LocationInfoVariantLink"].writerow([loc_id, var_id])

# Close 
for file in csv_files.values():
    file.close()
