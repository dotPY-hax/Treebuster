import requests
import sys

from treebuster import Treebuster


def start():
    args = sys.argv
    try:
        target = args[1]
    except IndexError:
        print("NEED A TARGET 'http://<target>!")
        return
    requests.packages.urllib3.disable_warnings()
    try:
        requests.get(target, verify=False)
    except requests.ConnectionError:
        print(target + " seems to be down")
        return
    buster = Treebuster(target)
    buster.run()

start()