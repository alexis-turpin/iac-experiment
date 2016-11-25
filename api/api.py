import tornado.web
from tornado.ioloop import IOLoop
import allBananasHandler
import homeHandler
import singleBananaHandler
import requests
import boto3
import json


class Application(tornado.web.Application):
    def __init__(self, settings):
        handlers = [
            (r"/?", homeHandler.Home, settings),
            (r"/banana/?", allBananasHandler.AllBananas, settings),
            (r"/banana/([^/]*)", singleBananaHandler.SingleBanana, settings)
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)


def get_settings():
    try:
        sg = requests.get("http://169.254.169.254/latest/meta-data/security-groups").text
        infra = sg.split("-")[0]
    except Exception as e:
        print("No AWS infrastructure detected, localhost configuration loaded\n", str(e))
        return {
            "db_user": "root",
            "db_passwd": "Password01",
            "db_endpoint": "localhost",
            "db_name": "bananadb",
        }
    else:
        # Get the database config file from S3
        s3 = boto3.client("s3")
        file = s3.get_object(Bucket="terraform-states-iac-experiment", Key=infra+"/data.tfstate")
        file_js = json.loads(file["Body"].read().decode("utf-8"))
        db_conf = file_js["modules"][1]["resources"]["aws_db_instance.main"]["primary"]["attributes"]
        return {
            "db_user": db_conf["username"],
            "db_passwd": db_conf["password"],
            "db_endpoint": db_conf["address"],
            "db_name": db_conf["name"],
        }
        # TODO : Test from EC2 with right IAM role (S3 read)


def main():
    settings = get_settings()
    app = Application(settings)
    app.listen(8080)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
