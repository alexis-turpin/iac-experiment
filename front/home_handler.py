import requests
import initialization_handler


class Home(initialization_handler.InitializationHandler):
    """
    """
    # TODO pydoc
    def get(self):
        """
        """
        # TODO pydoc
        try:
            url = "http://169.254.169.254/latest/meta-data/local-ipv4"
            local_ip = requests.get(url).text
        except Exception:
            local_ip = "Not AWS hosted"

        try:
            url = "http://" + self.back_ip
            api_ip = requests.get(url).json()["api-ip"]
        except Exception:
            api_ip = "No API IP"
        print("render with", self.front_ip)
        self.render(
            "templates/home.html",
            local_ip=local_ip,
            api_ip=api_ip,
            front_ip=self.front_ip,
            infra=self.infra,
        )
