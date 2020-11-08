#!/usr/bin/python3

import subprocess
import sys

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

def create_pv(exec_loc,remote_ip):
	cmd="pvcreate "
	print("Enter the name of the block device (Enter 0 to return back to the LVM Main Menu): ")
	dev_name=input()
	if (dev_name=="0"):
		print("Returning to the LVM Main Menu")
		return -1
	else:
		cmd=cmd+dev_name
		print(cmd)
		cmd_exec(exec_loc,cmd,remote_ip)
	return 0

def display_pv(exec_loc,remote_ip):
	check=True
	while(check):
		print("Generic List or details of specific PV (Generic-1/Specific-2/Return back-0): ")
		choice=int(input())
		if (choice==1):
			cmd_exec(exec_loc,"pvdisplay",remote_ip)
			check=False
		elif(choice==2):
			print("Enter the name of the desired PV(s) (For multiple PVs, write them seperated by spaces: ")
			pv_name=input()
			cmd_exec(exec_loc,"pvdisplay"+pv_name,remote_ip)
			check=False
		elif(choice==0):
			print("Returning to Main Menu...")
			check=False
		else:
			print("Invalid option!! Please enter the correct option")


def create_vg(exec_loc,remote_ip):
	print("Enter the name of the Volume Group you want to create (Enter 0 at any prompt to return back to the LVM Main Menu): ")
	vg_name=input()
	print("Enter the names of the PVs you want to allocate to this VG (Write the PVs seperated by spaces):")
	pvs_alloc=input()
	if (vg_name=="0" or pvs_alloc=="0"):
		print("Returning to LVM Main Menu...")
		return -1
	else:
		cmd="vgcreate "+vg_name+" "+pvs_alloc
		cmd_exec(exec_loc,cmd,remote_ip)
		print("Confirming if the PVs are allocatable...")
		cmd_exec(exec_loc,"pvdisplay "+pvs_alloc,remote_ip)
	return 0

def display_vg(exec_loc,remote_ip):
	check=True
	while(check):
		print("Generic List or details of specific VG (Generic-1/Specific-2/Return back-0): ")
		choice=int(input())
		if (choice==1):
			cmd_exec(exec_loc,"vgdisplay",remote_ip)
			check=False
		elif(choice==1):
			print("Enter the name of the desired VG: ")
			vg_name=input()
			cmd_exec(exec_loc,"pvdisplay"+vg_name,remote_ip)
			check=False
		elif(choice==0):
			print("Returning to LVM Main Menu...")
			check=False
			return -1
		else:
			print("Invalid option!! Please enter the correct option")
	return 0

def create_lv(exec_loc,remote_ip):
	print("Enter the size of the LV being created (For example, For partition of size 50 MiB, enter 50M; for partition of size 1 GiB, enter 1G: ")
	size=int(input())
	print("Enter the name of LV being created: ")
	lv_name=input()
	print("Enter the name of the VG from which LV is being created: ")
	vg_name=input()
	if (exec_loc==1):
		(status,out)=subprocess.getstatusoutput("ssh root@{i} vgdisplay {v}".format(i=remote_ip,v=vg_name))
	else:
		(status,out)=subprocess.getstatusoutput("vgdisplay {v}".format(v=vg_name))
	if(status!=0):
		print("Invalid VG name!! Returning to Main Menu")
		return -1

	cmd="lvcreate --size "+size+"--name "+lv_name+" "+vg_name
	cmd_exec(exec_loc,cmd,remote_ip)
	print("LV "+lv_name+" has been created successfully!")
	return 0

def display_lv(exec_loc,remote_ip):
	check=True
	while(check):
		print("Generic List or details of specific VG (Generic-1/Specific-2/Return back-0): ")
		choice=int(input())
		if (choice==1):
			cmd_exec(exec_loc,"lvdisplay",remote_ip)
			check=False
		elif(choice==1):
			print("Enter the name of the desired LV(s) (For multiple LVs, seperate the names by spaces): ")
			lv_name=input()
			cmd_exec(exec_loc,"lvdisplay"+vg_name,remote_ip)
			check=False
		elif(choice==0):
			print("Returning to Main Menu...")
			check=False
			return -1
		else:
			print("Invalid option!! Please enter the correct option")
	return 0


def lvm_commands(exec_loc,remote_ip=" "):

	print("What do you want to do in Logical Volume Management?\n")
	print("1. Create Physical Volume(s)\n")
	print("2. Display physical volumes\n")
	print("3. Create Volume Group(s)\n")
	print("4. Display Volume Group(s)\n")
	print("5. Create Logical Volume(s) (and format and mount the LV(s))\n")
	print("6. Display Logical Volume(s)\n")
	print("7. Display all block devices\n")
	print("8. Display details about available filesystems\n")
	print("9. Display available disk partitions\n")
	print("0. Return to Main Menu\n")
	choice=int(input())

	if (choice==1):
		pv_num=int(input("How many PVs?: "))
		if (pv_num<=0):
			print("Invalid input!!!")
		else:
			for i in range(pv_num):
				out=create_pv(exec_loc,remote_ip)
				if (out==-1):
					break
	elif (choice==2):
		display_pv(exec_loc,remote_ip)
	elif (choice==3):
		vg_num=int(input("How many VGs?: "))
		if (vg_num<=0):
			print("Invalid input!!!")
		else:
			for i in range(vg_num):
				create_vg(exec_loc,remote_ip)
	elif (choice==4):
		display_vg(exec_loc,remote_ip)
	elif (choice==5):
		lv_num=int(input("How many LVs?: "))
		if (lv_num<=0):
			print("Invalid input!!!")
		else:
			for i in range(lv_num):
				create_lv(exec_loc,remote_ip)
	elif (choice==6):
		display_lv(exec_loc,remote_ip)
	elif (choice==7):
		cmd_exec(exec_loc,"lsblk",remote_ip)
	elif (choice==8):
		cmd_exec(exec_loc,"df -h",remote_ip)
	elif (choice==9):
		fdisk_input=input("Which disk partition(s) do you want to see? (If you want to see all, type all;else type all the desired disk names seperated by spaces")
		if (fdisk_input=="all"):
			cmd_exec(exec_loc,"fdisk -l",remote_ip)
		else:
			cmd_exec(exec_loc,"fdisk -l "+fdisk_input,remote_ip)
	elif (choice==0):
		print("Exiting LVM Menu...")
		cmd_exec(exec_loc,"sleep 5",remote_ip)

exec_loc=int(input("Execution of commands - local or remote (0/1)?: "))
if (exec_loc==1):
	remote_ip=input("Remote IP Address: ")
	lvm_commands(exec_loc,remote_ip)
else:
	print("Executing commands on local system\n")
	lvm_commands(exec_loc)
