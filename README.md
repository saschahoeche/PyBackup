# Incremental Folder Backup

Author: Sascha Höche

## Overview

This script performs an incremental copy of a folder and its contents to a specified location. It identifies modified or new files in the source folder and copies them to the corresponding destination folder. The script keeps track of the copied files and generates a log file with the summary of the copied files' source and destination directories.

## Features

- Performs incremental backup of a folder and its contents
- Supports copying files and preserving their metadata (timestamps, permissions, etc.)
- Generates a log file with the summary of the copied files
- Provides progress information during the copying process
- Does not require any external libraries

## Usage

1. Ensure you have Python 3 installed on your system.
2. Clone this repository or download the `incremental_copy.py` script.
3. Open a terminal or command prompt and navigate to the directory containing the `incremental_copy.py` script.
4. Modify the source folder and destination folder paths in the `incremental_copy.py` script according to your requirements.
5. Run the script by executing the following command:

   ```shell
   python incremental_copy.py
   ```
6. The script will perform the incremental copy, display the progress information, and generate a log file in the parent folder of the destination folder.

## Example

```python
import os
import shutil
import time

# Function definitions...

if __name__ == "__main__":
    source_folder = "/path/to/source/folder"
    destination_folder = "/path/to/destination/folder"

    incremental_copy(source_folder, destination_folder)
```

## License
This project is licensed under the MIT License.



