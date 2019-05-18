#
#Ponto 5
#José Morais nº15100
import os
import subprocess
import string 
from ponto1 import *

def user_input():
	global gama_ip, fqdn, ip, zone, reverse, resolv_dns
	gama_ip = raw_input("Insira o IP para a zona reverse: ")
	fqdn = raw_input("Insira o FQDN: ")
	ip = raw_input("Insira o IP para o FQDN: ")

	zone = 'zone "'+gama_ip+'.in-addr.arpa" IN { \n	type master;\n	file "/var/named/reverse.'+fqdn+'";\n};'

	reverse = '$TTL 38400\n@	IN	SOA	@ root(\n			100;\n			10800;\n			3600;\n			684000;\n			38400;\n			)\n	IN	NS	trabalho.pt.\n'+ip+'	IN	PTR	'+fqdn+'.\n'

	resolv_dns = "search projecto.pt\nnameserver 127.0.0.1"

def write_reverse():
	file = open("/etc/named.conf").read()
	if gama_ip not in file:
		create_zone(zone, gama_ip)

def create_reverse_fqdn_file(fqdn, reverse):
	with open('/var/named/reverse.'+fqdn+'', 'w') as myfile:
		myfile.write(reverse)

if __name__ == '__main__':
	os.system("rpm -qa > installedPackages.txt")
	packageList = open("installedPackages.txt").read()
	if "bind" not in packageList:
		os.system("yum install bind* -y")
	user_input()
	write_reverse()
	write_resolv_file(resolv_dns)
	create_reverse_fqdn_file(fqdn, reverse)
	replace_lines()
	restart_named()