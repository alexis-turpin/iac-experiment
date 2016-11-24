import tornado.web
import pymysql

class InitializationHandler(tornado.web.RequestHandler):

    def initialize(
            self,
            db_user,
            db_passwd,
            db_endpoint,
            db_name,
            api_dns_name
    ):
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db_endpoint = db_endpoint
        self.db_name = db_name
        self.api_dns_name = api_dns_name

    def connect_db(self):
        return pymysql.connect(
            self.db_endpoint,
            self.db_user,
            self.db_passwd,
            self.db_name,
        )
