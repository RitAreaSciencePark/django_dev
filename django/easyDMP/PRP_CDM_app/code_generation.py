from uuid import uuid4

from PRP_CDM_app.models import Proposals, ServiceRequests, Samples

from datetime import datetime
import re

def affiliationShortnener(affiliation):
    out = re.sub("(?<=\w{4})(\w+)","", affiliation)
    out = re.sub("(\s+)", "", out)
    return out

def proposal_id_generation(affiliation):
    try:
        # Get the latest proposal_id
        last_proposal = Proposals.objects.latest('proposal_id')
        last_proposal_id = last_proposal.proposal_id
    except Proposals.DoesNotExist:
        last_proposal_id = None

    if last_proposal_id:
        new_progressive = int(last_proposal_id.split('_')[-1]) + 1
    else:
        new_progressive = 1
    
    new_proposal_id = f"p_{datetime.now().year}_{affiliationShortnener(affiliation)}_{new_progressive:05d}"

    return new_proposal_id



def sr_id_generation(proposal, lab):
    proposal_id = proposal.proposal_id
    lab_id = lab.lab_id
    try:
        # Get the latest sr_id
        last_sr = ServiceRequests.objects.latest('sr_id')
        last_sr_id = last_sr.sr_id
    except ServiceRequests.DoesNotExist:
        last_sr_id = None

    if last_sr_id:
        new_progressive = int(last_sr_id.split('_')[-1]) + 1
    else:
        new_progressive = 1
    
    new_sr_id = f"sr_{proposal_id[2:]}_{lab_id}_{new_progressive:05d}"

    return new_sr_id




def sample_id_generation(sr_id):
    try:
        # Get the latest sr_id
        last_sample = Samples.objects.latest('sample_id')
        last_sample_id = last_sample.sample_id
    except Samples.DoesNotExist:
        last_sample_id = None
    
    if last_sample_id:
        new_progressive = int(last_sample_id.split('_')[-1]) + 1
    else:
        new_progressive = 1
    
       
    if(sr_id is not None):
        new_sample_id = f"s_{sr_id[3:]}_{new_progressive:05d}"
    else:
        new_sample_id = f"s_internal_{new_progressive:05d}"


    return new_sample_id


# TO DO: step_id_generation: s_year_{sample_id[22:]}_intrument_technique_progr