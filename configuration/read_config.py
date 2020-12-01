from configparser import ConfigParser

def retrieve_variable(variable):

    config_object = ConfigParser()
    config_object.read("configuration/clinic.conf")

    userinfo = config_object["user_info"]
    
    return userinfo[variable]


# print(retrieve_variable('username'))