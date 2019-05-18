#
#Ponto 6
#José Morais nº15100
import os
import subprocess
import string 
from ponto1 import restart_named

def delete_zone_forward():
    dominio_to_delete = raw_input("Insira  o dominio a eliminar: ")

    delete_lines_zone(dominio_to_delete)

    os.system("rm /var/named/"+dominio_to_delete+".hosts")

def delete_zone_reverse():
    ip_to_delete = raw_input("Insira o IP para da zona reverse a eliminar: ")
    fqdn = raw_input("Insira o FQDN a eliminar: ")

    delete_lines_zone(ip_to_delete)

    os.system('rm /var/named/reverse.'+fqdn+'')

def delete_virtualHost():
    dominio_to_delete = raw_input("Insira  o dominio a eliminar: ")
    ip_input = raw_input("Insira o IP do dominio a eliminar: ")

    delete_lines_zone(dominio_to_delete)

    os.system("rm /var/named/"+dominio_to_delete+".hosts")
    os.system("rm -r /"+dominio_to_delete+"/")

    fin = open("/etc/httpd/conf/httpd.conf", "r")
    data = fin.readlines()
    fin.close()

    for i, line in enumerate(data):
        if ip_input in line:
            del data[i:i+6]
    
    fout = open("/etc/httpd/conf/httpd.conf", "w")
    fout.writelines(data)
    fout.close()

def delete_lines_zone(dominio):
    fin = open("/etc/named.conf", "r")
    data = fin.readlines()
    fin.close()

    for i, line in enumerate(data):
        if dominio in line:
            del data[i:i+4]
    
    fout = open("/etc/named.conf", "w")
    fout.writelines(data)
    fout.close()

def input_switch():
    selection = raw_input("Insira uma opcao: \n1 - Delete Zone Forward\n2 - Delete Zone Reverse\n3 - Delete VirtualHosts\n")
    
    if selection == '1':
        delete_zone_forward()
        restart_named()
    elif selection == '2':
        delete_zone_reverse()
        restart_named()
    elif selection == '3':
        delete_virtualHost()
        restart_named()
        subprocess.check_call("service httpd restart".split())
    else:
        print("Input invalido")
        input_switch()

if __name__ == '__main__':
    input_switch()