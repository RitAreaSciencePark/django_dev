from PRP_CDM_app.models import *

class FormsDefinition:

    class LageForm:
        lab = 'LAGE'
        content = [
            Administration,
            lageSample,
        ]

    class LameForm:
        lab = 'LAME'
        content = [
            Administration,
        ]
