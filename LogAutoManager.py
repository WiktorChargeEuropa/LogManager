import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name, ip_address=None, log_directory=None):
    try:
        logging.info(f"Starting script: {script_name} with IP adress: {ip_address} "
                     f"{f'with directory: {log_directory}' if log_directory else ''}")
        
        # Argument list 
        args = ["python", script_name]
        if ip_address:
            args.append(ip_address)
        if log_directory:
            args.append(log_directory)

        result = subprocess.run(args, check=True)
        logging.info(f"Script {script_name} finished.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error in {script_name}: {e}")
        sys.exit(1)

def main(ip_address, log_directory):

    # Krok 1: Get logs from FTP host
    run_script("GetLogs.py", ip_address, log_directory)

    # Krok 2: Delete logs
    run_script("ClearLogs.py", ip_address)

    # Krok 3: Summarize
    run_script("LogHandler.py", log_directory)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Using: python LogManagement.py <IP> <log_directory>")
        sys.exit(1)

    ip_address = sys.argv[1]
    log_directory = sys.argv[2]
    main(ip_address, log_directory)
