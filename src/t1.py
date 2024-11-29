import qbittorrentapi
import os
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace with your qBittorrent WebUI credentials
client = qbittorrentapi.Client(host='http://127.0.0.1:8080', username='admin', password='adminadmin')

# Authenticate with the qBittorrent WebUI
try:
    client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    logging.error(f"Failed to login to qBittorrent: {e}")
    exit(1)

# Path to your local file
file_path = 'readme.md'
torrent_file = file_path + '.torrent'

# Create a torrent from a local file
try:
    torrent_info = client.torrents.create_torrent(file_path, save_path=os.path.dirname(file_path))
    logging.info(f"Torrent created: {torrent_file}")
except Exception as e:
    logging.error(f"Failed to create torrent: {e}")

# Verify the torrent creation
try:
    time.sleep(5)  # Wait for the torrent to be processed
    torrents = client.torrents_info(category='blockchain')
    for torrent in torrents:
        logging.info(f"{torrent.hash[-6:]}: {torrent.name} ({torrent.state})")
except Exception as e:
    logging.error(f"Failed to retrieve torrent info: {e}")
