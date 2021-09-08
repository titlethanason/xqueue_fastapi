from nbgrader.apps import NbGraderAPI
from traitlets.config import Config
import settings

# create a custom config object to specify options for nbgrader
config = Config()
config.CourseDirectory.course_id = settings.NBGRADER_DIR

api = NbGraderAPI(config=config)
