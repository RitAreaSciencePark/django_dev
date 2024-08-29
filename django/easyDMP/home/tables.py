from django_tables2 import tables, Column

from PRP_CDM_app.models import Proposals,ServiceRequests,Samples

class ProposalsTable(tables.Table):
    proposal_id = Column(empty_values=(),attrs={"th": {"id": "foo"}},verbose_name="id of the proposal")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render_proposal_id(self, record):
        return f"uuid: {record.proposal_id}"

    def render_id(self, value):
        return f"<{value}>"

    class Meta:
        model = Proposals
        template_name = "django_tables2/bootstrap.html"
        fields = ("proposal_date","proposal_filename","proposal_id", "proposal_status", "proposal_feasibility" )
        row_attrs = {
        "onClick": lambda record: f"document.getElementById('proposalIdBox').value = '{record.proposal_id}';"
        }
        orderable = True

class ServiceRequestTable(tables.Table):
    class Meta:
        model = ServiceRequests
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("sr_id","proposal_id","lab_id","sr_status","output_delivery_date")
        row_attrs = {
        "onClick": lambda record: f"document.location.href='/sample-entry-information/?sr_id={record.sr_id}';"
        }

class SamplesTable(tables.Table):
    class Meta:
        model = Samples
        template_name = "django_tables2/bootstrap.html"
        fields = ("sample_id","sr_id","sample_feasibility","sample_status")