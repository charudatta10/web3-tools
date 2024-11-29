import subprocess 

def create_torrent(file_name, torrent_file):
    command = f" webtorrent create {file_name} -o {torrent_file}"
    result = subprocess.run(["powershell.exe", command], capture_output=True, text=True) 
    

def download_torrent(torrent_file, save_path):
    command = f"webtorrent download {torrent_file}"
    result = subprocess.run(["powershell.exe", command], capture_output=True, text=True) 


def seed_torrent(torrent_file):
    command = f"webtorrent seed {torrent_file} --keep-seeding"
    result = subprocess.run(["powershell.exe", command], capture_output=True, text=True) 



if __name__ == "__main__":
    # Create a torrent
    create_torrent('file_name, torrent_file')

    # Download a torrent
    download_torrent(torrent_file, 'path/to/save')

    # Seed a torrent
    seed_torrent(torrent_file)

