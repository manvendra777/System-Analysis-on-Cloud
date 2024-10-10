## Install requirements
pip install -r /path/to/requirements.txt

## Browser settings
Add the extension 'requestly' to modify the header during the request from browser. Can also use Postman/Curl command and pass the header there.

Header can be obtained by visiting 'http://ec2-52-53-156-147.us-west-1.compute.amazonaws.com:5000/token'

## EC2
Start the EC2 instance and update the security group to allow all access for the port 5000.
ssh into EC2 instance using

'ssh -i ~/path/to/key-pair.pem -A ec2-user@ec2-52-53-156-147.us-west-1.compute.amazonaws.com'

copy all the files to the EC2 instance using

'scp -i \~/path/to/key-pair.pem -r ~/path/to/files ec2-user@ec2-52-53-156-147.us-west-1.compute.amazonaws.com:\~/path/'

## Daemon
Install daemontools on EC2.
sudo yum install gcc make -y
wget http://cr.yp.to/daemontools/daemontools-0.76.tar.gz
tar -xzvf daemontools-0.76.tar.gz
cd admin/daemontools-0.76/

echo gcc -O2 -include /usr/include/errno.h > src/conf-cc
echo 'SV:123456:respawn:/command/svscanboot' >> /etc/inittab

#create directories and set permissions
sudo init q
sudo mkdir -p /service/cloud/log
sudo vim /service/cloud/run

'#!/bin/sh
exec 2>&1
exec /usr/bin/python3 /home/ec2-user/cloud.py'

sudo chmod +x /service/cloud/run
sudo vim /service/cloud/log/run

'#!/bin/sh
exec multilog t ./main'

sudo chmod +x /service/cloud/log/run

- Start the daemon
sudo svscan /service &

- Monitor the daemon
sudo svstat /service/cloud/

- Monitor the logs
sudo tail -f /service/cloud/log/main/current

## Future
Use the Dockerfile to create a docker image for the code.
Deploy it on a fleet of AWS instances. Write code for a controller that will poll all these instances and send the response to the user.
