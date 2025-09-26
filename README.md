# Folder Sync Script

A simple Python script for synchronizing the contents of a **source folder** with a **replica folder**.  
It ensures that the replica is always an up-to-date copy of the source.  
The script logs all operations, supports repeated synchronization with intervals, and handles file updates/removals.

---

## Features
- Copies new and updated files from the source to the replica.
- Removes files and directories from the replica if they no longer exist in the source.
- Preserves file metadata (timestamps, permissions).
- Logs all operations to both console and a log file.
- Supports scheduled repeated synchronizations with intervals.

---

## Requirements
- Python 3.6 or higher
- No external dependencies (only standard library)

---

## Usage

```bash
python folder_sync.py <source_folder_path> <replica_folder_path> <interval_between_sync> <amount_of_sync> <log_path>
```

### Arguments:
1. `source_folder_path` – Path to the folder that should be mirrored.
2. `replica_folder_path` – Path to the folder that will become a synchronized copy of the source.
3. `interval_between_sync` – Time in seconds between synchronizations (e.g., `60` for 1 minute).
4. `amount_of_sync` – Number of synchronizations to perform.
5. `log_path` – Path to the log file where operations will be recorded.

---

## Example

```bash
python folder_sync.py ./source ./replica 60 5 ./sync.log
```

This will:
- Sync `./source` → `./replica`
- Run synchronization every **60 seconds**
- Perform it **5 times in total**
- Log all actions into `./sync.log`

---

## Logging
Each sync action is logged in the following format:

```text
2025-09-26 14:00:00 | INFO | File was copied/updated: ./replica/file.txt
2025-09-26 14:00:00 | INFO | File was removed: ./replica/old_file.txt
2025-09-26 14:00:00 | INFO | *SYNC START* - 1/5
2025-09-26 14:00:01 | INFO | *SYNC DONE* - 1/5
```

---

## Error Handling
- If the source directory does not exist → script exits with an error.
- If interval or amount are invalid → script exits with a warning.
- Any sync error is logged without stopping the script.

---

## License
This project is provided as-is, without warranty.  
You are free to use and modify it for personal or commercial purposes.
