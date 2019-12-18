#!/bin/bash
# CloudMail.ru Downloader
# Original idea: https://novall.net/itnews/bash-skript-dlya-skachivaniya-fajlov-s-mail-ru-cherez-konsol-linux.html

# env
sudo apt install -y aria2 &> /dev/null

URL="$1"

[ -z "$URL" ] && {
	echo "Usage: `basename $0` <file url>" >&2
	echo "Example: `basename $0` https://cloud.mail.ru/public/User/Project/Photo.jpg" >&2
	exit 1
}

URL1=$(wget --quiet -O - $URL | grep -om1 'https://cloclo.*G')
URL2=$(echo $URL | awk -F '/public/' '{print $2}')
TOKEN=$(wget --quiet -O - "https://cloud.mail.ru/api/v2/tokens/download" | grep -oP '(?<=token":")[^"]*')

aria2c "$URL1/$URL2?key=$TOKEN&key=$TOKEN"
