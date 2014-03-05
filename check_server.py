import paramiko
import argparse
import cmd

from getpass import getpass


parser = argparse.ArgumentParser(description='Retrive som information via ssh (paramiko)')
serverlist = parser.add_argument_group('ServerList', 'Server List options')
serverlist.add_argument('-f', '--file', type=str, help='file containing server to check')
serverlist.add_argument('-i', '--interlace', action='store_true', help='launch one commande at a time on each host')
server = parser.add_argument_group('Server', 'Single server options')
server.add_argument('-s', '--server', help='specify server')
server.add_argument('-u', '--user', help='specify user')
server.add_argument('-p', '--password', action='store_true',  help='ask for password')
parser.add_argument('-c', '--command', type=str, help='command')
parser.add_argument('-S', '--scenario', type=str, help='scenario to play')
parser.add_argument('--silent', action='store_true', help='print only result of the command')

args = parser.parse_args()

hosts = []
connections = []

def main():
    if args.file:
        processServerList()

    if args.server:
        processServer()

def processServerList():
    with open(args.file, 'r') as List:
        for line in List:
            if line[0] != '#':
                hosts.append(line.split(','))

    connect()
    if args.interlace:
        with open(args.scenario, 'r') as scenario:
            for command in scenario:
                runall(command)
    else:
        for host, conn in zip(hosts, connections):
            with open(args.scenario, 'r') as scenario:
                for command in scenario:
                    run(command, host, conn)
    

    close()

def processServer():
    if args.password:
        password = getpass('password for %s: ' % args.server)
        hosts.append([args.server, args.user, password])

    connect()
    runall(args.command)
    close()


def connect():
    for host in hosts:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host[0],username=host[1],password=host[2])
        connections.append(client)
 
def runall(command):
    for host, conn in zip(hosts, connections):
        run(command, host, conn)

def run(command, host, conn):
    if command[0] == '"':
        print command.lstrip('"').replace('\n', '')
    elif command[0] == ";":
        prefix, suffix, subcmd, subprefix, subsuffix, cmd, = command.lstrip(';').split(';') 
        stdin, stdout, stderr = conn.exec_command(cmd)
        stdin.close()
        for line in stdout.read().splitlines():
            if args.silent:
                interpret(host, conn, line, prefix, suffix, subcmd, subprefix, subsuffix)
            else:
                print 'host: %s: %s' % (host[0], line)
    elif command[0] == ":":
        prefix, suffix, subcmd, subprefix, subsuffix, cmd, = command.lstrip(':').split(':') 
        stdin, stdout, stderr = conn.exec_command(cmd)
        stdin.close()
        for line in stdout.read().splitlines():
            if args.silent:
                interpret(host, conn, line, prefix, suffix, subcmd, subprefix, subsuffix)
            else:
                print 'host: %s: %s' % (host[0], line)
    else:
        stdin, stdout, stderr = conn.exec_command(command)
        stdin.close()
        for line in stdout.read().splitlines():
            if args.silent:
                print line
            else:
                print 'host: %s: %s' % (host[0], line)

def interpret(host, conn, line, prefix, suffix, subcmd, subprefix, subsuffix):
    print '%s%s%s' % (prefix, line, suffix)
    if subcmd:
        if subprefix:
            print subprefix
        run("%s" % (subcmd.replace('{}', line)), host, conn)
        if subsuffix:
            print subsuffix
    
def close():
    for conn in connections:
        conn.close()

if __name__ == '__main__':
    main()
