import requests

class EDC:
    connString = "http://localhost:8080"
    username = "MTUCI-EDC"
    password = "PASWWORD"

    def signFile(self, file, username):
        url = self.connString + "/signFile"
        files = {'file': file}

        return requests.post(
            url, 
            files=files, 
            data={'username': self.username, 'password': self.password}
        ).text

edc = EDC()
file = open("test.txt", "r")
print(edc.signFile(file, 'Misha'))
