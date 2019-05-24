from flask_table import Table, LinkCol, Col, OptCol


def get_status(sub):
    if sub.is_open() and not sub.is_claimed():
        return "open"
    elif sub.is_open() and sub.is_claimed():
        return "claimed"
    else:
        return "closed"


class SubTable(Table):
    classes = ["fullwidth"]
    details = LinkCol("Details", "upload.submission", url_kwargs={"index": "id"})
    status = OptCol("Status", choices={"open": "offen", "under review": "wird korrigiert", "closed": "korrigiert"})
    points = Col("Punkte")

    def __init__(self, *args, **kwargs):
        super(SubTable, self).__init__(*args, **kwargs)

        for i in self.items:
            i.status = get_status(i)
            if i.points is None:
                i.points = 0
