import initialization_handler
import requests
import tornado.web

class AllBananas(initialization_handler.InitializationHandler):
    """
    """
    # TODO pydoc
    def get(self):
        """
        """
        # TODO pydoc
        try:
            url = "http://{}/banana".format(self.back_ip)
            answer = requests.get(url).json()
            if "error" in answer:
                raise tornado.web.HTTPError(500)
        except tornado.web.HTTPError:
            self.render(
                "templates/error.html",
                error_code=answer["error"],
                error_msg=answer["errorCode"],
                front_ip=self.front_ip,
                infra=self.infra,
            )
        except Exception as e:
            self.render(
                "templates/error.html",
                error_code="with backend query: " + str(e),
                error_msg="500",
                front_ip=self.front_ip,
                infra=self.infra,
            )
        else:
            self.render(
                "templates/bananas.html",
                bananas=answer,
                front_ip=self.front_ip,
                infra=self.infra,
            )

    def post(self):
        """
        """
        # TODO pydoc
        data = {
            "color": self.get_argument('color', None),
            "size": self.get_argument('size', None),
            "price": self.get_argument('price', None),
        }
        try:
            url = "http://{}/banana".format(self.back_ip)
            answer = requests.post(url, data=data).json()
            if "error" in answer:
                raise tornado.web.HTTPError(500)
        except tornado.web.HTTPError:
            self.render(
                "templates/error.html",
                error_code=answer["error"],
                error_msg=answer["errorCode"],
                front_ip=self.front_ip,
                infra=self.infra,
            )
        except Exception as e:
            self.render(
                "templates/error.html",
                error_code="Error with backend query: " + str(e),
                error_msg="500",
                front_ip=self.front_ip,
                infra=self.infra,
            )
        else:
            self.redirect("/banana/" + str(answer["last_row_id"]))


