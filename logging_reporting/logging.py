import os
import argparse
import datetime
import json
import csv

def log_analysis(file_path, log_data, level="INFO", format="text"):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        "timestamp": timestamp,
        "level": level,
        "message": log_data
    }
    
    try:
        if format == "text":
            with open(file_path, 'a') as log_file:
                log_file.write(f"[{timestamp}] {level}: {log_data}\n")
        elif format == "json":
            with open(file_path, 'a') as log_file:
                json.dump(log_entry, log_file)
                log_file.write('\n')
        elif format == "csv":
            file_exists = os.path.isfile(file_path)
            with open(file_path, 'a', newline='') as log_file:
                writer = csv.DictWriter(log_file, fieldnames=log_entry.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")

def generate_report(analysis_data, report_path, format="text"):
    try:
        if format == "text":
            with open(report_path, 'w') as report_file:
                report_file.write("Analysis Report\n")
                report_file.write("=" * 40 + "\n")
                report_file.write(analysis_data + '\n')
        elif format == "json":
            with open(report_path, 'w') as report_file:
                json.dump(analysis_data, report_file, indent=4)
        elif format == "csv":
            with open(report_path, 'w', newline='') as report_file:
                writer = csv.writer(report_file)
                writer.writerow(["Analysis Report"])
                writer.writerow(["=" * 40])
                writer.writerow([analysis_data])
    except Exception as e:
        print(f"Error writing to report file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Log analysis and reporting tool.")
    parser.add_argument("log_path", help="The path to the log file.")
    parser.add_argument("report_path", help="The path to the report file.")
    parser.add_argument("log_data", help="The data to be logged and analyzed.")
    parser.add_argument("--level", choices=["INFO", "WARNING", "ERROR"], default="INFO", help="The log level.")
    parser.add_argument("--format", choices=["text", "json", "csv"], default="text", help="The format for the log and report.")
    args = parser.parse_args()

    log_analysis(args.log_path, args.log_data, args.level, args.format)
    generate_report(args.log_data, args.report_path, args.format)

if __name__ == "__main__":
    main()