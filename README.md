# dir-sync
Sync files in the local folder with files in the remote location, e.g. Google Drive.

## Install

1. Run the following command in your command line:
```bash
pip install dir-sync
```

2. Check the version you installed:
```bash
$ dir-sync --version
Version: X.X.X
```

## Command Options
|Option|Description|Required|Default|
|------|-----------|--------|-------|
|--src-type|Source type.|Yes||
|--dst-type|Destination type.|Yes||
|--src|Source directory path. The value depends on the source type.|Yes||
|--dst|Destination directory path. The value depends on the source type.|Yes||
|--auth-key-file|Path to auth key file.|Yes||

## Filesystem Adapter
Depends on the source type and destination type, the value of source directory path and destination directory path can be vary.

### Local Filesystem
When `--src-type` or `--dst-type` is `local`, the `--src`/`--dst` must be a valid directory path in your local filesystem.

### Google Drive
When `--src-type` or `--dst-type` is `google-drive`, the `--src`/`--dst` must be a valid Google Drive directory ID. (reference: [https://developers.google.com/drive/api/v3/reference/files](https://developers.google.com/drive/api/v3/reference/files))
