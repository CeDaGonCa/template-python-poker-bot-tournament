import os


def run_test(room, type, times):
    os.system("python main.py --host ws.turingpoker.com --port 80 --room " + str(room) + " --username foe")


run_test("11135", "insecure", 1)
