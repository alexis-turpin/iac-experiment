import tornado.web


class InitializationHandler(tornado.web.RequestHandler):
    """
    """
    # TODO pydoc

    def initialize(
            self,
            front_ip,
            back_ip,
            infra,
    ):
        """
        """
        # TODO pydoc
        self.front_ip = front_ip
        self.back_ip = back_ip
        self.infra = infra
