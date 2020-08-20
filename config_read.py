import configparser

class config_data():
    def read_config(self,url):
        config = configparser.ConfigParser()
        config.read(url) 
        url = config['xnat']['url']
        username = config['xnat']['username']
        password = config['xnat']['password']
        return url,username,password
