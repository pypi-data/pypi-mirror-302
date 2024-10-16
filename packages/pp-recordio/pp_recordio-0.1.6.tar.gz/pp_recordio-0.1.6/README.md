# README

`pp_recordio` is a python library that lets you store sequences of binary blobs 
and read them out efficiently. It's designed to detect and tolerate
corruptions to individual records. A common failure mode of sequential read/write
formats like this is the incomplete write; another is bitrot from long term storage.
Storing in this format helps us deal with these problems while also allowing the
underlying data to be processed in parallel using tools like Apache Beam and reducing
filesystem / database load caused by storing things as a large number of files.

You can install it using `pip` ([Pypi project here](https://pypi.org/project/pp-recordio/)):

```bash
pip install pp-recordio
```

Example Usage:

```python
# Import the module.
from pp_recordio import pp_recordio as rio

FILENAME = "test.pp_recordio"
w = rio.RecordWriter(FILENAME)
w.write(b'This is a binary blob!')
w.write(b'Individual messages can be quite big.!')
w.write(b'Protocol buffers are good to store here!')

r = rio.RecordReader(FILENAME)
for item in r.read():
  print(item)
```

## Project Goals

- [x] Sequential writing
- [x] Appending to a previously created file
- [x] Sequential reading
- [ ] Seeking while reading
- [ ] Optional compression:
  - [x] gzip
  - [ ] zstd
  - [ ] brotli
- [ ] Data corruption detected + reading can be resumed after skipping over a corrupted region (e.g _incomplete write_).
  - [x] Payload level data corruptions 
  - [ ] All data corruptions
     
### Big brain ideas that aren't on the roadmap

Param to store and compress N frames at a time instead of one at a time; good for temporally local image frames for example.

## Implementation Notes

The core implementation is done in golang and wrapped using `cgo`.

The frame is composed of a header followed by the actual data. The total frame
size is variable, depending on the size of the data being stored.

### Frame Header

- Magic Number: 4 bytes; constant value: 0xDEADBEEF. Used to identify the start
  of a frame.
- Length: 8 bytes; stores the total length of the frame (header + data).
- CRC32: 8 bytes; stores the CRC32 checksum of the data for integrity checking.
- Flags: 4 bytes; used to indicate various frame properties (e.g., compression).
- Reserved: 16 bytes; currently unused, reserved for future use.

4 + 8 + 8 + 4 + 16 = 40 bytes total overhead per stored datum.

### Alternative Design Ideas

One problem with the current design is that if there's a corrupt record whose length value was very big but actual stored data is very small, the reader will skip over many valid / records.

One way to get around this would be to chunk up user data into linked shards and have magic numbers available more frequently so that there's more tolerance to corruption.

The problem with this is just more overhead. I think we're making the correct tradeoff for a video storage service; we kind of get this if all our RecordIO entries are a fixed number of frames anyway (e.g. 10 seconds @ 10Hz = 100 frames for typical record).

## Release Notes

### Version 0.1.5

First working version.

Issues I'd like to address / fix:

- Does not tolerate corruption to the frames themselves.
- Does not support sharded paths and requires suffix to be `.pp_recordio`.
- Not thread safe.
- The underlying go library generates a ton of noisy logs. I should clean those up / remove them.
- The underlying go library has a gzip compression feature that should either be removed or exposed to the python interface. Since we typically store compressed images, I wonder if adding gzip/zstd/etc compression to individual entries is useful at all or just adding unnecessary overhead and complexity.
- We don't currently have a test case covering reads after incomplete writes. Being able to skip over incomplete writes is a critical feature.

## Releasing new version of the code

First install some prerequisites:

```bash
pip install -r requirements.txt 
```

### Compile Go Shared Objects

The go code for this project is in `/src`.

The annoying thing about distributing python wheels is that you need to compile
wheels on each machine type you intend on supporting. Golang makes it possible
to cross-compile between some platforms (e.g. Linux x86 and aarch64).

Make sure you turn on this environment variable:

```bash
export GO111MODULE=on
```

Then here are the compile commands. Run the one for your platform.

```bash
# Mac, Apple silicon.
export MACOSX_DEPLOYMENT_TARGET=11.0
GOOS=darwin GOARCH=arm64 go build -buildmode=c-shared -o pp_recordio_lib_darwin_arm64.so pp_recordio.go

# Mac, x86.
export MACOSX_DEPLOYMENT_TARGET=11.0
GOOS=darwin GOARCH=amd64 go build -buildmode=c-shared -o pp_recordio_lib_darwin_amd64.so pp_recordio.go

# Linux, x86 (most linux PCs).
GOOS=linux GOARCH=amd64 go build -buildmode=c-shared -o pp_recordio_lib_linux_amd64.so pp_recordio.go

# Linux, ARM / aarch64 (e.g. nvidia jetson).
GOOS=linux GOARCH=arm64 go build -buildmode=c-shared -o pp_recordio_lib_linux_arm64.so pp_recordio.go

# Common scenario: cross-compiling on x86 linux to linux ARM / aarch64:
sudo apt-get install gcc-aarch64-linux-gnu
export CC=aarch64-linux-gnu-gcc
CGO_ENABLED=1 GOOS=linux GOARCH=arm64 go build -buildmode=c-shared -o pp_recordio_lib_linux_arm64.so pp_recordio.go

# Windows, x86.
# Unsupported since I don't have a windows machine..
# GOOS=windows GOARCH=amd64 go build -buildmode=c-shared -o pp_recordio_lib_windows_amd64.dll pp_recordio.go
```

Once you have generated the shared objects, copy them into `//pp_recordio`.

### Compile wheels for Pypi upload

```bash
bash compile_for_pypi.sh
```

#### Upload to Pypi

```bash
twine upload dist/*
```

## Running the unit test

Python:

```bash
# Change platform string based on which system you're running the test.
PLATFORM_STRING=darwin_arm64
go build -buildmode=c-shared -o pp_recordio/pp_recordio_lib_${PLATFORM_STRING}.so src/pp_recordio.go && python -m unittest pp_recordio/pp_recordio_test.py
```

Go unit tests:

```bash
cd src
go test
```
