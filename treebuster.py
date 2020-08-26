import os
import requests
import time

from console_input import ConsoleInput
from console_output import ConsoleOutput
from html_parser import GetLinks
from launcher import Launcher

requests.packages.urllib3.disable_warnings()


class Treebuster:
    def __init__(self, target):
        self.target = target
        self.launcher = Launcher(self.target)
        self.console = ConsoleOutput(debug=False)
        self.found = []
        self.target_from_listing = []
        self.started = time.time()
        self.last_found = self.started
        self.last_update = 0

    def initiate_first_scan(self):
        self.found = [self.target]
        self.launcher.launch_gobuster()

    def poll(self):
        output = self.launcher.poll_processes()
        found = []
        for line in output:
            line = line.decode("UTF-8").strip()
            if self.target not in line:
                continue
            found.append(line.split()[0])
        self.found += found
        return found

    def is_directory(self, target):
        return "." not in target.split("/")[-1]

    def check_for_404_redirects(self, target):
        result = requests.get(target, verify=False)
        return result.status_code != 404

    def try_to_get_listing(self, target):
        result = requests.get(target, verify=False)
        directory = target.split("/")[-1]
        if not "Index of /{}".format(directory) in result.text:
            return None
        links = GetLinks()
        links = links.feed(result.text)
        fully_qualified = [os.path.join(target, link) for link in links]
        return fully_qualified[1:]

    def branch_out(self, target):
        self.last_found = time.time()
        self.refresh_console()
        if self.is_directory(target) and self.check_for_404_redirects(target):
            found = self.try_to_get_listing(target)
            if not found:
                self.launcher.launch_gobuster(target)
            else:
                self.found += found
                self.target_from_listing += found


    def refresh_console(self):
        self.last_update = time.time()
        self.console.refresh(to_draw=self.found, processes=len(self.launcher.processes.items()), started=self.started,
                             last_found=self.last_found, threads=self.launcher.used_threads(), amount_found=len(self.found))

    def force_console_update(self):
        if time.time() - self.last_update > 5:
            self.refresh_console()

    def main_loop(self):
        self.initiate_first_scan()
        while len(self.launcher.processes):
            new_targets = self.poll()
            new_targets += self.target_from_listing
            self.target_from_listing = []
            for target in new_targets:
                self.branch_out(target)
            else:
                self.force_console_update()

        self.quit()

    def run(self):
        try:
            self.main_loop()
        except KeyboardInterrupt:
            self.quit()
        finally:
            self.launcher.clean_up()

    def quit(self):
        print("bye bye")
        raise exit(0)


