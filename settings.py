import tutor

# $(tutor config printroot)/data/xqueue/media/openedx
SAVE_FILE_DIR = "/home/title/.local/share/tutor/data/xqueue/media/openedx/"

# use relative path for nbgrader
NBGRADER_DIR = "./nbgrader_workspace/"

# tutor config
tutor_config = {
    "XQUEUE_AUTH_USERNAME": "lms",
    "XQUEUE_AUTH_PASSWORD": tutor.USERS.get('lms'),
    "ACTIVATE_HTTPS": False,
    "XQUEUE_HOST": "xqueue.learn-ai.t.innosoft.kmutt.ac.th"
}