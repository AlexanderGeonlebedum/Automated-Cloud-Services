#!/usr/bin/env python3
import sys
import boto3
import subprocess
import webbrowser
import time


ec2 = boto3.resource('ec2')
s3 = boto3.resource("s3")
s3client = boto3.client('s3')

#Creating and Configuring of my EC2 instance 

try:
    instance = ec2.create_instances(
    ImageId='ami-00ae935ce6c2aa534',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.nano',
    KeyName= 'alexander_key',

    SecurityGroups=[
        'httpssh2',
    ],

TagSpecifications=[
        {
'ResourceType':'instance',
 'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'ACS Assignent-1'
                        },
                    ]
 },
    ],
    
     UserData='''#! /bin/bash
yum update -y
yum install httpd -y
systemctl enable httpd
systemctl start httpd

echo "<h2>Test page</h2>Instance ID: " > /var/www/html/index.html
curl --silent http://169.254.169.254/latest/meta-data/instance-id/ >> /var/www/html/index.html
echo "<br>Availability zone: " >> /var/www/html/index.html
curl --silent http://169.254.169.254/latest/meta-data/placement/availability-zone/ >> /var/www/html/index.html
echo "<br>IP address: " >> /var/www/html/index.html
curl --silent http://169.254.169.254/latest/meta-data/public-ipv4 >> /var/www/html/index.html
echo <img src=http://alexbucket321.s3-website-eu-west-1.amazonaws.com>/var/www/html/index.html
echo "<br>Contents of my S3: " >> /var/www/html/index.html
curl --silent http://alexbucket321.s3-website-eu-west-1.amazonaws.com/ >> /var/www/html/index.html
'''
)
    print ('New instance Id is '+ instance[0].id)
except Exception as error:
    print ("Instance Error")
   
# Realoading my instance
    
try:
    instance[0].wait_until_running()
    print (instance[0].id +' is waiting until running')
except Exception as error:
    print(error)
    
try:
    instance[0].reload()
    print (instance[0].id +' is reloading')
except Exception as error:
    print(error)
 

try:
    ipaddress = instance[0].public_ip_address
    ipaddressprivate = instance[0].private_ip_address  
    print (instance[0].id +' is now in the running state')
    print('Ipaddress:'+ipaddress, 'Private Ipaddress:'+ipaddressprivate, 'Instance ID:'+instance[0].id)
except Exception as error:
    print(error)
    
#Creating and Configuring my s3 Bucket
try:
    response = s3.create_bucket(ACL='public-read', Bucket="alexbucket321", CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    print (response)  
except Exception as error:
    print ("Bucket Error")
    
subprocess.run(['curl', '-s', 'https://witacsresources.s3-eu-west-1.amazonaws.com/image.jpg', '--output', 'aleximage.jpg'])


#Uploading my files unto S3 bucket
try:
	response = s3.Object('alexbucket321', 'aleximage.jpg').put(Body=open('aleximage.jpg', 'rb'),ACL='public-read')
	print (response)
except Exception as error:
	print (error)
	
try:
	webPage = s3client.upload_file("index.html","alexbucket321","index.html",ExtraArgs={'ContentType':'text/html', 'ACL' : 'public-read'})
	print ("Index page uploaded...")
 
except Exception as error:
	print ("Error uploading Index file")
	print (error) 
 
 #----->Adding a new file {css file}
try:
	cssPage = s3client.upload_file("style.css","alexbucket321","style.css",ExtraArgs={'ContentType':'text/css', 'ACL' : 'public-read'})
	print ("Css page uploaded...")  
 
except Exception as error:
	print ("Error uploading Index file")
	print (error)

 # Define the website configuration
website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}   	

s3client.put_bucket_website(Bucket='alexbucket321',
                      WebsiteConfiguration=website_configuration)

result = s3client.get_bucket_website(Bucket='alexbucket321')
    	
#Launch Browser to display URL
try:
    webbrowser.open_new_tab('http://alexbucket321.s3-website-eu-west-1.amazonaws.com/')
    print ("S3 Website is now up")
except Exception as error:
    print("Opening Instance webPage failed")

ipaddress = instance[0].public_ip_address
try:
	time.sleep(40)
	webbrowser.open_new_tab('http://'+ipaddress)
	print ("EC2 Website is now up")
except Exception as error:
    print("Opening Instance webPage failed")
 
#Additional functionality

 #Deletes Bucket Contents
s3contents = boto3.resource('s3')
bucket = s3contents.Bucket('alexbucket321')
for key in bucket.objects.all():
 try:
    time.sleep(25)
    response = key.delete()
    print (response)
    print("Bucket contents deleting....")
 except Exception as error:
    print ("Error deleting Bucket Contents")
    
#Deletes Bucket 
s3_deleteBuc = boto3.resource('s3')
bucket = s3_deleteBuc.Bucket('alexbucket321')
try:
    time.sleep(10)
    response = bucket.delete()
    print (response)
    print("Bucket Deleted")
except Exception as error:
    print ("Error Deleting Bucket")
 
#Deletes Instance 
ec2_terminateInstance = boto3.resource('ec2') 
try:
    time.sleep(10)
    instance = ec2_terminateInstance.Instance(instance[0].id)
    response = instance.terminate()
    print (response)
    print("Instance Terminated")
except Exception as error:
    print ("Error in terminating instance")
	
print("****************Thank you for using this script****************")
print("*****Student Name:AlexanderGeonlebedum-20088717****************")	
 
 
    	
