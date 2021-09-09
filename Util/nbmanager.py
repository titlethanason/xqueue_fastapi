from nbgrader.apps import NbGraderAPI
from nbgrader.coursedir import CourseDirectory
from traitlets.config import Config
import settings

# create a custom config object to specify options for nbgrader
config = Config()
config.CourseDirectory.course_id = settings.NBGRADER_DIR
config.CourseDirectory.db_url = "sqlite:///"+settings.NBGRADER_DIR+"gradebook.db"
config.CourseDirectory.source_directory = settings.NBGRADER_DIR+"source"
config.CourseDirectory.release_directory = settings.NBGRADER_DIR+"release"
config.CourseDirectory.submitted_directory = settings.NBGRADER_DIR+"submitted"
config.CourseDirectory.autograded_directory = settings.NBGRADER_DIR+"autograded"
config.CourseDirectory.feedback_directory = settings.NBGRADER_DIR+"feedback"


#TODO: complete coursedir using config
api = NbGraderAPI(config=config)


def generate(assignment_id):
    return api.generate_assignment(assignment_id)
