import os
import subprocess as sp


#Function to check & install java 

def is_java_installed():
    return_code = os.system('java -version')
    if return_code != 0 :
        print("Java is not installed.")
        choice= input("Do you want to install Java.([y]/[n]):")
        if (choice == "y") or (choice == "Y"):
            report= os.system('rpm  -ivh  jdk-8u171-linux-x64.rpm')
            if report != 0:
                print("ERROR: Installation Failed")
            else:
                print("Successfully installed Java")
        else:
            print("Installation interrupted")
    else:
        print("Java is installed already.") 
        return True

#Function to check & install hadoop 

def is_hadoop_installed():
    return_code = os.system('hadoop version')
    if return_code != 0 :
        print("Hadoop is not installed.") 
        choice = input("Do you want to install Hadoop.([y]/[n]):")
        if (choice == "y") or (choice == "Y"):
            report = os.system('rpm -ivh hadoop-1.2.1-1.x86_64.rpm --force')
            if report != 0:
                print("EROR: Installation Failed.")
            else:
                print("Successfully installed Hadoop")
        else:
            print("Installation Interrupted")
    else:
        print("Hadoop is installed already.") 
        return True

#hdfs files

HDFS_SITE_FILE='''
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
<property>
<name>dfs.{node_type}.dir</name>
<value>{folder_path}</value>
</property>

</configuration>
'''

#core-site file

CORE_SITE_FILE='''
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{ip_address}:9001</value>
</property>
</configuration>
'''

#Function to configure namenode 

def configure_namenode():
#creating directory for namenode   
    print("Name node Directory is not set.")
    choice = input("To Continue Set the directory. \nDo you want to set it? ([y]/[n]):")
    if (choice == "N") or (choice == "n"):
        print("Can not proceed ahead... Set the Name Node directory to continue. ")
        return False
    else:
        directory = input("Enter the name node directory path & directory name (ex- /nn):") 
        return_code = os.system ("mkdir {}".format(directory))
        if return_code != 0:
            print("Error: can not create directory at given path. Make sure you are giving proper path.")
        else:
            print("Directory successfully created.")

#editing hdfs-site file for namenode

    print("Editing hdfs-site.html")
    hdfs_site = HDFS_SITE_FILE.format(node_type='name',folder_path= directory)
    return_code =  os.system('cat > /etc/hadoop/hdfs-site.xml << EOL {}'.format(hdfs_site))
    if return_code !=0:
        print('Error: can not create hdfs-site.xml file properly')
    else:
        print("Configured hdfs-site.xml file successfully.")


#editing core-site file for namenode

    ip = input('Enter the Namenode IP:')    
    core_site = CORE_SITE_FILE.format(ip_address=ip)
    return_code = os.system('cat > /etc/hadoop/core-site.xml << EOL {}'.format(core_site))
    if return_code !=0:
        print('Error: can not create core-site.xml file properly')
    else:
        print("Configured core-site.xml file successfully.")

 #format name node
    print('Formating Name Node...')
    return_code = os.system('hadoop namenode -format')
    if return_code != 0:
        print("Error: Can not able to format.")
        return False
    else:
        print('Name node formated successfully')


 #start name node
    print('Starting Name Node...')
    return_code = os.system('hadoop-daemon.sh start namenode')
    if return_code != 0:
        print("Error: Something went wrong. Can not able to start namenode service")
    else:
        print('Name node started successfully')



#Function to configure Datanode

def configure_datanode():
#creating directory for datanode
    IP = input("Enter the DataNode IP address:")
    print("Data node Directory is not set.")
    choice = input("To Continue Set the directory. \nDo you want to set it? ([y]/[n]):")
    if (choice == "N") or (choice == "n"):
        print("Can not proceed ahead... Set the Name Node directory to continue. ")
        return False
    else:
        directory = input("Enter the name node directory path & directory name (ex- /dn):") 
        return_code = os.system ("ssh {} mkdir {}".format(IP, directory))
        if return_code != 0:
            print("Error: can not create directory at given path. Make sure you are giving proper path.")
        else:
            print("Directory successfully created.")
    
#edit hdfs-site.xml for datanode
    print("Editing hdfs-site.html")
    hdfs_site = HDFS_SITE_FILE.format(node_type='data',folder_path= directory)
    return_code =  os.system('ssh {} cat > /etc/hadoop/hdfs-site.xml << EOL {}'.format(IP, hdfs_site))
    if return_code !=0:
        print('Error: can not create hdfs-site.xml file properly')
    else:
        print("Configured hdfs-site.xml file successfully.")

#edit core-site.xml for datanode
    print('Enter name node IP address.')
    ip = input()
    core_site = CORE_SITE_FILE.format(ip_address=ip)
    return_code = os.system('ssh {} cat > /etc/hadoop/core-site.xml << EOL {}'.format(IP, core_site))
    if return_code !=0:        
        print('Error: can not create core-site.xml file properly')
    else:
        print("Configured core-site.xml file successfully.")

#start data node node for datanode
    print('Starting Data Node...')
    return_code = os.system('ssh {} hadoop-daemon.sh start datanode'.format(IP))
    if return_code != 0:
        print("Error: Something went wrong. Can not able to start datanode service")
    else:
        print('Data node started successfully')


#function to configure client

def configure_client():
    
    #edit core-site.xml 
    IP = input("Enter the client's IP address:")
    ip = input('\nEnter name node IP address.')
    core_site = CORE_SITE_FILE.format(ip_address=ip)
    return_code = os.system('ssh {} cat > /etc/hadoop/core-site.xml << EOL {}'.format(IP, core_site))
    if return_code !=0:
        print('Error: can not create core-site.xml file properly')
    else:
        print("Configured core-site.xml file successfully.")


#function to get the hdfs cluster report
def get_report():
    return_code= os.system('hadoop dfsadmin -report')
    if return_code !=0 :
        print('Something went wrong...')


#Function to Put file in hadoop cluster
def put_file():   
    file_path = input("Type the Location/name of file: ")
    return_code = os.system("hadoop fs -put {}".format(file_path))
    if return_code != 0:
        print("Error: can not put file in hdfs cluster. check file path properly")
    else:
        print("file put successfully in clutser")
    
#Function that Gives all the files present in our hadoop cluster

def list_files():
    
    return_code = os.system("hadoop fs -ls /")
    if return_code != 0:
        print("Error: can not list files in hdfs cluster. ")
        return False
    return True


#Function to Read the file from cluster
def read_file():
    
    file_name = input("Type which file name you want to read: ")
    return_code = os.system("hadoop fs -cat /{}".format(file_name))
    if return_code != 0:
        print("Error: can not put file in hdfs cluster. check file path properly")
        return False
    else:
        print("file put successfully in clutser")
    return True


    
        
def hadoop():
    print("Welcome to hadoop menu..")
    while(True):
        print('\n\nServices - ')
        print('1. Install Java & Hadoop')
        print('2. Configure Namenode')
        print('3. Configure Datanode')
        print('4. Configure Client')
        print('5. Hadoop report')
        print('6. Hadoop list files')
        print('7. Read file from cluster')
        print('8. Put file in cluster')
        print('0. Exit')

        service = int(input('Enter here : '))
        if service == 1:
            is_java_installed()
            is_hadoop_installed()
        elif service == 2:
            configure_namenode()
        elif service == 3:
            configure_datanode()
        elif service == 4:
            configure_client()
        elif service == 5:
            get_report()
        elif service == 6:
            list_files()
        elif service == 7:
            read_file()
        elif service == 8:
            put_file()
        elif service == 0 :
            print("Exiting")
            exit()
        else: 
            print("INVALID INPUT")


hadoop()
