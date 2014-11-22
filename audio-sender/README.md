# Dependency

- websocket-client

- pyalsaaudio

    ```
    $ sudo apt-get install python-alsaaudio
    $ sudo pip install -r requirements.txt

    $ sudo nano /etc/modprobe.d/alsa-base.conf
    以下の行を削除またはコメントアウト。
    options snd-usb-audio index=-2
    そこに以下の行を追加。
    options snd-bcm2835 index=0
    options snd-usb-audio index=1
    ```

# Usage

    ```
    $ SOUNDCARD=/etc/proc/asound/cardsで確認できるマイクのサウンドカード名
    $ python audio-sender.py --server=server_api_address --card=$SOUNDCARD
    ```
