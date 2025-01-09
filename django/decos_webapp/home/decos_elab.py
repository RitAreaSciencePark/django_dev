from decos_elabftw_API.decos_elabftw_API import ElabFTWAPI
from django.template.loader import render_to_string
from PRP_CDM_app.models import LageSamples
from django.forms.models import model_to_dict

class Decos_Elab_API(ElabFTWAPI):

    def _new_LAGE_experiment(self, experiment_info, username):
        dict_to_render = model_to_dict(experiment_info)
        title = f"{dict_to_render["sample_id"]}: {dict_to_render["sample_short_description"]}"
        dict_to_send = {
            "title" : title,
            # "date": "2024-10-29", # TODO: Implement date time!!!
            # "username" : username,
            "body": render_to_string("home/elabFTW/experiment_template.html", dict_to_render),
        }
        self.create_experiment(dict_to_send)

    def create_new_decos_experiment(self, lab, username, experiment_info):
        match lab.lab_id:
            case 'LAGE':
                self._new_LAGE_experiment(experiment_info, username)
            case _:
                raise Exception('No laboratory elab template found')
            

        '''"title": request.POST.get("sr_id_hidden"),
        "body": render_to_string("home/elabFTW/experiment_template.html", { 
            "username" : username,
            "sample_id" : data.sample_id,
            })
        

        self.create_experiment(experiment_info)'''
