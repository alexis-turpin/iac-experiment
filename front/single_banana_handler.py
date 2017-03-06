import initialization_handler
import requests
import tornado.web


class SingleBanana(initialization_handler.InitializationHandler):
    """
    """
    # TODO pydoc
    def get(
            self,
            banana_id=None
    ):
        """
        """
        # TODO pydoc
        try:
            url = "http://{}/banana/{}".format(self.back_ip, int(banana_id))
            answer = requests.get(url).json()
            if "error" in answer:
                raise tornado.web.HTTPError(500)
        except tornado.web.HTTPError:
            self.render(
                "templates/error.html",
                error_code=answer["error"],
                error_msg=api_ip["errorCode"],
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
            self.render(
                "templates/single_banana.html",
                banana_id=answer["id"],
                color=answer["color"],
                size=answer["size"],
                price=answer["price"],
                front_ip=self.front_ip,
                infra=self.infra,
            )

    def delete(
            self,
            banana_id=None
    ):
        """
        """
        # TODO pydoc
        try:
            url = "http://{}/banana/{}".format(self.back_ip, int(banana_id))
            answer = requests.delete(url).json()
            if "error" in answer:
                raise tornado.web.HTTPError(500)
        except tornado.web.HTTPError:
            self.render(
                "templates/error.html",
                error_code=answer["error"],
                error_msg=api_ip["errorCode"],
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
            self.redirect("/banana/")
