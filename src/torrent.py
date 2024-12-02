import subprocess 

def create_torrent(file_name, torrent_file):
    command = f" webtorrent create {file_name} -o {torrent_file}"
    result = subprocess.run(["powershell.exe", command], capture_output=True, text=True) 
    

def download_torrent(torrent_file, save_path):
    command = f"webtorrent download {torrent_file} -o {save_path}"
    result = subprocess.run(["powershell.exe", command], capture_output=True, text=True) 


def seed_torrent(torrent_file, save_path):
    command = f"start webtorrent seed {torrent_file} --keep-seeding"
    result = subprocess.run(["powershell.exe", command], capture_output=True, text=True) 



if __name__ == "__main__":
    
    file_name = "b.txt"
    torrent_file = "b.torrent"
    save_path = "src/"

    # Create a torrent
    print("Torrent created")
    create_torrent(file_name, torrent_file)

    # Seed a torrent
    print("Torrent seeding")
    seed_torrent(torrent_file, save_path)

    # Download a torrent
    print("Torrent downloading")
    download_torrent(torrent_file, save_path)

   

