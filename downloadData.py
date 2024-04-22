import logging
import os
import requests
import shutil
import gzip
import subprocess


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GenomicDataDownloader:
    def __init__(self, url, filename, size_limit=None):
        self.url = url
        self.filename = filename
        self.size_limit = size_limit

    def head_request(self):
        response = requests.head(self.url)
        response.raise_for_status()
        file_size = int(response.headers.get('Content-Length', 0))
        return file_size

    def download_file(self):
        file_size = self.head_request()
        if self.size_limit and file_size > self.size_limit:
            logging.error(f"File exceeds the size limit of {self.size_limit} bytes.")
            return False

        response = requests.get(self.url, stream=True)
        response.raise_for_status()
        with open(self.filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logging.info(f"Download completed successfully for {self.filename}")
        return True

    def decompress_file(self):
        decompressed_filename = self.filename.rstrip('.gz')
        with gzip.open(self.filename, 'rb') as file_in:
            with open(decompressed_filename, 'wb') as file_out:
                shutil.copyfileobj(file_in, file_out)
        logging.info(f"File decompressed as {decompressed_filename}")
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def run_annotation(self, vcf_filename):
        snpEff_command = [
            'java', '-Xmx8g', '-jar', 'snpEff/snpEff.jar',
            'GRCh37.75',
            '-strict',  
            '-ud', '5000',  
            vcf_filename
    ]
        with open('clinvar_annotated.vcf', 'w') as file_out:
            process = subprocess.run(snpEff_command, stdout=file_out, stderr=subprocess.PIPE)

        if process.returncode != 0:
            logging.error(f"SnpEff failed with return code {process.returncode}")
            logging.error(process.stderr.decode())
            return False

        logging.info("Annotation with SnpEff completed.")
        return True


if __name__ == "__main__":
    clinvar_url = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz'
    output_filename = 'clinvar.vcf.gz'
    # Increase the size limit or set it to None to have no limit
    size_limit = 100 * 1024 * 1024  # 100 MB

    downloader = GenomicDataDownloader(clinvar_url, output_filename, size_limit)

    if downloader.download_file():
        downloader.decompress_file()
        # Pass the decompressed filename to the annotation function
        if not downloader.run_annotation(output_filename.rstrip('.gz')):
            logging.error("Annotation process failed.")
