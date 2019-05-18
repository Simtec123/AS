#
#Ponto 6
#José Morais nº15100
import os
import subprocess
import string
import fileinput

def create_user_input():
    global dir_input, ip_input, netmask_input
    dir_input = raw_input("Insira a directoria a ser partilhada: ")
    ip_input = raw_input("Insira o IP da network: ")
    netmask_input = raw_input("Insira os bits da Netmask: ")

def directory_creation():
    global directory
    directory = "/"+dir_input+"/"
    if not os.path.exists(directory):
    		os.makedirs(directory)

    os.system("chown 65534.65534 "+directory+"")
    os.system("chmod 755 "+directory+"")

def write_exports(direct, ip, mask, optWrite, optHide, optSync):
    export_line = ""+direct+" "+ip+"/"+mask+"("+optWrite+","+optHide+","+optSync+")"
    file = open("/etc/exports").read()
    with open("/etc/exports", "a") as myfile:
        if direct  not in file:
            myfile.write("\n"+ export_line)

def options():
    global option_write
    option_write = raw_input("Insira a opcao rw ou ro: ")

    if option_write not in ('rw', 'ro'):
        print('Input Invalido')
        options()
    
    option_hide()

def option_hide():
    global option_hide_write
    option_hide_write = raw_input("Insira a opcao hide ou nohide: ")

    if option_hide_write not in ('hide', 'nohide'):
        print('Input Invalido')
        option_hide()

    option_sync()

def option_sync():
    global option_sync_write
    option_sync_write = raw_input("Insira a opcao sync ou async: ")

    if option_sync_write not in ('sync', 'async'):
        print('Input Invalido')
        option_sync()  

def delete_partilha():
    dir_to_delete_input = raw_input("Insira a directoria a ser eliminada: ")

    delete_line(dir_to_delete_input)
    
    os.system("rm -r /"+dir_to_delete_input+"/")

def change_partilha():
    global directory_to_change, ip_to_change_input, netmask_to_change_input    
    dir_to_change_input = raw_input("Insira a directoria a ser alterada: ")
    directory_to_change = "/"+dir_to_change_input+"/"
    ip_to_change_input = raw_input("Insira o IP da network: ")
    netmask_to_change_input = raw_input("Insira os bits da Netmask: ")

def delete_line(stringToFind):
    fin = open("/etc/exports", "r")
    data = fin.readlines()
    fin.close()

    for i, line in enumerate(data):
        if stringToFind in line:
            del data[i:i+1]
            print("sucesso")
    
    fout = open("/etc/exports", "w")
    fout.writelines(data)
    fout.close()

def restart_services():
    subprocess.check_call("service rpcbind restart".split())
    subprocess.check_call("service nfs restart".split())

def input_switch():
    selection = raw_input("Insira uma opcao: \n1 - Criar partilha\n2 - Alterar partilha\n3 - Eliminar partilha\n")
    
    if selection == '1':
        create_user_input()
        directory_creation()
        options()
        write_exports(directory, ip_input, netmask_input, option_write, option_hide_write, option_sync_write)
        restart_services()
    elif selection == '2':
        change_partilha()
        options()
        delete_line(directory_to_change)
        write_exports(directory_to_change, ip_to_change_input, netmask_to_change_input, option_write, option_hide_write, option_sync_write)
        restart_services()
    elif selection == '3':
        delete_partilha()
        restart_services()
    else:
        print("Input invalido")
        input_switch()

if __name__ == '__main__':
    os.system("rpm -qa > installedPackages.txt")
    packageList = open("installedPackages.txt").read()
    if "nfs" not in packageList:
        os.system("yum install nfs* -y")
    restart_services()
    input_switch()