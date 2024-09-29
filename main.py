import sys
import argparse
from extract_metadata import extract_metadata
from list_files import list_files
from classify_files import classify

def main():
    parser = argparse.ArgumentParser(description="File management tool")
    parser.add_argument("--task", choices=['list', 'extract', 'classify'], required=True, help="Task to perform")
    args = parser.parse_args()

    task = args.task

    task_map = {
        'list': list_files,
        'extract': extract_metadata,
        'classify': classify
    }

    print(f"Executing task: {task}")
    task_map[task]()

if __name__ == "__main__":
    main()
