import json
import os
if __name__ == '__main__':
    dict_infos = json.load(open('freedict-database.json', encoding='utf-8'))
    for dict_info in dict_infos:
        print(dict_info)
        dict_name = dict_info["name"]
        for release in dict_info["releases"]:
            if release["platform"] == "src":
                if not os.path.isfile("zipfold/{}".format(dict_name)):
                        os.system("curl {} --output zipfold/{}".format(release["URL"], dict_name))
                if not os.path.isfile("Data/{}".format(dict_name)):
                    os.system("tar -xf zipfold/{0} -C Data/".format(dict_name))

