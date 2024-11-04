import os
from datetime import datetime, timedelta
from tqdm import tqdm
import time

def get_recent_top_level_dirs(path=".", exclude_dirs=None, days=60):
    if exclude_dirs is None:
        exclude_dirs = ["lib", "Pods"]

    cutoff_time = datetime.now() - timedelta(days=days)
    top_level_dirs = {}

    # Get the list of top-level directories, excluding specified ones
    entries = [
        entry for entry in os.scandir(path)
        if entry.is_dir() and entry.name not in exclude_dirs and not entry.name.startswith('.')
    ]

    total_dirs = len(entries)
    if total_dirs == 0:
        print("No directories to process.")
        return []

    for entry in tqdm(entries, desc="Processing directories", unit="dir"):
        dir_path = os.path.join(path, entry.name)
        latest_mtime = None
        latest_file = None

        # Walk through the directory, limit depth to current directory
        for root, dirs, files in os.walk(dir_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                except OSError:
                    continue  # Skip files that can't be accessed
                if file_mtime >= cutoff_time:
                    if not latest_mtime or file_mtime > latest_mtime:
                        latest_mtime = file_mtime
                        latest_file = file
            # Limit traversal to top-level directory
            break

        if latest_mtime:
            top_level_dirs[entry.name] = {
                "mtime": latest_mtime,
                "file": latest_file
            }
        time.sleep(0.01)  # Simulate processing time

    # Format the results with aligned brackets
    formatted_results = []
    for top_level_dir, info in sorted(top_level_dirs.items(), key=lambda x: x[1]["mtime"]):
        # Use fixed width for day (9 characters) and month (9 characters)
        formatted_time = info["mtime"].strftime("[ %-9A, %-9B %2d %Y %I:%M %p ]")
        formatted_results.append(f"{formatted_time} {top_level_dir}/{info['file']}")

    return formatted_results

excluded_directories = ["lib", "Pods"]
recent_dirs = get_recent_top_level_dirs(".", excluded_directories)

print("\nTop-level directories with modifications in the last 60 days:")
for line in recent_dirs:
    print(line)
