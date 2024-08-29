from PRP_CDM_app.models import *

class ReportDefinition:

    class LageReport:
        lab = 'LAGE'
        content = [
            Administration,
            LageSamples,
        ]