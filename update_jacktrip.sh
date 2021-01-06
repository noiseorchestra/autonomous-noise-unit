# Install rtaudio from apt

sudo apt-get -y install librtaudio-dev

# Build JackTrip from source

sudo apt-get -y install qt5-default qt5-qmake
sudo rm -r jacktrip
git clone https://github.com/jacktrip/jacktrip.git
cd jacktrip/src
git checkout v1.2.1
qmake jacktrip.pro
sudo make install
