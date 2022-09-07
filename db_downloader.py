import os
import zipfile

import requests

from ct_decompression import decompress_dcm


def get_ct_files_urls():
    with open("db_urls.txt", "r") as db_urls_file:
        return [url.rstrip() for url in db_urls_file.readlines()]


def extract_zipped_ct(ct_file_name: str):
    print(f"Extracting content...")

    with zipfile.ZipFile(ct_file_name, 'r') as zip_ref:
        zip_ref.extractall("files")
        dcm_files_path = zip_ref.namelist()

        print(f"Decompressing DICOM files...")
        [decompress_dcm(f"files/{file_path}") for file_path in dcm_files_path]


def download_ct_file(ct_file_url: str, ct_file_name: str):
    print(f"Downloading {ct_file_name}...")

    with requests.get(ct_file_url, stream=True) as download_request:
        download_request.raise_for_status()
        with open(ct_file_name, 'wb') as f:
            for chunk in download_request.iter_content(chunk_size=8192):
                f.write(chunk)


def main():
    ct_files_urls = get_ct_files_urls()

    for ct_index, ct_file_url in enumerate(ct_files_urls):
        ct_file_name = ct_file_url.split("/")[-1]

        download_ct_file(ct_file_url, ct_file_name)
        extract_zipped_ct(ct_file_name)
        os.remove(ct_file_name)  # remove zip file after download

        print(
            f"Finished download {ct_file_name} - {ct_index + 1}/{len(ct_files_urls)}\n")


if __name__ == "__main__":
    main()
