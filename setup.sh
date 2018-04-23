sudo apt-get update 
sudo apt-get -y upgrade 
sudo apt-get update 

sudo apt-get -y install git
git clone https://github.com/6564200/TiomeBOX.git

sudo apt-get -y install exfat-fuse
sudo apt-get -y install exiftool
#sudo mkdir /mnt/SD
sudo apt-get -y install build-essential 
sudo apt-get -y install python-dev
sudo apt-get -y install python pip
sudo pip install -U pip
sudo pip install Adafruit_Python_DHT
sudo apt-get -y install htop mc
sudo apt-get -y install swig

sudo apt-get -y install python-smbus
sudo apt-get -y install i2c-tools

sudo apt-get -y install libpng3
sudo apt-get -y install libjpeg-dev 
sudo apt-get -y install libjpeg8-dev 
sudo apt-get -y install libfreetype6 
sudo apt-get -y install libfreetype6-dev 
sudo apt-get -y install zlib1g-dev 

sudo apt-get -y install lirc
sudo apt-get -y install libusb-dev

sudo apt-get -y install libssl-dev 
sudo apt-get -y install libffi-dev 
sudo apt-get -y install python3-dev

sudo pip install --upgrade setuptools
sudo pip install cryptography
sudo pip install paramiko

wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh 
chmod +x gphoto2-updater.sh 
sudo ./gphoto2-updater.sh
