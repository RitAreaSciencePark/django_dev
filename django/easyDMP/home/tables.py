from django_tables2 import tables, Column

from PRP_CDM_app.models import Proposals

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
        orderable = True
