import subprocess

# Path to SnpEff executable
snpeff_path = "/Users/julielervagbreivik/DSG/snpEff.jar"
# Path to input VCF file
input_vcf = "test.vcf"

# Path to output annotated VCF file
output_vcf = "test_annotated.vcf"

# Command to run SnpEff annotation
command = f"java -jar {snpeff_path} -v GRCh37.75 {input_vcf} > {output_vcf}"

# Run the command
subprocess.run(command, shell=True)

print("Annotation complete!")

