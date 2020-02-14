from torrentool.api import Torrent
from datetime import datetime
from urllib import request
from tqdm import tqdm
import humanize

#Get the latest version available
try:
    latest_version = request.urlopen("https://cdn.download.clearlinux.org/releases/current/clear/latest").read().decode('utf-8').strip()    
    print("Latest version : " + latest_version)
except request.HTTPError as e:
    print("Error "+str(e.code))
    print("Resource not available. Quitting...")
    quit()

#latest Desktop Live iso URL
webseed_desktop_live = "https://cdn.download.clearlinux.org/releases/"+latest_version+"/clear/clear-"+latest_version+"-live-desktop.iso"
iso_desktop_live = "/tmp/clear-linux_"+latest_version+"_live-desktop.iso"

#Check if iso is available
try:
    print("Downloading latest iso (Version : " + latest_version + ") from mirror (" + 
    humanize.naturalsize(request.urlopen(webseed_desktop_live).getheader("Content-Length")) +
    "). Please wait...")

#TODO : Check if file exists and overwrite
#retrieve iso from clear linux website

    request.urlretrieve(webseed_desktop_live,iso_desktop_live)

except request.HTTPError as e:
    print("Error "+str(e.code))
    print("Resource not available. Quitting...")
    quit()

live_desktop_torrent = Torrent.create_from(iso_desktop_live)
live_desktop_torrent.announce_urls = 'udp://tracker.openbittorrent.com:80'
live_desktop_torrent.webseeds = webseed_desktop_live
live_desktop_torrent.comment = "Torrent automatically created on " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
live_desktop_torrent.to_file('clear-linux-live-desktop-'+latest_version+'.torrent')
