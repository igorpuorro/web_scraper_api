# Web Scraper API

## Web Scraper API's Documentation

https://igorpuorro.github.io/web_scraper_api/

## Installing with Docker on Linux or WSL 2

1\. Clone the main branch:

```
    git clone https://github.com/igorpuorro/web_scraper_api.git
```

2\. Change to the root directory:

```
    cd web_scraper_api/
```

3\. Generate SSH keys to connect to the container:

```
    ./ssh_tools.sh --keygen
```

4\. Build an Ubuntu Linux Docker image:

```
    ./docker_tools.sh --build-image web-scraper-api ./web_scraper_api/
```

5\. Start the Docker container:

```
    ./docker_tools.sh --start-container
```

6\. Connect to the container:

```
    ./ssh_tools.sh --connect-to-container
```

7\. Proceed to [step 6 on "Installing on Ubuntu Linux."](#step-6).

## Installing with Docker on Windows

1\. Clone the main branch and disable line ending conversion:

```
    git config --global core.autocrlf false
    git clone https://github.com/igorpuorro/web_scraper_api.git
```

2\. Change to the root directory:

```
    cd .\web_scraper_api
```

3\. Generate SSH keys to connect to the container:

```
    .\ssh_tools.bat --keygen
```

4\. Build an Ubuntu Linux Docker image:

```
    .\.docker_tools.bat --build-image web-scraper-api .\web_scraper_api
```

5\. Start the Docker container:

```
    .\docker_tools.bat --start-container
```

6\. Connect to the container:

```
    .\ssh_tools.bat --connect-to-container
```

7\. Proceed to [step 6 on "Installing on Ubuntu Linux."](#step-6).

## Installing on Ubuntu Linux or WSL 2 running Ubuntu Linux

Recommended version >= Ubuntu 22.04.3 LTS (Jammy Jellyfish)

1\. Clone the main branch:

```
    git clone https://github.com/igorpuorro/web_scraper_api.git
```

2\. Change to the root directory:

```
    cd web_scraper_api/
```

3\. Install Chrome for testing dependencies:

```
    cat web_scraper_api/config/ubuntu-packages.txt | sudo xargs apt install -y
```

4\. **Optionally** create a Python Virtual Environment (venv):

```
    python3 -m venv .venv
    source .venv/bin/activate
```

5\. Install App requirements:

```
    pip3 install -r web_scraper_api/config/requirements.txt
```

<a name="step-6"></a>6\. Change to the App directory:

```
    cd web_scraper_api/
```

7\. Install the latest version of Chrome for Testing along with ChromeDriver:

This script is a tool to download the specified version of Chrome for Testing.

When the ```--chrome-version``` option is used along with ```latest``` as an argument, it will try to look up for the latest stable version available. If the script fails to find it, visit the website, check for the most reliable version and run the script again with the version as an argument.

https://googlechromelabs.github.io/chrome-for-testing/

```
    ./config/cft_download_tools.py --chrome-version latest --platform linux64 --download ./selenium/ --unzip
```

8\. Start the App running uWSGI:

```
    uwsgi --ini config/uwsgi.ini
```
