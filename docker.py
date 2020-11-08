#!/usr/bin/python3

import subprocess
import sys

#Function to execute any command
def cmd_exec(exec_loc,cmd,remote_ip=" "):
	if exec_loc==1:
		output=subprocess.run(["ssh","root@{r}".format(r=remote_ip),cmd],
			shell=False,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,check=True)
	else:
		output=subprocess.run(cmd,
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,check=True)

	result=output.stdout
	if (result == "b\'\'"):
		error=output.stderr
		print("Error: {e}".format(e=error.decode('utf-8')))
	else:
		print(result.decode('utf-8'))
		#print()

#Function to run docker container
def docker_con_run(exec_loc,remote_ip):
	cmd="docker run -it"
	print("Enter the name of the docker image: ")
	image_name=input()
	print("Enter the name of the container: ")
	name=input()
	print("Options to launch the container (Enter 0 if you want none of the options:\n")
	print("1. Detached(Background)\n")
	print("2. Exposing Ports\n")
	print("3. Attach a filesystem\n")
	print("4. Give extended privileges\n")
	print("5. Bind/Mount a volume\n")
	print("6. Set the working directory\n")
	options=input("Enter the numbers, seperated by commas(,): ")
	options=options.split(',')
	for j in options:
		if (int(j)==1):
			cmd=cmd+"d"
		elif (int(j)==2):
			cmd=cmd+" -p "
			print("Enter the port number to be exposed: ")
			port_num=input()
			cmd=cmd+port_num+" "
		elif (int(j)==3):
			cmd=cmd
		elif (int(j)==4):
			cmd=cmd
		elif (int(j)==5):
			cmd=cmd
		elif (int(j)==6):
			print("Enter the path of the working directory: ")
			path=input()
			cmd=cmd+" -w "+path
	cmd=cmd+" --name "+name+" "+image_name
	print(cmd)
	cmd_exec(exec_loc,cmd,remote_ip)

# Function to stop docker container
def docker_con_stop(exec_loc,remote_ip):
	print("Enter the name of the container: ")
	name=input()
	cmd="docker stop "+name
	cmd_exec(exec_loc,cmd,remote_ip)

#Function to attach docker container to foreground
def docker_con_foregnd(exec_loc,remote_ip):
	print("Enter the name of the container: ")
	name=input()
	cmd="docker attach "+name
	cmd_exec(exec_loc,cmd,remote_ip)

#Function to delete any container with given name
def docker_con_del(exec_loc,remote_ip):
	print("Enter the name of the container: ")
	name=input()
	cmd="docker rm -f "+name
	cmd_exec(exec_loc,cmd,remote_ip)
	print("Container "+name+" has been deleted!")

#Function to pull a Docker Image from Docker Hub
def docker_pull_img(exec_loc,remote_ip):
	print("Enter the name of the image: ")
	name=input()
	cmd="docker pull "+name
	cmd_exec(exec_loc,cmd,remote_ip)
	print("Image "+name+" has been pulled successfully!")

#Function to search for images in DockerHub with a keyword
def dockerhub_search(exec_loc,remote_ip):
	print("Enter the keyword for Docker images search on DockerHub: ")
	name=input()
	cmd="docker search "+name
	cmd_exec(exec_loc,cmd,remote_ip)

#Function to delete a container image
def dockerimage_del(exec_loc,remote_ip):
	print("Enter the name of the image: ")
	name=input()
	cmd="docker rmi "+name
	cmd_exec(exec_loc,cmd,remote_ip)
	print("Image "+name+" has been deleted successfully!")

#Function to install Docker CE version
def docker_install(exec_loc,remote_ip):
	#cmd=["date", "rpm -q firefox", "cal", "ifconfig enp0s3"]
	cmd=["ifconfig enp0s3",
		"touch /etc/yum.repos.d/docker_config.repo",
		"echo \"[docker]\" > /etc/yum.repos.d/docker_config.repo",
		"echo \"baseurl=https://download.docker.com/linux/centos/7/x86_64/stable\" >> /etc/yum.repos.d/docker_config.repo",
		"echo \"gpgcheck=0\" >> /etc/yum.repos.d/docker_config.repo",
		"yum clean all",
		"yum repolist",
		"yum install docker-ce --nobest -y",
		"rpm -q docker-ce",
		"systemctl start docker",
		"systemctl status docker"
		]
	print("#############----------Installaing Docker----------#############")
	for i in cmd:
		val=cmd.index(i)
		if (val == 0):
			print("Verifying remote execution...")
		elif (val == 1):
			print("Configuring the YUM repo")
		elif (val == 5):
			print("Cleaning YUM repo list")
		elif (val == 6):
			print("Configuring YUM repo list")
		elif (val == 7):
			print("Installing Docker CE Version")
		elif (val == 9):
			print("Starting Docker Daemon")
		elif (val == 10):
			print("Confirming status of Docker Daemon")

		if exec_loc==1:
			output=subprocess.run(["ssh","root@{r}".format(r=remote_ip),i],
				shell=False,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,check=True)
		else:
			output=subprocess.run(i,
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,check=True)

		result=output.stdout
		if (result == "b\'\'"):
			error=output.stderr
			print("Error: {e}".format(e=error.decode('utf-8')))
		else:
			print(result.decode('utf-8'))




def docker_commands(exec_loc,remote_ip=" "):
	if (exec_loc==1):
		(check_docker,out)=subprocess.getstatusoutput("ssh root@{i} rpm -q docker-ce".format(i=remote_ip))
	else:
		(check_docker,out)=subprocess.getstatusoutput("rpm -q docker-ce")
	#print(check_docker)
	if (check_docker==1):
		docker_install(exec_loc,remote_ip)
	cmd_exec(exec_loc,"systemctl start docker",remote_ip)
	print("What do you want to do in Docker?\n")
	print("1. Start a new container\n")
	print("2. Stop a running container\n")
	print("3. List all the running containers\n")
	print("4. List all shut-down and running containers\n")
	print("5. Bring a container into forefront\n")
	print("6. Delete a container\n")
	print("7. Pull a container image from DockerHub\n")
	print("8. Search for images on DockerHub\n")
	print("9. Delete a docker image\n")
	print("10. List all pulled Docker Images\n")
	print("0. Return to Main Menu\n")
	choice=int(input())

	if (choice==1):
		docker_con_run(exec_loc,remote_ip)
	elif (choice==2):
		docker_con_stop(exec_loc,remote_ip)
	elif (choice==3):
		cmd_exec(exec_loc,"docker ps",remote_ip)
	elif (choice==4):
		cmd_exec(exec_loc,"docker ps -a",remote_ip)
	elif (choice==5):
		docker_con_foregnd(exec_loc,remote_ip)
	elif (choice==6):
		docker_con_del(exec_loc,remote_ip)
	elif (choice==7):
		docker_pull_img(exec_loc,remote_ip)
	elif (choice==8):
		dockerhub_search(exec_loc,remote_ip)
	elif (choice==9):
		dockerimage_del(exec_loc,remote_ip)
	elif (choice==10):
		cmd_exec(exec_loc,"docker images",remote_ip)
	elif (choice==0):
		print("Exiting Docker.... The Docker Daemon will be shut down on exit")
		cmd_exec(exec_loc,"sleep 5",remote_ip)
		cmd_exec(exec_loc,"systemctl stop docker",remote_ip)

exec_loc=int(input("Execution of commands - local or remote (0/1)?: "))
if (exec_loc==1):
	remote_ip=input("Remote IP Address: ")
	#docker_install(exec_loc,remote_ip)
	docker_commands(exec_loc,remote_ip)
else:
	print("Executing commands on local system\n")
	#docker_install(exec_loc,"")
	docker_commands(exec_loc)
