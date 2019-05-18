#
#Ponto 3
#José Morais nº15100
import os
import subprocess
import string 
from ponto1 import *

def user_input():
	global resolv_dns_file, zone_forward, dominio_input, hosts_file, ip_input

	dominio_input = raw_input("Insira o dominio: ")

	zone_forward = '\nzone "'+dominio_input+'" IN { \n	type master;\n	file "/var/named/'+dominio_input+'.hosts";\n};'

	ip_input = raw_input("Insira o IP para o dominio: ")

	hosts_file = '$TTL 38400\n@	IN	SOA	projecto.pt. mail.'+dominio_input+'.(\n			100;\n			10800;\n			3600;\n			684000;\n			38400;\n			)\n	IN	NS	projecto.pt.\n	IN	A	'+ip_input
	
	resolv_dns_file = 'search projecto.pt\nnameserver 127.0.0.1'

def config_httpd_conf():
	portaTCP = raw_input("Insira a porta TCP: ")

	subprocess.check_call("service httpd start".split())

	subprocess.check_call("chkconfig httpd on".split())
	listenTCP = "Listen "+portaTCP+"\n"
	nameVirtualHost = "NameVirtualHost "+ip_input+":"+portaTCP+"\n"
	virtualHost = "<VirtualHost "+ip_input+":"+portaTCP+">"
	file = open("/etc/httpd/conf/httpd.conf").read()
	with open("/etc/httpd/conf/httpd.conf", "a") as myfile:
		if listenTCP not in file:	
			myfile.write(listenTCP)
		if nameVirtualHost not in file:
			myfile.write(nameVirtualHost)
		if virtualHost not in file:
			addVirtualHost = virtualHost+"\n	ServerName www."+dominio_input+"\n	DocumentRoot /"+dominio_input+"\n	ServerAlias "+dominio_input+"\n</VirtualHost>\n"
			myfile.write(addVirtualHost)

def create_html_page():
	directory = "/"+dominio_input+"/"
	if not os.path.exists(directory):
    		os.makedirs(directory)
	with open(directory+"/index.html", "w") as myfile:
		html = "<html>\n	<body>\n		<h1>Pagina "+dominio_input+"</h1>\n	</body>\n</html>"
		myfile.write(html)
	subprocess.check_call("service httpd restart".split())

def run_scripts():
	user_input()
	replace_lines()
	write_resolv_file(resolv_dns_file)
	create_zone(zone_forward, dominio_input)
	create_hosts_file(dominio_input, hosts_file)
	config_httpd_conf()
	create_html_page()

if __name__ == '__main__':
	os.system("rpm -qa > installedPackages.txt")
	packageList = open("installedPackages.txt").read()
	if "bind" not in packageList:
		os.system("yum install bind* -y")
	if "httpd" not in packageList:
		os.system("yum install httpd* -y")
	run_scripts()
	restart_named()
	