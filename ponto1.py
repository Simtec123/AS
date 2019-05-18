#
#Ponto 1
#José Morais nº15100
import subprocess
import string 
import os

def domain_input_zone_forward():
	global resolv_dns_file, zone_forward, dominio_input, hosts_file
	
	dominio_input = raw_input("Insira o dominio: ")
	
	zone_forward = '\nzone '+dominio_input+' IN { \n	type master;\n	file "/var/named/'+dominio_input+'.hosts";\n};'
	hosts_file = '$TTL 38400\n@	IN	SOA	projecto.pt. mail.'+dominio_input+'.(\n			100;\n			10800;\n			3600;\n			684000;\n			38400;\n			)\n	IN	NS	projecto.pt.\n	IN	A	127.0.0.1'
	resolv_dns_file = 'search projecto.pt\nnameserver 127.0.0.1'

def replace_lines():
	s = open("/etc/named.conf").read()
	s = s.replace('listen-on port 53 { 127.0.0.1; };', 'listen-on port 53 { 127.0.0.1; any;};')
	s = s.replace('allow-query     { localhost; };', 'allow-query     { localhost; any;};')
	f = open("/etc/named.conf", 'w')
	f.write(s)
	f.close()

def create_zone(zone, dominio):
	file = open("/etc/named.conf").read()
	with open("/etc/named.conf", "a") as myfile:
		if dominio  not in file:
			myfile.write("\n"+ zone)	

def create_hosts_file(dominio, hosts):
	with open("/var/named/"+dominio+".hosts", "w") as myfile:
		myfile.write(hosts)

def write_resolv_file(resolv_dns):
	with open("/etc/resolv.conf", "w") as myfile:
		myfile.write(resolv_dns)

def restart_named():
	subprocess.check_call("service named restart".split())

def run_scripts():
	domain_input_zone_forward()
	replace_lines()
	write_resolv_file(resolv_dns_file)
	create_zone(zone_forward, dominio_input)
	create_hosts_file(dominio_input, hosts_file)
        
if __name__=='__main__':
	os.system("rpm -qa > installedPackages.txt")
	packageList = open("installedPackages.txt").read()
	if "bind" not in packageList:
		os.system("yum install bind* -y")
	run_scripts()
	restart_named()
