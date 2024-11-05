# Download, delete and summarize by using LogAutoManager.py
python .\LogAutoManager.py <IP> <local directory>

or do it manually

# Step 1: Retrieve logs
python .\GetLogs.py <IP> <local directory>

# Step 2: Delete logs
python .\ClearLogs.py <IP>

# Step 3: Summarize logs
python .\LogHandler.py <IP> <local directory>
