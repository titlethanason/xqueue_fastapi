from Problem import *


def handle(request):
    problem_number = eval(request["body"]["grader_payload"])["problem_number"]
    if problem_number == 1:
        file = request["file"]
        filename = list(file.values())[0].split("/")[-1]
        return problem1.process(filename)

    elif problem_number == 2:
        code = request["body"]["student_response"]
        return problem2.process(code)
