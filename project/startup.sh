sudo apt update
sudo apt -y upgrade
sudo apt-get install wget 
sudo apt install git
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev
wget https://www.python.org/ftp/python/3.9.11/Python-3.9.11.tgz
tar -xf Python-3.9.11.tgz
cd Python-3.9.11
./configure --enable-optimizations
make -j 2
sudo make altinstall
python3.9 --version

## install docker
sudo apt install docker.io
sudo gpasswd -a $USER docker
sudo service docker restart
mkdir ~/bin
cd ~/bin
wget https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -O docker-compose
chmod +x docker-compose
./docker-compose version
cd ~
echo export PATH="${HOME}/bin:${PATH}" >> .bashrc
