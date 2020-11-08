import subprocess
import os

print("******************************************Welcome to My AWS-cloud Menu Tool***********************************************\n\n\n\n")


#Menu
def menu():
    print("Press 0: To Create a key pair")
    print("Press 1: To Provision Instance on the AWS cloud")
    print("Press 2: To create a tag for the Instance")
    print("Press 3: To Start your instance.")
    print("Press 4: To stop your instance")
    print("Press 5: To Describe your instances")
    print("Press 6: To Create a s3 storage bucket")
    print("Press 7: To Delete a s3 storage bucket")
    print("Press 8: To Copy files in the s3 bucket")
    print("Press 9: To Remove files from the s3 bucket")
    print("Press 10: To ssh your instance on the AWS cloud")
    print("Press 11: To setup cloudfront to your aws s3 bucket ")
    print("Press 12: To create one EBS storage")
    print("Press 13: To exit the program")



#Function to Execute the command and check whether the command run successfully or not
def run(command):
	x = subprocess.getstatusoutput(command)
	print(x[1])
	if x[0] == 0 :
		print("Command executed successfully\n\n")


#0.Function to create a Key 
def create_key():
    key_name = input("Enter the key name:") 
    run("aws ec2 create-key-pair --key-name {}".format(key_name))


#1.Function to start the instane on the aws cloud
def provisionVM():
    print("Enter which Image type you wnat: \n 1.Amazon Linux 2 AMI \n 2.Red Hat Enterprise Linux 8 \n 3.Any other Image")
    ch = int(input("Enter choice:"))
    if ch==1 :
        key = input("Enter the key name:")
        run("aws ec2 run-instances --image-id ami-0e306788ff2473ccb --instance-type t2.micro  --key-name {}".format(key))
    elif ch ==2:
        key = input("Enter the key name:")
        run("aws ec2 run-instances --image-id ami-052c08d70def0ac62 --instance-type t2.micro  --key-name {}".format(key))
    elif ch==3 :
        image_id = input("Enter the image ID:")
        key = input("Enter the key name:")
        instance_type = input("Enter the instance type:")
        run("aws ec2 run-instances --image-id {} --instance-type {}  --key-name {}".format(image_id, instance_type, key))
    else:
        print("Invalid Input")

#2.Function to create the tag for the instance 
def tagVM():
     Instance_ID = input("Enter your Instance ID:")
     Value = input("Enter the Tag for your Instance:")
     run("aws ec2 create-tags --resources {} --tags Key=Name,Value={}".format(Instance_ID, Value))

#3.Function to Start the stopped instance
def startVM():
    Instance_ID = input("Enter the Instance ID whcih you want to Start:")
    run("aws ec2 start-instances --instance-ids {}".format(Instance_ID))

#4.Function to Start the stopped instance
def stopVM():
    Instance_ID = input("Enter the Instance ID whcih you want to Stop:")
    run("aws ec2 stop-instances --instance-ids {}".format(Instance_ID))

#5.Function to Describe All the ec2 instances
def describe():
    run("aws ec2 describe-instances")

#6.Function to create the s3 Storage bucket 
def s3bucket():
     bucket_name = input("Enter the Unique Bucket Name:")
     print("Default region (ap-south-1)")
     print("To continuue Press 0 \nTo chnage press 1")
     choice = int(input("(0/1):"))
     if choice==0:
        run("aws s3api create-bucket --bucket {} --region ap-south-1 --create-bucket-configuration LocationConstraint=ap-south-1".format(bucket_name))
     else:
        region = int(input("Enter your Region Name:"))
        run("aws s3api create-bucket --bucket {} --region {} --create-bucket-configuration LocationConstraint={}".format(bucket_name, region, region))

#7.Function to delete the s3 storage bucket 
def s3delbucket():
    bucket_name = input("Enter the Unique Bucket Name:")
    region = input("Enter your Region Name:")
    run("aws s3api delete-bucket --bucket {} --region {}".format(bucket_name, region))

#8.Function to copy the Files in the s3 storage bucket 
def s3cpbucket():
    file_name = input("Enter your File Name:")
    bucket_name = input("Enter the unique Bucket name:")
    run("aws s3 cp {} s3://{}/ --acl public-read".format(file_name, bucket_name))

#9.Function to remove the Files from the s3 storage bucket 
def s3rmbucket():
    file_name = input("Enter your File Name:")
    bucket_name = input("Enter the unique Bucket name:")
    run("aws s3 rm s3://{}/{} ".format(bucket_name, file_name))

#10.Function to ssh the aws ec2 instance
def sshinstance():
    Key = input("Enter your Key Name:")
    ip = input("Enter your Instance Public IPv4 or Public IPv4 DNS:")
    run("ssh -i {} ec2-user@{}".format(Key, ip))

#11.Function to setup the cloud front
def cloudfront():
    domain_name = input("Enter the origin name(s3 bucket name):")
    run("aws cloudfront create-distribution --origin-domain-name {}.s3.amazonaws.com".format(domain_name))

#12.Function to create the EBS block storage 
def ebs():
    volume_type = input("Enter the Volume type:")
    size = input("Enter the size of the EBS volume:")
    zone = input("Enter the availability zone Name:")
    run("aws ec2 create-volume --volume-type {} --size {} --availability-zone {}".format(volume_type, size, zone))

#Function to configure the aws cli on your system
def aws_configure():
    ch = input("AWS cli is installed in your system \nDo you want to configure AWS \nPress [n] & continue If configured already ([y]/[n]):")
    if "y" in ch or "Y" in ch :
        print("configuring aws cli")
        os.system("aws configure")
    else:
        run_menu()


def run_menu():
    while True: 
        menu()
        c=int(input("Enter your choice:"))
        if c==0:
            create_key()
        elif c==1:
            provisionVM()
        elif c==2: 
            tagVM()
        elif c==3:
            startVM()
        elif c==4:
            stopVM()
        elif c==5:
            describe()
        elif c==6:
            s3bucket()
        elif c==7:
            s3delbucket()
        elif c==8:
            s3cpbucket()
        elif c==9:
            s3rmbucket()
        elif c==10:
            sshinstance()
        elif c==11:
            cloudfront()
        elif c==12:
            ebs()
        elif c==13:
            print("Exiting the program")
            break
       
def check_req():
		print("checking requirements...")
		x = subprocess.getstatusoutput("aws --version")
		if x[0] != 0 :
			print("AWS cli not installed on your system")
			print("please install aws cli")
			ch = input("press [y/n] = " )
			if ch == "y" or ch == "Y":
				os.system(" curl \"https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip\" -o \"awscliv2.zip\"")
				os.system("unzip awscliv2.zip")
				os.system("sudo ./aws/install")
				check_req()
			else:
				print("aws cli required to run aws commands")
				
		else :
			aws_configure()

check_req()

