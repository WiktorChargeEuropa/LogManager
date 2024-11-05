import os
import click
import datetime
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@click.command()
@click.argument('input_directory', type=click.Path(exists=True))

def process_logs(input_directory):
    startup_files = [f for f in os.listdir(input_directory) if f.startswith("Startup") and f.endswith(".log")]
    
    if not startup_files:
        logging.error("No startup log files found. Exiting.")
        sys.exit(1)

    for startup_file in startup_files:
        startup_path = os.path.join(input_directory, startup_file)

        try:
            startup_datetime_str = startup_file.replace("Startup", "").replace(".log", "")
            startup_datetime = datetime.datetime.strptime(startup_datetime_str, "%d%m%Y_%H%M%S")
        except ValueError:
            logging.error(f"Invalid startup log filename format for {startup_file}. Skipping.")
            continue

        output_file = os.path.join(input_directory, f"output_{startup_datetime_str}.log")
        
        with open(output_file, "w") as outfile:
            # Process the startup log
            with open(startup_path, "r") as startup_infile:
                for line in startup_infile:
                    parts = line.strip().split(";")
                    if len(parts) < 3:
                        continue

                    tick = parts[1]
                    messages = parts[2:]

                    for message in messages:
                        try:
                            timestamp_str, log_message = message.split(":", 1)
                            timestamp = datetime.datetime.fromtimestamp(int(timestamp_str))
                            human_readable_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                            if log_message.startswith("[") and "]:" in log_message:
                                log_level, rest = log_message.split("]:", 1)
                                log_level = log_level + "]"
                                tag, message_content = rest.split(":", 1)
                                outfile.write(f"<{tick}> {human_readable_time} {log_level} ({tag}) {message_content.strip()}\n")
                            else:
                                outfile.write(f"<{tick}> {human_readable_time} {log_message.strip()}\n")
                        except ValueError:
                            continue

            # Process other log files based on the startup file's timestamp
            log_files = []
            for filename in os.listdir(input_directory):
                if filename.startswith("Startup") or not filename.endswith(".log"):
                    continue

                try:
                    log_datetime_str = filename.replace(".log", "")
                    log_datetime = datetime.datetime.strptime(log_datetime_str, "%d%m%Y_%H%M%S")
                except ValueError:
                    continue

                if log_datetime >= startup_datetime:
                    log_files.append(filename)

            log_files.sort()

            for log_file in log_files:
                log_path = os.path.join(input_directory, log_file)
                with open(log_path, "r") as infile:
                    for line in infile:
                        parts = line.strip().split(";")
                        if len(parts) < 3:
                            continue

                        tick = parts[1]
                        messages = parts[2:]

                        for message in messages:
                            try:
                                timestamp_str, log_message = message.split(":", 1)
                                timestamp = datetime.datetime.fromtimestamp(int(timestamp_str))
                                human_readable_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                                if log_message.startswith("[") and "]:" in log_message:
                                    log_level, rest = log_message.split("]:", 1)
                                    log_level = log_level + "]"
                                    tag, message_content = rest.split(":", 1)
                                    outfile.write(f"<{tick}> {human_readable_time} {log_level} ({tag}) {message_content.strip()}\n")
                                else:
                                    outfile.write(f"<{tick}> {human_readable_time} {log_message.strip()}\n")
                            except ValueError:
                                continue

        logging.info(f"Processing complete for {startup_file}. Log saved to: {output_file}")

if __name__ == "__main__":
    process_logs()
