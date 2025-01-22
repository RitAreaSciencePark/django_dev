from APIs.decos_elabftw_API.decos_elabftw_API import ElabFTWAPI
from django.template.loader import render_to_string
from PRP_CDM_app.models import LageSamples
from django.forms.models import model_to_dict
from APIs.decos_jenkins_API.decos_jenkins_API import Server
from PRP_CDM_app.models import API_Tokens
import re

class Decos_Jenkins_API(Server):
    
    def __init__(self, username, lab):
        user_id = username, 
        laboratory_id = lab
        jenkins_token = API_Tokens.objects.filter(user_id=username, laboratory_id = lab.lab_id).values("jenkins_token").first()['jenkins_token']
        credentials = (username, jenkins_token)
        # 'http://localhost:9000/' or jenkins-test
        # TODO: SOFTCODE HOST:
        host = 'http://jenkins-test:8080/'
        super().__init__(host, credentials)

'''
    def get_sample_list(self,path_info):
        raw_output = self.get_console_info(path_info)
        pattern = r"s_\w+"
        full_name_list = re.findall(pattern,raw_output)
        sample_id_list = []
        pattern = r"s(\_[a-zA-Z0-9]+){2}"
        for sample_full_name in full_name_list:
            sample_id_s = re.search(pattern, sample_full_name)
            if sample_id_s:
                sample_id = sample_id_s.group()
                sample_id_list.append((sample_id, sample_full_name))

        return sample_id_list


    host = secrets.host
    credentials = (secrets.id, secrets.token)
    server = Server(host, credentials)
    folder_list = server.get_job_folders()
    print(server.get_jobs(folder_list[0])[0]['name'])
    print(f"{folder_list[0]}/job/{server.get_jobs(folder_list[0])[0]['name']}")
    path_info = f"{folder_list[0]}/job/{server.get_jobs(folder_list[0])[0]['name']}"
    build_list = server.get_builds(path_info)
    for build in build_list:
        print(f"{build['fullDisplayName']} - result: {build['result']}")
    print(server.get_latest_build(path_info,server.LAST_SUCCESSFUL_BUILD))
    print(...)
    print(server.get_console_info(path_info))
    print(server.build_job(path_info, secrets.secret_token_folder_list))'''