import ftplib
import click
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@click.command()
@click.argument('ftp_host')
def delete_logs(ftp_host):

    # Connect to FTP host
    try:
        with ftplib.FTP(ftp_host) as ftp:
            ftp.login()  # Połączenie anonimowe
            logging.info("Connected with FTP: %s", ftp_host)

            # File list download
            files = ftp.nlst()
            log_files = [f for f in files if f.endswith('.log')]

            if not log_files:
                logging.warning("No .log files on server.")
                return

            # Delete every .log file
            for log_file in log_files:
                try:
                    ftp.delete(log_file)
                    logging.info("Deleted file: %s", log_file)
                except ftplib.error_perm as e:
                    logging.error("Cant delete file %s: %s", log_file, e)

    except ftplib.all_errors as e:
        logging.error("Error: %s", e)

    logging.info("Clear finished.")

if __name__ == "__main__":
    delete_logs()
