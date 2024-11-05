import ftplib
import os
import click
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@click.command()
@click.argument('ftp_host')
@click.argument('local_directory', type=click.Path(exists=True))
def download_logs(ftp_host, local_directory):
    # Connect to FTP host
    try:
        with ftplib.FTP(ftp_host) as ftp:
            ftp.login() 
            logging.info("Connected with FTP host: %s", ftp_host)

            # File list download
            files = ftp.nlst()
            log_files = [f for f in files if f.endswith('.log')]

            if not log_files:
                logging.warning("No .log files for downloading.")
                return

            # Download every .log file
            for log_file in log_files:
                local_path = os.path.join(local_directory, log_file)
                with open(local_path, 'wb') as local_file:
                    ftp.retrbinary(f'RETR {log_file}', local_file.write)
                logging.info("Downloaded file: %s", log_file)

    except ftplib.all_errors as e:
        logging.error("Error: %s", e)

    logging.info("Download succesfull")

if __name__ == "__main__":
    download_logs()
