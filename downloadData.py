import requests
import gzip
import shutil

def download_and_decompress(url, output_path):
    # Send a GET request to the URL
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f_out, gzip.GzipFile(fileobj=response.raw, mode='rb') as gz:
            shutil.copyfileobj(gz, f_out)
        print(f"File downloaded and decompressed to {output_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

# URL to the ClinVar VCF file
url = "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz"
output_path = "clinvar.vcf"
download_and_decompress(url, output_path)

