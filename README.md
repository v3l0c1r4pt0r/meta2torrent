# meta2torrent

Python script to convert meta files as left by rtorrent into valid torrent files

## Usage

Clone and install dependencies:

```
git clone https://github.com/v3l0c1r4pt0r/meta2torrent
cd meta2torrent
pip install -r requirements.txt
```

Convert with:

```
./meta2torrent.py A8F2B5E67788128CD4F23DCFCB5826F2A5021A07.meta A8F2B5E67788128CD4F23DCFCB5826F2A5021A07.torrent
```
or if you want to have some trackers added (--announce can be used many times):

```
./meta2torrent.py --announce 'udp%3A//tracker.opentrackr.org%3A1337/announce' A8F2B5E67788128CD4F23DCFCB5826F2A5021A07.meta A8F2B5E67788128CD4F23DCFCB5826F2A5021A07.torrent
```

## Command line options

```
usage: meta2torrent [-h] [--announce ANNOUNCE] meta torrent

Convert rtorrent' meta file into valid torrent

positional arguments:
  meta                 meta file to convert
  torrent              torrent file to create

options:
  -h, --help           show this help message and exit
  --announce ANNOUNCE  add to announce list
```
