from flask_table import Table, LinkCol, Col, OptCol

from app.helpers.table_helpers import IdentityDict


class SubTable(Table):
    classes = ["fullwidth"]
    details = LinkCol("Details", "upload.submission", url_kwargs={"index": "id"}, text_fallback="Url")
    status = OptCol("Status", choices=IdentityDict())
    points = Col("Punkte", attr="review.points")

    def __init__(self, *args, **kwargs):
        super(SubTable, self).__init__(*args, **kwargs)

        for i in self.items:
            if i.review and i.review.points is None:
                i.review.points = 0.0
