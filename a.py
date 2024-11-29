from torrentool.api import Torrent

# Reading and modifying an existing file.
my_torrent = Torrent.from_file('/home/idle/some.torrent')
my_torrent.total_size  # Total files size in bytes.
my_torrent.magnet_link  # Magnet link for you.
my_torrent.comment = 'Your torrents are mine.'  # Set a comment.
my_torrent.to_file()  # Save changes.

# Or we can create a new torrent from a directory.
new_torrent = Torrent.create_from('/home/idle/my_stuff/')  # or it could have been a single file
new_torrent.announce_urls = 'udp://tracker.openbittorrent.com:80'
new_torrent.to_file('/home/idle/another.torrent')
