import tornado.web
from tornado.ioloop import IOLoop
import allBananasHandler
import homeHandler
import singleBananaHandler


class Application(tornado.web.Application):
    def __init__(self, settings):
        handlers = [
            (r"/?", homeHandler.Home, settings),
            (r"/banana/?", allBananasHandler.AllBananas, settings),
            (r"/banana/([^/]*)", singleBananaHandler.SingleBanana, settings)
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)

def get_settings():
    # TODO : Get the DB_USER / PASSWD / API_DNS_NAME / DB_NAME
        # from the terraform remote state on S3 (boto3)
    return {
        "db_user": "root",
        "db_passwd": "Password01",
        "db_endpoint": "localhost",
        "db_name": "bananadb",
        "api_dns_name": "http://192.168.65.132:8080"
    }


def main():
    settings = get_settings()
    app = Application(settings)
    app.listen(8080)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
