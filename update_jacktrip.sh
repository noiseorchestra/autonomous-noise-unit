# Install rtaudio from apt

sudo apt-get -y install librtaudio-dev

# Build JackTrip from source

sudo apt-get -y install qt5-default qt5-qmake
cd ~/
sudo rm -r jacktrip
git clone https://github.com/jacktrip/jacktrip.git
cd jacktrip/src
git checkout beta.rc.1.3.0
sudo rm -r /usr/local/bin/jacktrip
qmake jacktrip.pro
sudo make install
