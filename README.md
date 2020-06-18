# PC-Parts-Web-Scraper
A simple web scraper that crawls through multiple websites and extracts product data relating to each computer component.



## How to Setup
PRECAUTION: THIS IS ONLY TESTED FOR THE WINDOWS OS

### Prerequisites
* Install **Python** (https://www.python.org/downloads/)
* Install **Git** (https://git-scm.com/)

### Create a Virtual Environment
* Create a directory anywhere you wish.
* Open command line.
* Run the following commands:
```console
cd /your/directory/path
py -m venv (name_of_your_environment)
```

* After installing, activate your virtual environment.
```console
.(name_of_your_environment)/Scripts/activate.bat
```

### Installation
Once your virtual environment is activated and currently running, follow these steps:

* Create a directory named **(name_of_your_directory)** to store the web scrapper within **(name_of_your_environment)**.
* cd to **(name_of_your_directory)**.
* Inside **(name_of_your_directory)**, create two folders named **'pcparts'** where there's one parent and one child.
* In the parent folder, create a file titled: **scrapy.cfg**.

* Copy and paste the following text:
```
[settings]
default = pcparts.settings

[deploy]
#url = http://localhost:6800/
project = pcparts
```

* cd to the child folder.

* Run the following commands:
```console
git clone "https://github.com/johncmanuel/PC-Parts-Web-Scraper.git"
pip install -r requirements.txt
```

Inside your **name_of_your_environment** folder, your project directory should look like this:
```
* (name_of_your_directory)
  * pcparts
    * pcparts
      * ..rest of the project files
    * scrapy.cfg
```

* Run the following command to test if Scrapy works:
```console
scrapy crawl amazon
```
