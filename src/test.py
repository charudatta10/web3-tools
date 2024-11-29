from qbittorrentapi import Client

# Replace with your qBittorrent WebUI credentials
client = Client(host='http://127.0.0.1:8080', username='admin', password='adminadmin')

# Authenticate with the qBittorrent WebUI
try:
    client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(f"Failed to login to qBittorrent: {e}")
    exit(1)
import time

# URL of the torrent or magnet link
torrent_url = './blockchain.json.torrent'

# Add the torrent to qBittorrent
try:
    client.torrents_add(urls=torrent_url, save_path='./docs/')
    print(f"Torrent added: {torrent_url}")

    # Wait for the download to complete
    while not any(torrent.state_enum.is_complete for torrent in client.torrents_info()):
        time.sleep(1)
        print("Waiting for the download to complete...")

    print("Download complete")
except Exception as e:
    print(f"Failed to add torrent: {e}")
