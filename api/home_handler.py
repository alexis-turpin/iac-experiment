import requests
import initialization_handler


class Home(initialization_handler.InitializationHandler):

    def get(self):
        # TODO : Add a connection to the API LB
        try:
            url = "http://169.254.169.254/latest/meta-data/local-ipv4"
            local_ip = requests.get(url).text
        except Exception as e:
            local_ip = "Not AWS hosted" + str(e)
        self.write({"api-ip": local_ip})
