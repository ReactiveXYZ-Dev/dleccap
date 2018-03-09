# leccap
Download CAEN and LSA-ISS Lecture recordings. Boosted.

**Credits to [Maxim Aleska](https://github.com/maxim123/dleccap) for his great work :)**

## New features
* **Concurrent download** !!
* Concurrency and destination folder configurable

## Updates
* Major code rewritten, pretty much everything
* Got rid of some old dependencies

## Installation

### clone and run
```sh
python leccap/leccap.py $CMD
```
or

### through pip (Not yet...)
```sh
pip install leccap
leccap $CMD
```

## API 
**demo using pip installed version. use `python leccap/leccap.py` for cloned version**

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
 `concurreny` (number of downloads at once, default to 5) 
 `dest_path` (destination download **full** path, default to current directory)
 
 ### Development
 Please post a github issue or pull request if you see bugs :)

 #### TODOs
 * Python 3 support
 * pip support
