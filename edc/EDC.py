import requests

class EDC:
    connString = "https://hsmserver.herokuapp.com"
    #connString = "http://localhost:8080"
    schemaname = "MTUCI-EDC"
    password = "PASWWORD"

    def signFile(self, file, username):
        url = self.connString + "/signFile"
        files = {'file': file}

        return requests.post(
            url, 
            files=files, 
            data={  'schemaname': self.schemaname, 
                    'password': self.password, 
                    'username': username}
        ).text

# edc = EDC()
# file = open("edc/test.txt", "r")
# print(edc.signFile(file, 'Emil'))
