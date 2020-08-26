import select
import subprocess
import sys


class Launcher:
    def __init__(self, target):
        self.target = target
        self.processes = {}

        self.absolute_thread_limit = 200
        self.thread_limit_per_process = 12
        self.gobuster_path = "" #CHANGE ME!!
        self.gobuster_params = "-u {target} -w {wordlist} --wildcard -q -e -k -t {threads} dir"
        self.extensions = "-x txt,xml,php"
        self.wordlist = "" #CHANGE ME!!

    def launch_gobuster(self, target=None):
        target = target if target else self.target
        thread_amount = self.get_appropiate_thread_amount()
        params = self.gobuster_params.format(target=target, wordlist=self.wordlist, threads=thread_amount)
        command = "{} {} {}".format(self.gobuster_path, params, self.extensions)
        self.new_subprocess(command, target, thread_amount)

    def new_subprocess(self, command, target_name, thread_amount):
        command_list = command.split()
        process = subprocess.Popen(command_list, stderr=sys.stdout, stdout=subprocess.PIPE)
        self.processes[target_name] = [process, thread_amount]
        return process

    def poll_processes(self):
        to_delete = []
        to_return = []
        # debugging only
        import random
        id = random.randint(0, 100)
        for name, process in self.processes.items():
            process, *_ = process
            while select.select([process.stdout], [], [], 0.5)[0]:
                to_return.append(process.stdout.readline())
            if process.poll():
                to_delete.append(name)

        for name in to_delete:
            del self.processes[name]

        return to_return

    def used_threads(self):
        return sum([process[1] for process in self.processes.values()])

    def get_appropiate_thread_amount(self):
        used_threads = self.used_threads()
        available = self.absolute_thread_limit - used_threads
        if available > self.thread_limit_per_process:
            return self.thread_limit_per_process
        elif available > 1:
            return available // 2
        else:
            return 1

    def clean_up(self):
        names = list(self.processes.keys()).copy()
        for name in names:
            del self.processes[name]
