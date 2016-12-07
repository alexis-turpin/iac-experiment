import tornado.web
import pymysql

class InitializationHandler(tornado.web.RequestHandler):
    """Class used to describe common attributes and method of all other
    handlers of this project.

    Completing the tornado.web.RequestHandler Class by adding attributes and
    method needed to connect to remote or local database.

    Attributes:
        db_user: Target database instance username.
        db_passwd: Target database instance password.
        db_endpoint: Target database instance to connect to.
        db_name: Target database to connect to.
    """

    def initialize(
            self,
            db_user,
            db_passwd,
            db_endpoint,
            db_name,
    ):
        """Tornado RequestHandler hook for subclass initialization.

        Received database info as args to allow future connections to DB.
        Called for each request.

        Args:
            STR db_user: Target database instance username.
            STR db_passwd: Target database instance password.
            STR db_endpoint: Target database instance to connect to.
            STR db_name: Target database to connect to.
        """
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db_endpoint = db_endpoint
        self.db_name = db_name

    def connect_db(self):
        """Connect to the default database

        Simply return a connection to the default database of this
        project.

        Returns:
             A connection object to the default database.
             Must be closed after usage.
        """
        return pymysql.connect(
            self.db_endpoint,
            self.db_user,
            self.db_passwd,
            self.db_name,
        )
