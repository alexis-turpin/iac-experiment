from tornado import httpserver
from tornado.ioloop import IOLoop
import tornado.web
import requests
import all_bananas_handler
import home_handler
import single_banana_handler


class Application(tornado.web.Application):
    def __init__(self, settings):
        handlers = [
            (r"/?", home_handler.Home, settings),
            (r"/banana/?", all_bananas_handler.AllBananas, settings),
            (r"/banana/([^/]*)", single_banana_handler.SingleBanana, settings),
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)

def get_settings():
    """
    """
    # TODO pydoc
    try:
        url = "http://169.254.169.254/latest/meta-data/security-groups"
        sg = requests.get(url).text
        infra = sg.split("-")[0]
    except Exception as e:
        print("No AWS infrastructure detected, "
              "localhost configuration loaded\n", str(e))
        return {
            "front_ip": "192.168.65.140:8080",
            "back_ip": "192.168.65.132:8080",
            "infra": "Local",
        }
    else:
        # Get the database config file from S3
        # TODO check the tfstate file to extract the values
        return {
            "front_ip": "192.168.65.140:8080",
            "back_ip": "192.168.65.132:8080",
            "infra": infra
        }


def main():
    settings = get_settings()
    app = Application(settings)
    app.listen(8080)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
