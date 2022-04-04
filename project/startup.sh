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
wget <compose_url> -O docker-compose
chmod +x docker-compose
./docker-compose version
cd ~
echo export PATH="${HOME}/bin:${PATH}" >> .bashrc

## terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform