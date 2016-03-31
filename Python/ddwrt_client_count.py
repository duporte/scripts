#!/usr/bin/python
# Nome:      ddwrt_client_count
# Descrição: Plugin do Nagios para retornar o número de usuários conectados
#            em um roteador com a firmware dd-wrt através da quantidade de
#            DHCP leases.
#
# Obs.: O acesso telnet deve estar habilitado para o funcionamento do script.
#
import telnetlib
import re
import sys
import getopt

def main(argv):
    host = ""
    warn = ""
    crit = ""
    user = "USUARIO"
    password = "SENHA"

    try:
        opts, args = getopt.getopt(argv,"hH:w:c:", ["host=", "warn=", "crit="])
    except getopt.GetoptError:
        print "check_wireless_clients -H <host> -w <warn> -c <crit>"
        exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print "check_wireless_clients -H <host> -w <warn> -c <crit>"
            exit()
        elif opt in ("-H"):
            host = arg
        elif opt in ("-w"):
            warn = arg
        elif opt in ("-c"):
            crit = arg

    tn = telnetlib.Telnet(host)

    tn.read_until("login: ")
    tn.write(user + "\n")

    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")
        tn.write("wl_atheros assoclist\n")
        tn.write("exit\n")

        clients = len(re.findall(r'([0-9A-F]{2}(?::[0-9A-F]{2}){5})', tn.read_all()))

        print "Clientes conectados: %d | clients=%d" % (clients, clients)

        if clients >= warn and warn < crit:
            exit(1)
        if clients >= crit:
            exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
