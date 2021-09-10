from nbgrader.apps import NbGraderAPI
from traitlets.config import Config
from Util import filemanager
import settings
import secrets

# create a custom config object to specify options for nbgrader
config = Config()
config.CourseDirectory.course_id = settings.NBGRADER_DIR
config.CourseDirectory.db_url = "sqlite:///" + settings.NBGRADER_DIR + "gradebook.db"
config.CourseDirectory.source_directory = settings.NBGRADER_DIR + "source"
config.CourseDirectory.release_directory = settings.NBGRADER_DIR + "release"
config.CourseDirectory.submitted_directory = settings.NBGRADER_DIR + "submitted"
config.CourseDirectory.autograded_directory = settings.NBGRADER_DIR + "autograded"
config.CourseDirectory.feedback_directory = settings.NBGRADER_DIR + "feedback"

api = NbGraderAPI(config=config)


def _generate_user():
    return secrets.token_hex(16)


def generate(assignment_id):
    return api.generate_assignment(assignment_id)


def autograde(assigment_id, user_id):
    return api.autograde(assigment_id, user_id)


def get_submission(assigment_id, user_id):
    return api.get_student_notebook_submissions(user_id, assigment_id)


def _get_score(assigment_id, user_id):
    res = get_submission(assigment_id, user_id)
    return int(res[0]["score"]), int(res[0]["max_score"])


def grade(filename, assignment_id, problem_id):
    user_id = _generate_user()
    submitted_folder = f'{settings.NBGRADER_DIR}submitted/{user_id}/{assignment_id}'
    submitted_filename = f'{problem_id}.ipynb'
    filemanager.copy_file(filename, submitted_folder, submitted_filename)
    autograde(assignment_id, user_id)
    score, max_score = _get_score(assignment_id, user_id)
    return {"score": score, "max_score": max_score}
