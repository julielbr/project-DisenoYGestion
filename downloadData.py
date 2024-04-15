import requests
import gzip
import shutil

class GenomicDataDownloader:
    def __init__(self, url, filename, size_limit):
        self.url = url
        self.filename = filename
        self.size_limit = size_limit  # Size limit in bytes

    def download_file(self):
        try:
            with requests.head(self.url) as r:  # Send a HEAD request to get file size
                file_size = int(r.headers.get('Content-Length', 0))
            
            if file_size > self.size_limit:
                print(f"File exceeds the size limit of {self.size_limit} bytes.")
                return

            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                with open(self.filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            print("Download completed successfully!")
            self.decompress_file()
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")

    def decompress_file(self):
        decompressed_filename = self.filename.rstrip('.gz')
        with gzip.open(self.filename, 'rb') as f_in:
            with open(decompressed_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"File decompressed as {decompressed_filename}")

if __name__ == "__main__":
    clinvar_url = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz'
    output_path = 'clinvar.vcf.gz'
    max_file_size = 100 * 1024 * 1024  # 100 MB size limit bc problems with git...
    downloader = GenomicDataDownloader(clinvar_url, output_path, max_file_size)
    downloader.download_file()