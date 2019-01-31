# leccap
Download CAEN and LSA-ISS Lecture recordings. Boosted.

**Credits to [Maxim Aleska](https://github.com/maxim123/dleccap) for his great work :)**

## New features
* **Duo 2fa Support** !!
* **Concurrent download** !
* configurable concurrency and destination folder 
* Python 3 support

## Updates
* Support 2fa
* Major code rewritten.
* Got rid of some unnecessary dependencies

## Installation

### download and run
```sh
cd PATH_TO_DOWNLOADED
pip install -r requirements.txt
python leccap.py COMMANDS
```
or

### through pip
```sh
pip install leccap
leccap COMMANDS
```

## Usage 
**demo using pip installed version. use `python leccap.py` for downloaded version.**

#### Search lecture
```sh
leccap search $class $year?
```
where class can be a normal catelog number such as ***eecs281***. 

year is optional, default to current year, or enter one to download past lectures.

#### Download lecture
```sh
leccap dl $url
```
where url is in form of either: 
https://leccap.engin.umich.edu/leccap/site/XXX to download multiple recordings from a course site or
https://leccap.engin.umich.edu/leccap/viewer/r/XXX to download a single recording

**Removed canvas/ctools support since they seems deprecated, if you want to have those, shoot me an email :)**

#### Configuration
##### Update config
```sh
leccap config $key $value
```
##### Reset config
 ```sh
 leccap reset $key
```
where `$key` can be any one of :

`logins.username` (umich uniqname)

`logins.password` (umich password)

`concurrency` (number of downloads at once, default to 5, not recommending 10+, unless you live in a data center with 10Gbps ethernet.) 

`dest_path` (destination download **full** path, default to current directory)

`all` (everything, for **reset only**)
 
 ### Development
 Please post a issue or pull request if you see bugs or have any suggestions :)

 #### TODOs
 * Better download scheduling method
