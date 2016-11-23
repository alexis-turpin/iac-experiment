import tornado.web
import requests


class Home(tornado.web.RequestHandler):
    def get(self):
        # TODO : Add a connection to the API LB
        try:
            local_ip = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4").text
        except Exception as e:
            local_ip = "Not AWS hosted" + str(e)
        self.write({"api-ip": local_ip})
