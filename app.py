import pandas as pd

# Prompt the user to enter log entries
print("Enter firewall log entries (press Enter twice to finish):")
log_entries = []
while True:
    line = input()
    if not line:
        break
    log_entries.append(line)

# Split log entries into lines
log_lines = log_entries

# Define data columns
columns = ["Date/Time", "Action", "Protocol", "Source IP", "Destination IP", "Source Port", "Destination Port", "Size", "flag", "Info"]

# Create an empty list to store parsed log data
log_data = []

# Parse each log entry and store in the log_data list
for line in log_lines:
    # Skip lines starting with a comment symbol
    if not line.startswith("#"):
        # Use split with a different delimiter for better handling
        parts = line.split(" ")
        # Combine all elements from the 11th position onwards as the "Info" field
        info = " ".join(parts[11:])
        log_data.append(dict(zip(columns, [parts[0] + " " + parts[1]] + parts[2:10] + [info])))

# Create a DataFrame from the parsed log data
df = pd.DataFrame(log_data)

# Display the entire DataFrame
print(df.to_string())

# Calculate statistics
total_entries = len(df)
action_stats = df["Action"].value_counts()
protocol_stats = df["Protocol"].value_counts()
top_src_ips = df["Source IP"].value_counts().head()
top_dst_ips = df["Destination IP"].value_counts().head()
top_blocked_ports = df[df["Action"] == "BLOCK"]["Destination Port"].value_counts().head()
top_allowed_ports = df[df["Action"] == "ALLOW"]["Destination Port"].value_counts().head()

# Additional statistic for Destination IP and Action
dest_ip_action_stats = df.groupby(["Destination IP", "Action"]).size().reset_index(name="Count")

# Display statistics
print("\nStatistics:")
print(f"Total Number of Entries in the Log: {total_entries}")
print("\nAction Statistics:")
print(action_stats.reset_index().rename(columns={"index": "Action", "Action": "Count"}))
print("\nProtocol Distribution:")
print(protocol_stats.reset_index().rename(columns={"index": "Protocol", "Protocol": "Count"}))
print("\nTop Source IP Addresses:")
print(top_src_ips.reset_index().rename(columns={"index": "Source IP", "Source IP": "Count"}))
print("\nTop Destination IP Addresses:")
print(top_dst_ips.reset_index().rename(columns={"index": "Destination IP", "Destination IP": "Count"}))
print("\nTop Blocked Ports:")
print(top_blocked_ports.reset_index().rename(columns={"index": "Blocked Port", "Destination Port": "Count"}))
print("\nTop Allowed Ports:")
print(top_allowed_ports.reset_index().rename(columns={"index": "Allowed Port", "Destination Port": "Count"}))
print("\nDestination IP and Action Statistics:")
print(dest_ip_action_stats.to_string(index=False))



