from Problem import *


def handle(request):
    file = request["file"]
    filename = list(file.values())[0].split("/")[-1]
    return problem1.process(filename)
