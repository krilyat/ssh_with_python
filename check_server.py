import paramiko
import argparse
import cmd


parser = argparse.ArgumentParser(description='Retrive som information via ssh (paramiko)')
parser.add_argument('-f', '--file', help='file containing server to check')
parser.add_argument('-s', '--server', help='specify server')
parser.add_argument('-u', '--user', help='specify user')
parser.add_argument('-p', '--pass', action='store_true',  help='ask for password')
parser.add_argument('-S', '--scenario', help='scenario to play')
parser.add_argument('-c', '--command', type=str, help='command')


args = parser.parse_args()
'''
class RunCommand(cmd.Cmd):
    """ Simple shell to run a command on the host """

    prompt = 'ssh > '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.hosts = []
        self.connections = []

    def do_add_host(self, args):
        """add_host
        Add the host to the host list"""
        if args:
            self.hosts.append(args.split(','))
        else:
            print "usage: host "

    def do_connect(self, args):
        """Connect to all hosts in the hosts list"""
        for host in self.hosts:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            client.connect(host[0],
                           username=host[1],
                           password=host[2])
            self.connections.append(client)

    def do_run(self, command):
        """run
        Execute this command on all hosts in the list"""
        if command:
            for host, conn in zip(self.hosts, self.connections):
                stdin, stdout, stderr = conn.exec_command(command)
                stdin.close()
                for line in stdout.read().splitlines():
                    print 'host: %s: %s' % (host[0], line)
        else:
            print "usage: run "

    def do_close(self, args):
        for conn in self.connections:
            conn.close()
'''

def main():
    print args




if __name__ == '__main__':
    main()
