# PC-Parts-Web-Scraper
A simple web scraper that crawls through multiple websites and extracts product data relating to each computer component.



## How to Set-up
PRECAUTION: THIS IS ONLY TESTED FOR THE WINDOWS OS

### Prerequisites
* Install Python (https://www.python.org/downloads/)
* Install git (https://git-scm.com/)

### Create a Virtual Environment
* Create a directory anywhere you wish.
* Open command line
* Run the following commands:
```console
cd /your/directory/path
py -m venv (name_of_your_environment)
```

* After installing, activate your virtual environment
```console
.(name_of_your_environment)/Scripts/activate.bat
```

### Installation
Once your virtual environment is activated and currently running, follow these steps:

* Create a directory named (name_of_your_directory) to store the web scrapper within (name_of_your_environment).
* Open command line and cd to (name_of_your_directory).
* Run the following commands:

```console
git clone "https://github.com/johncmanuel/PC-Parts-Web-Scraper.git"
pip install -r requirements.txt
```

* After everything is installed, cd to /pcparts (it should contain a folder with the same name and a .cfg file)
* Run the following command to test if Scrapy works:

```console
scrapy crawl amazon
```
