import os
import time
from anytree import Node, RenderTree


class ConsoleOutput:
    def __init__(self, debug=False):
        self.debug = debug
        self.to_draw = []
        self.root = None
        self.nodes = {}

    def make_tree(self):
        self.nodes = {}
        root = self.to_draw[0].split("/")[2]
        self.root = Node(root, str_name=root)
        self.nodes[root] = self.root
        for line in self.to_draw:
            path = line.split("/")[2:]
            path = path if path[-1] else path[:-1]
            name = path[-1]
            try:
                parent = self.nodes[path[-2]]
            except (IndexError, KeyError):
                continue
            self.nodes[name] = Node(name, parent=parent, str_name=line)

    def draw(self, processes, started, last_found, threads, amount_found):
        self.banner()
        self.lolprint("{} processes {} threads running!".format(processes, threads))
        self.lolprint("running for: {} seconds".format(int(time.time() - started)))
        self.lolprint("last found {} seconds ago".format(int(time.time() - last_found)))
        self.lolprint("{} items found!".format(amount_found))
        for pre, _, node in RenderTree(self.root):
            self.lolprint("{}{}".format(pre, node.str_name))

    def clear(self):
        os.system("clear")

    def refresh(self, to_draw=None, processes=0, started=0, last_found=0, threads=0, amount_found=0):
        if self.debug:
            return

        if to_draw:
            self.to_draw = to_draw
        self.make_tree()
        self.clear()
        self.draw(processes, started, last_found, threads, amount_found)

    def lolprint(self, string):
        print(string)

    def banner(self):
        self.lolprint("Treebuster - recursive Gobuster")