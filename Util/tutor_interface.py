import json
import requests


def get_xqueue_response(user_config, client_func_name, *args, **kwargs):
    client = Client(user_config)
    func = getattr(client, client_func_name)
    result = func(*args, **kwargs)
    return result


class Client:
    def __init__(self, user_config, url=None):
        self._session = None
        self.username = user_config["XQUEUE_AUTH_USERNAME"]
        self.password = user_config["XQUEUE_AUTH_PASSWORD"]

        self.base_url = url
        if not self.base_url:
            scheme = "https" if user_config["ACTIVATE_HTTPS"] else "http"
            host = user_config["XQUEUE_HOST"]
            self.base_url = "{}://{}".format(scheme, host)
        self.login()

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def url(self, endpoint):
        # Don't forget to add a trailing slash to all endpoints: this is how xqueue
        # works...
        return self.base_url + endpoint

    def login(self):
        response = self.request(
            "/xqueue/login/",
            method="POST",
            data={"username": self.username, "password": self.password},
        )
        message = response.get("content")
        if message != "Logged in":
            print(
                "Could not login to xqueue server at {}. Response: '{}'".format(
                    self.base_url, message
                )
            )

    def show_submission(self, queue="openedx"):
        response = self.request("/xqueue/get_submission/", params={"queue_name": queue})
        if response["return_code"] != 0:
            return response
        data = json.loads(response["content"])
        header = json.loads(data["xqueue_header"])
        submission_body = json.loads(data["xqueue_body"])
        submission_id = header["submission_id"]
        submission_key = header["submission_key"]
        submission_files = {}
        for filename, path in json.loads(data["xqueue_files"]).items():
            if not path.startswith("http"):
                # Relative path: prepend with server url
                path = self.base_url + "/" + path
            submission_files[filename] = path
        return {
            "id": submission_id,
            "key": submission_key,
            "body": submission_body,
            "files": submission_files,
            "return_code": response["return_code"],
        }

    def count_submissions(self, queue="openedx"):
        return self.request("/xqueue/get_queuelen/", params={"queue_name": queue})

    def grade_submission(self, submission_id, submission_key, grade, correct, msg):
        return self.request(
            "/xqueue/put_result/",
            method="POST",
            data={
                "xqueue_header": json.dumps(
                    {"submission_id": submission_id, "submission_key": submission_key}
                ),
                "xqueue_body": json.dumps(
                    {"correct": correct, "score": grade, "msg": msg}
                ),
            },
        )

    def request(self, endpoint, method="GET", data=None, params=None):
        func = getattr(self.session, method.lower())
        response = func(self.url(endpoint), data=data, params=params)
        # TODO handle errors >= 400 and non-parsable json responses
        return response.json()


# user_config = {
#     "XQUEUE_AUTH_USERNAME": "lms",
#     "XQUEUE_AUTH_PASSWORD": "mVlLdT1h",
#     "ACTIVATE_HTTPS": False,
#     "XQUEUE_HOST": "xqueue.learn-ai.t.innosoft.kmutt.ac.th"
# }
#
# get_xqueue_response(user_config, "count_submissions", "openedx")
