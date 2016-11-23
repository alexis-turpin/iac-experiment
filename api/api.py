import pymysql.cursors
import tornado.web
from tornado.ioloop import IOLoop
import allBananasHandler
import homeHandler
import singleBananaHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", homeHandler.Home),
            (r"/banana/?", allBananasHandler.AllBananas),
            (r"/banana/([^/]*)", singleBananaHandler.SingleBanana)
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)


# def get_settings():
#     # TODO : Get the DB_USER / PASSWD / API_DNS_NAME / DB_NAME
#         # from the terraform remote state on S3 (boto3)
#     DB_USER = "root"
#     DB_PASSWD = "Password01"
#     DB_ENDPOINT = "localhost"
#     DB_NAME = "bananadb"
#     API_DNS_NAME = None


def connect_db():
    DB_USER = "root"
    DB_PASSWD = "Password01"
    DB_ENDPOINT = "localhost"
    DB_NAME = "bananadb"
    API_DNS_NAME = None
    return pymysql.connect(
        DB_ENDPOINT,
        DB_USER,
        DB_PASSWD,
        DB_NAME,
    )


def main():
    # Verify the database exists and has the correct layout
    app = Application()
    app.listen(8080)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
