# data-sync
Data synchronisation tool that chunks files from the specified input dir and sends to listening server, validating file integrity per chunk.

To test the tool, clone the repo or download the files.

To start the server:
```
python server.py
```
Send the included test file (.mov) to the server
```
python data-sync.py
```
