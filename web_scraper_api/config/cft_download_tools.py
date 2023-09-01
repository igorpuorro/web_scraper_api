#!/usr/bin/env python3

import sys
import os
import zipfile
import requests

from bs4 import BeautifulSoup

page_url = "https://googlechromelabs.github.io/chrome-for-testing/"

usage = f"""Usage:
  python {sys.argv[0]} [options]

Options:
  --chrome-version <version|latest>  Specify the Chrome version to query (use "latest" for the latest version).
  --platform <platform>              Specify the target platform.
  --download [directory]             Download Chrome files (optionally specify download directory).
  --unzip                            Unzip downloaded Chrome files (only with --download).

Check for available versions at {page_url}.
"""


def find_latest_version():
    try:
        page_response = requests.get(page_url, timeout=30)
        page_response.raise_for_status()
        html = page_response.text

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('div', class_='table-wrapper summary').table

        for row in table.tbody.find_all('tr', class_='status-ok'):
            first_column = row.th
            second_column = row.find('td')

            if first_column.a and 'stable' in first_column.a.text.lower():
                code_tag = second_column.find('code')
                if code_tag and all(c.isdigit() or c == '.' for c in code_tag.text):
                    return code_tag.text

        return None  # Return None if no matching information is found

    except requests.exceptions.RequestException as error:
        print(f"Error fetching HTML from URL: {error}")
        return None

    except Exception as error:
        print(f"Error: {error}")
        return None


# Get command line arguments
if len(sys.argv) < 5 or sys.argv[1] != '--chrome-version' or sys.argv[3] != '--platform':
    print(usage)
    sys.exit(1)

target_version = sys.argv[2]
if target_version == "latest":
    latest_version = find_latest_version()
    if latest_version is None:
        print("Latest Chrome version not found. Please check your data source.")
        sys.exit(1)
    target_version = latest_version

platform_filter = sys.argv[4]
download_mode = False
download_dir = None
unzip_mode = False

# Check if --download is present
if '--download' in sys.argv:
    download_mode = True
    download_index = sys.argv.index('--download')
    if download_index < len(sys.argv) - 1 and not sys.argv[download_index + 1].startswith('--'):
        download_dir = sys.argv[download_index + 1]
        # Check if the specified directory exists
        if not os.path.exists(download_dir):
            print(
                f"The directory '{download_dir}' does not exist. Please create it.")
            sys.exit(1)

# Check if --unzip is present
if '--unzip' in sys.argv:
    if not download_mode:
        print("The '--unzip' option can only be used with '--download'.")
        sys.exit(1)
    unzip_mode = True

# URL of the JSON data
json_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"

# Make an HTTP request to fetch the JSON data
response = requests.get(json_url, timeout=30)
if response.status_code != 200:
    print("Failed to fetch JSON data from the URL.")
    sys.exit(1)

# Load JSON data
data = response.json()

# Find matching versions and handle download/unzip mode
for version_info in data["versions"]:
    if version_info["version"] == target_version:
        for key in version_info["downloads"]:
            if key == "chrome" or key == "chromedriver":
                if download_mode:
                    if unzip_mode:
                        print(
                            f"Unzipping {key} version {target_version} files...")
                        zip_filenames = [os.path.basename(
                            download["url"]) for download in version_info["downloads"][key]]
                        zip_files_with_version = [
                            filename for filename in zip_filenames if target_version in filename]
                        if len(zip_files_with_version) == 2:
                            for zip_filename in zip_files_with_version:
                                zip_file_path = os.path.join(
                                    download_dir, zip_filename)
                                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                                    zip_ref.extractall(download_dir)
                            print(
                                f"Unzipped {key} version {target_version} files.")
                        else:
                            print(
                                f"Downloading and unzipping {key} version {target_version} files...")
                            for download in version_info["downloads"][key]:
                                if download["platform"] == platform_filter:
                                    download_url = download["url"]
                                    filename = os.path.basename(download_url)
                                    save_path = os.path.join(
                                        download_dir, filename)
                                    response = requests.get(
                                        download_url, timeout=30)
                                    if response.status_code == 200:
                                        with open(save_path, 'wb') as file:
                                            file.write(response.content)
                                        with zipfile.ZipFile(save_path, 'r') as zip_ref:
                                            zip_ref.extractall(download_dir)
                                        print(
                                            f"Downloaded and unzipped {filename} to {download_dir}")
                                    else:
                                        print(f"Failed to download {filename}")
                    else:
                        print(
                            f"Downloading {key} version {target_version} files...")
                        for download in version_info["downloads"][key]:
                            if download["platform"] == platform_filter:
                                download_url = download["url"]
                                filename = os.path.basename(download_url)
                                save_path = os.path.join(
                                    download_dir, filename)
                                response = requests.get(
                                    download_url, timeout=30)
                                if response.status_code == 200:
                                    with open(save_path, 'wb') as file:
                                        file.write(response.content)
                                    print(
                                        f"Downloaded {filename} to {download_dir}")
                                else:
                                    print(f"Failed to download {filename}")
                    print(
                        f"All {key} files have been downloaded to {download_dir}")
                else:
                    print(f"Download URLs for {key} version {target_version}:")
                    for download in version_info["downloads"][key]:
                        if download["platform"] == platform_filter:
                            print(download["url"])

if not download_mode:
    print("Use the '--download' option to actually download the files.")
