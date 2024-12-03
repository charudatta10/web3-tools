import subprocess
import os


def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)


def create_torrent(file_name, torrent_file):
    command = ["webtorrent", "create", file_name, "-o", torrent_file]
    run_command(command)


def download_torrent(torrent_file, save_path):
    command = ["webtorrent", "download", torrent_file, "-o", save_path]
    run_command(command)


def seed_torrent(torrent_file):
    command = ["webtorrent", "seed", torrent_file, "--keep-seeding"]
    run_command(command)


if __name__ == "__main__":
    file_name = "b.txt"
    torrent_file = "b.torrent"
    save_path = "src/"

    if not os.path.exists(file_name):
        print(f"File {file_name} does not exist.")
    else:
        print("Creating torrent...")
        create_torrent(file_name, torrent_file)

        if os.path.exists(torrent_file):
            print("Seeding torrent...")
            seed_torrent(torrent_file)
        else:
            print(f"Torrent file {torrent_file} does not exist.")

        print("Downloading torrent...")
        download_torrent(torrent_file, save_path)
