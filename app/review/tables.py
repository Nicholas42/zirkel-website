from random import choices

from flask_table import Table, Col, LinkCol, DatetimeCol, DateCol, BoolCol, ButtonCol


def transform_sub(sub):
    ret = sub.__dict__.copy()
    ret["author"] = sub.author.username
    ret["admin"] = sub.author.is_admin()
    if sub.reviewer:
        ret["reviewer"] = sub.reviewer.username

    return ret


class _EmptyCol(Col):
    def td_contents(self, item, attr_list):
        return ""


class _BaseTable(Table):
    allow_empty = True
    classes = ["fullwidth"]
    author = LinkCol("Name", "review.show_user", url_kwargs={"uid": "author_id"}, attr_list=["author"], th_html_attrs={"style": "width:20em"})
    upload_time = DatetimeCol("Hochgeladen", datetime_format="dd.MM.YYYY, HH:mm", th_html_attrs={"style": "width:10em"})
    url = LinkCol("Datei", "upload.serve_submission", url_kwargs={"filename": "filename"}, text_fallback="Url",
                  th_html_attrs={"style": "width:8em"})
    delete = LinkCol("Löschen", "admin.delete_submission", url_kwargs={"sub_id": "id"}, show="admin")

    def __init__(self, *args, **kwargs):
        super(_BaseTable, self).__init__(*args, **kwargs)
        self.items = list(map(transform_sub, self.items))
        if "delete" in self._cols:
            self._cols.move_to_end("delete")


class ActiveTable(_BaseTable):
    t = _EmptyCol("", "", th_html_attrs={"style": "width:20em"})
    claim = LinkCol("Korrektur", "review.claim_submission", url_kwargs={"sub_id": "id"}, text_fallback="beanspruchen",
                    th_html_attrs={"style": "width:8em"})


class UnderReviewTable(_BaseTable):
    reviewer = Col("Korrektor", th_html_attrs={"style": "width:20em"})
    claim = LinkCol("Korrektur", "review.review", url_kwargs={"sub_id": "id"}, text_fallback="hinzufügen",
                    th_html_attrs={"style": "width:8em"})


class ClosedTable(_BaseTable):
    reviewer = Col("Korrektor", th_html_attrs={"style": "width:20em"})
    review = LinkCol("Korrektur", "upload.serve_review", url_kwargs={"filename": "review.filename"}, text_fallback="Url",
                     th_html_attrs={"style": "width:8em"})


class UserListTable(Table):
    classes = ["fullwidth"]
    username = LinkCol("Name", "review.show_user", url_kwargs={"uid": "id"}, attr_list=["username"])
    next_module = DateCol("Nächste Bearbeitung", date_format="medium")
    next_sub = DateCol("Nächste Abgabe", date_format="medium")
    currently_working = BoolCol("Beschäftigt", yes_display="ja", no_display="nein")
    set_working = ButtonCol("Beschäftigen", endpoint="review.occupy", url_kwargs={"user_id": "id"},
                            text_fallback="Ändern")

