from configparser import ConfigParser

config_object = ConfigParser()
config_object.read(".clinic_config/clinic.conf")


#Get the password
userinfo = config_object["user_info"]
print(format(userinfo["campus"]))