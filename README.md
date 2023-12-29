
# Voorivex Video Downloader

Meet the `Voorivex Video Downloader` – your go-to buddy for effortlessly grabbing educational videos from Voorivex Academy!

Are you tired of creating a video link one by one? Our downloader lets you snag your videos from https://voorivex.academy/ with just a command.




## Installation

First, you must clone this project on your local machine. for that, you can use the following command.

```bash
git clone https://github.com/milad-karimifard/VoorivexVideoDownloader.git
cd VoorivexVideoDownloader
```

Next, you must create a `virtual environment` for this project.

``` bash
python -m venv
```

After these steps, you can activate the `virtual environment` and install dependencies. for activate environment you can use following link.

[Virtual environment based on python document](https://docs.python.org/3/library/venv.html#how-venvs-work)


```bash
# Installation dependencies
pip install -r requirements.txt
```
    
## Parameters
<br>

| Parameter | Required |               Switch               |                         Description                          |     Usage     |
|:-----------:|:----------:|:----------------------------------:|:------------------------------------------------------------:|:-------------:|
|Username   |    ✅      |           `-u`/`--user`            |              Your username in Voorivex Academy               |  -u username  |
|Password           |    ✅    |         `-p`/`--password`          |              Your password in Voorivex Academy               |  -p password  |
|Keyword      |    ❌      |          `-k`/`--keyword`          |        It's used to filter videos based on video name        | -k my_keyword |
|Include live      |    ❌      |       `-l`/`--include_live`        |    If you want to include live videos you use this switch    |      -l       |
|Class name     |    ❌      |        `-c`/`--class_name`         | You can specify your class name if you joined multiple class | -c classname  |

## Example(s)

* Simple usage: Download all videos
``` bash
python main.py -u {your username} -p {your password}
```
<hr>

* Simple usage: Download the videos of the third session
``` bash
python main.py -u {your username} -p {your password} -k 3-
```
<hr>

* Advance usage: Download the videos of the third session in specific class
``` bash
python main.py -u {your username} -p {your password} -k 3- -c {class name}
```
