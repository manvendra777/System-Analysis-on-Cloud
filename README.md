## Install requirements
pip install -r /path/to/requirements.txt

## Browser settings
Add the extension 'requestly' to modify the header during the request from browser. Can also use Postman/Curl command and pass the header there.
Requestly: [https://app.requestly.io/]

Header can be obtained by visiting http://ec2-52-53-156-147.us-west-1.compute.amazonaws.com:5000/token

## EC2
Start the EC2 instance and update the security group to allow all access for the port 5000.
ssh into EC2 instance using
```
ssh -i ~/path/to/key-pair.pem -A ec2-user@ec2-52-53-156-147.us-west-1.compute.amazonaws.com
```

If you face the issue for bad permissions, use this command
```
sudo chmod 400 /path/to/key-pair.pem
```

Copy all the files to the EC2 instance using
```
scp -i ~/path/to/key-pair.pem -r ~/path/to/files ec2-user@ec2-52-53-156-147.us-west-1.compute.amazonaws.com:~/path/
```
## Daemon
Install daemontools on EC2.
```
sudo yum install gcc make -y
wget http://cr.yp.to/daemontools/daemontools-0.76.tar.gz
tar -xzvf daemontools-0.76.tar.gz
cd admin/daemontools-0.76/
echo gcc -O2 -include /usr/include/errno.h > src/conf-cc
echo 'SV:123456:respawn:/command/svscanboot' >> /etc/inittab
```
Create directories and set permissions
```
sudo init q
sudo mkdir -p /service/app/log
sudo vim /service/app/run
```
```
'#!/bin/sh
exec 2>&1
exec /usr/bin/python3 /home/ec2-user/app.py'
```
```
sudo chmod +x /service/app/run
sudo vim /service/app/log/run
```
```
'#!/bin/sh
exec multilog t ./main'
```
```
sudo chmod +x /service/app/log/run
```
Start the daemon
```
sudo svscan /service &
```

Monitor the daemon
```
sudo svstat /service/app/
```
Monitor the logs
```
sudo tail -f /service/app/log/main/current
```

##Challenges Faced
- Initially had issues with accessing the open port for EC2. Even after adding the SG rule, there is some delay. Stopped and rebooted the instance and the access issue was resolved.
- Majorly faced problems in daemonising the application. Had to restart the entire process several times. Luckily there were number of StackOverflow posts and a couple YouTube videos that helped me resolve these issues. Added the commands as much as I could remember/find in the .bash_history file that I feel were relevant. May be missing a few changes here and there as the number of changes I did was a bit large to keep track of all of them.
- Initial permission issues while SSH into AWS, Added the chmod command that helped me solve that and SSH into the instance.

## Future
Use the Dockerfile to create a docker image for the code.
Deploy it on a fleet of AWS instances. Write code for a controller that will poll all these instances and send the response to the user.
