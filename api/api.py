import tornado.web
from tornado.ioloop import IOLoop
import all_bananas_handler
import home_handler
import single_banana_handler
import requests
import boto3
import json


class Application(tornado.web.Application):
    """Main application of the project

    Define the main web application of the project. Receive a settings dict
    and pass it through to all its handlers.
    Automatically reloads on file changes.
    Manages following path:
        /
        /banana/
        /banana/id

    Args:
        DICT settings: A dict containing all the needed key:value pair to
        allow handlers to connect to the project DB.
            Mandatory Keys:db_user, db_passwd, db_endpoint, db_name.
    """
    def __init__(self, settings):
        handlers = [
            (r"/?", home_handler.Home, settings),
            (r"/banana/?", all_bananas_handler.AllBananas, settings),
            (r"/banana/([^/]*)", single_banana_handler.SingleBanana, settings)
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)


def get_settings():
    """Get database settings

    Try to get database settings (user, password, endpoint, name) from a
    terraform remote state on an S3 bucket. It will guess the right S3 key from
    the instance security-group name.
    If not AWS hosted it will default to localhost dev values.

    Returns:
        A dict containing DB settings to use by all handler in order to connect
        to the project DB. Or default local value if not AWS hosted
        Example (not AWS hosted):
            {
                "db_user": "root",
                "db_passwd": "Password01",
                "db_endpoint": "localhost",
                "db_name": "bananadb",
            }
    """
    try:
        url = "http://169.254.169.254/latest/meta-data/security-groups"
        sg = requests.get(url).text
        infra = sg.split("-")[0]
    except Exception as e:
        print("No AWS infrastructure detected, "
              "localhost configuration loaded\n", str(e))
        return {
            "db_user": "root",
            "db_passwd": "Password01",
            "db_endpoint": "localhost",
            "db_name": "bananadb",
        }
    else:
        # Get the database config file from S3
        s3 = boto3.client("s3")
        file = s3.get_object(Bucket="terraform-states-iac-experiment",
                             Key=infra+"/data.tfstate")
        file_js = json.loads(file["Body"].read().decode("utf-8"))
        db_conf = file_js["modules"][1]["resources"]["aws_db_instance.main"]
        return {
            "db_user": db_conf["primary"]["attributes"]["username"],
            "db_passwd": db_conf["primary"]["attributes"]["password"],
            "db_endpoint": db_conf["primary"]["attributes"]["address"],
            "db_name": db_conf["primary"]["attributes"]["name"],
        }
        # TODO : Test from EC2 with right IAM role (S3 read)


def main():
    settings = get_settings()
    app = Application(settings)
    app.listen(8080)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
