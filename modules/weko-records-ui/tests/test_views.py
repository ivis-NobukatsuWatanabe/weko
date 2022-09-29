from unittest.mock import MagicMock
import pytest
import io
from flask import Flask, json, jsonify, session, url_for
from flask_security.utils import login_user
from invenio_accounts.testutils import login_user_via_session
from mock import patch
from weko_deposit.api import WekoRecord
from werkzeug.exceptions import NotFound
from weko_workflow.models import (
    Action,
    ActionStatus,
    ActionStatusPolicy,
    Activity,
    FlowAction,
    FlowDefine,
    WorkFlow,
)
from weko_records_ui.views import (
    check_permission,
    citation,
    escape_newline,
    get_image_src,
    get_license_icon,
    json_string_escape,
    pid_value_version,
    publish,
    restore,
    check_file_permission,
    record_from_pid,
    default_view_method,
    url_to_link,
    xml_string_escape,
    escape_str,
    init_permission,
    file_version_update,
    set_pdfcoverpage_header,
    parent_view_method,
    doi_ish_view_method,
    check_file_permission_period,
    get_file_permission,
    check_content_file_clickable,
    get_usage_workflow,
    get_workflow_detail,
)

# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp

# def record_from_pid(pid_value):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_record_from_pid -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_record_from_pid(app, records):
    indexer, results = records
    recid = results[0]["recid"]
    ret = record_from_pid(recid.pid_value)
    assert isinstance(ret, WekoRecord)

    ret = record_from_pid(0)
    assert ret == {}


# def url_to_link(field):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_url_to_link -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_url_to_link():
    assert url_to_link("file://localhost") == False
    assert url_to_link("http://localhost") == True
    assert url_to_link("https://localhost") == True


# def pid_value_version(pid_value):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_pid_value_version -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_pid_value_version():
    assert pid_value_version(1.1) == "1"
    assert pid_value_version(1.0) == "0"
    assert pid_value_version(1) == None
    assert pid_value_version("1") == None
    assert pid_value_version("1.1") == "1"


# def publish(pid, record, template=None, **kwargs):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_publish_acl_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_publish_acl_guest(client, records):
    url = url_for("invenio_records_ui.recid_publish", pid_value=1, _external=True)
    res = client.post(url)
    assert res.status_code == 302
    assert res.location == "http://test_server/records/1"


# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_publish_acl -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, status_code",
    [
        (0, 302),
        # (1, 302),
        # (2, 302),
        # (3, 302),
        # (4, 302),
        # (5, 302),
        # (6, 302),
        # (7, 302),
    ],
)
def test_publish_acl(client, records, users, id, status_code):
    login_user_via_session(client=client, email=users[id]["email"])
    url = url_for("invenio_records_ui.recid_publish", pid_value=1, _external=True)
    res = client.post(url)
    assert res.status_code == status_code
    assert res.location == "http://test_server/records/1"


# def export(pid, record, template=None, **kwargs):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_export_acl_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_export_acl_guest(client, records):
    url = url_for(
        "invenio_records_ui.recid_export", pid_value=1, format="json", _external=True
    )
    res = client.post(url)
    assert res.status_code == 405

    res = client.get(url)
    assert res.status_code == 200

    url = url_for(
        "invenio_records_ui.recid_export", pid_value=1, format="bibtex", _external=True
    )
    res = client.get(url)
    assert res.status_code == 200

    url = url_for(
        "invenio_records_ui.recid_export", pid_value=1, format="oai_dc", _external=True
    )
    res = client.get(url)
    assert res.status_code == 200

    url = url_for(
        "invenio_records_ui.recid_export",
        pid_value=1,
        format="jpcoar_1.0",
        _external=True,
    )
    res = client.get(url)
    assert res.status_code == 200


# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_export_acl -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, status_code",
    [
        (0, 200),
        # (1, 302),
        # (2, 302),
        # (3, 302),
        # (4, 302),
        # (5, 302),
        # (6, 302),
        # (7, 302),
    ],
)
def test_export_acl(client, records, users, id, status_code):
    login_user_via_session(client=client, email=users[id]["email"])
    url = url_for(
        "invenio_records_ui.recid_export", pid_value=1, format="json", _external=True
    )
    res = client.post(url)
    assert res.status_code == 405

    url = url_for(
        "invenio_records_ui.recid_export", pid_value=1, format="bibtex", _external=True
    )
    res = client.get(url)
    assert res.status_code == status_code

    url = url_for(
        "invenio_records_ui.recid_export", pid_value=1, format="oai_dc", _external=True
    )
    res = client.get(url)
    assert res.status_code == status_code

    url = url_for(
        "invenio_records_ui.recid_export",
        pid_value=1,
        format="jpcoar_1.0",
        _external=True,
    )
    res = client.get(url)
    assert res.status_code == status_code


# def get_image_src(mimetype):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_get_image_src -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_get_image_src():
    assert get_image_src("text/plain") == "/static/images/icon/icon_16_txt.jpg"
    assert (
        get_image_src(
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        == "/static/images/icon/icon_16_ppt.jpg"
    )
    assert (
        get_image_src(
            "application/vnd.openxmlformats-officedocument.presentationml.slide"
        )
        == "/static/images/icon/icon_16_ppt.jpg"
    )
    assert (
        get_image_src(
            "application/vnd.openxmlformats-officedocument.presentationml.slideshow"
        )
        == "/static/images/icon/icon_16_ppt.jpg"
    )
    assert (
        get_image_src(
            "application/vnd.openxmlformats-officedocument.presentationml.template"
        )
        == "/static/images/icon/icon_16_ppt.jpg"
    )
    assert (
        get_image_src(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        == "/static/images/icon/icon_16_xls.jpg"
    )
    assert (
        get_image_src(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.template"
        )
        == "/static/images/icon/icon_16_xls.jpg"
    )
    assert (
        get_image_src(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        == "/static/images/icon/icon_16_doc.jpg"
    )
    assert (
        get_image_src(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.template"
        )
        == "/static/images/icon/icon_16_doc.jpg"
    )
    assert get_image_src("application/msword") == "/static/images/icon/icon_16_doc.jpg"
    assert (
        get_image_src("application/vnd.ms-excel")
        == "/static/images/icon/icon_16_xls.jpg"
    )
    assert (
        get_image_src("application/vnd.ms-powerpoint")
        == "/static/images/icon/icon_16_ppt.jpg"
    )
    assert get_image_src("application/zip") == "/static/images/icon/icon_16_zip.jpg"
    assert get_image_src("audio/mpeg") == "/static/images/icon/icon_16_music.jpg"
    assert get_image_src("application/xml") == "/static/images/icon/icon_16_xml.jpg"
    assert get_image_src("image/jpeg") == "/static/images/icon/icon_16_picture.jpg"
    assert get_image_src("application/pdf") == "/static/images/icon/icon_16_pdf.jpg"
    assert get_image_src("video/x-flv") == "/static/images/icon/icon_16_flash.jpg"
    assert get_image_src("video/mpeg") == "/static/images/icon/icon_16_movie.jpg"
    assert get_image_src("application/json") == "/static/images/icon/icon_16_others.jpg"


# def get_license_icon(license_type):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_get_license_icon -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_get_license_icon(app):
    with app.test_request_context(headers=[("Accept-Language", "ja")]):
        assert get_license_icon("license_12") == (
            "static/images/default88x31(0).png",
            "Creative Commons CC0 1.0 Universal Public Domain Designation",
            "https://creativecommons.org/publicdomain/zero/1.0/",
        )
        assert get_license_icon("license_free") == ("", "", "#")


#     # In case of current lang is not JA, set to default.
#     current_lang = 'default' if current_i18n.language != 'ja' \
# def check_permission(record):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_check_permission -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_check_permission(app, records, users):
    indexer, results = records
    record = results[0]["record"]

    assert check_permission(record) == False

    with patch("flask_login.utils._get_user", return_value=users[1]["obj"]):
        assert check_permission(record) == True

    with patch("flask_login.utils._get_user", return_value=users[0]["obj"]):
        assert check_permission(record) == False


# def check_file_permission(record, fjson):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_check_file_permission -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, result",
    [
        (0, True),
        (1, True),
        (2, True),
        (3, True),
        (4, True),
        (5, True),
        (6, True),
        (7, True),
    ],
)
def test_check_file_permission(app,records,users,id,result):
    indexer, results = records
    record = results[0]["record"]
    assert isinstance(record,WekoRecord)==True
    with patch("flask_login.utils._get_user", return_value=users[id]["obj"]):
        assert check_file_permission(record,record['item_1617605131499'])==result


# def check_file_permission_period(record, fjson):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_check_file_permission_period -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, result",
    [
        (0, True),
        # (1, True),
        # (2, True),
        # (3, True),
        # (4, True),
        # (5, True),
        # (6, True),
        # (7, True),
    ],
)
def test_check_file_permission_period(app,records,users,id,result):
    indexer, results = records
    record = results[0]["record"]
    assert isinstance(record,WekoRecord)==True
    with patch("flask_login.utils._get_user", return_value=users[id]["obj"]):
        assert check_file_permission_period(record,record['item_1617605131499'])==result

# def get_file_permission(record, fjson):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_get_file_permission -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, result",
    [
        (0, None),
        # (1, True),
        # (2, True),
        # (3, True),
        # (4, True),
        # (5, True),
        # (6, True),
        # (7, True),
    ],
)
def test_get_file_permission(app,records,users,id,result):
    indexer, results = records
    record = results[0]["record"]
    assert isinstance(record,WekoRecord)==True
    with patch("flask_login.utils._get_user", return_value=users[id]["obj"]):
        assert get_file_permission(record,record['item_1617605131499'])==result

# def check_content_file_clickable(record, fjson):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_check_content_file_clickable -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, result",
    [
        (0, False),
        # (1, True),
        # (2, True),
        # (3, True),
        # (4, True),
        # (5, True),
        # (6, True),
        # (7, True),
    ],
)
def test_check_content_file_clickable(app,records,users,id,result):
    indexer, results = records
    record = results[0]["record"]
    assert isinstance(record,WekoRecord)==True
    with patch("flask_login.utils._get_user", return_value=users[id]["obj"]):
        assert check_content_file_clickable(record,record['item_1617605131499'])==result

# def get_usage_workflow(file_json):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_get_usage_workflow -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_get_usage_workflow(app,workflows):
    assert False

# def get_workflow_detail(workflow_id):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_get_workflow_detail -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_get_workflow_detail(app,workflows):
    wf = workflows['workflow']
    ret = get_workflow_detail(wf.id)
    assert isinstance(wf,WorkFlow)

    with pytest.raises(NotFound):
        ret = get_workflow_detail(0)
    

# def default_view_method(pid, record, filename=None, template=None, **kwargs):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_default_view_method -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
#     """Display default view.
#     def _get_rights_title(result, rights_key, rights_values, current_lang, meta_options):
def test_default_view_method(app,records,itemtypes):
    indexer, results = records
    record = results[0]["record"]
    recid = results[0]["recid"]
    with app.test_request_context():
        assert default_view_method(recid,record)==""

# def doi_ish_view_method(parent_pid_value=0, version=0):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_doi_ish_view_method_acl_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_doi_ish_view_method_acl_guest(app,client,records):
    url = url_for("weko_records_ui.doi_ish_view_method", parent_pid_value=1, _external=True)
    res = client.get(url)
    assert res.status_code == 302
    assert res.location == 'http://test_server/login/?next=%2Fr%2F1'

# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_doi_ish_view_method_acl -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, result",
    [
        (0, False),
        # (1, True),
        # (2, True),
        # (3, True),
        # (4, True),
        # (5, True),
        # (6, True),
        # (7, True),
    ],
)
def test_doi_ish_view_method_acl(app,client,records,users,id,result):
    login_user_via_session(client=client, email=users[id]["email"])
    url = url_for("weko_records_ui.doi_ish_view_method", parent_pid_value=1, _external=True)
    res = client.get(url)
    assert res.status_code == 302
    assert res.location == 'http://test_server/records/1.1'

# def parent_view_method(pid_value=0):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_parent_view_method_acl_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_parent_view_method_acl_guest(app,client,records):
    url = url_for("weko_records_ui.parent_view_method", pid_value=1, _external=True)
    res = client.get(url)
    assert res.status_code == 302
    assert res.location == 'http://test_server/login/?next=%2Frecords%2Fparent%3A1'

# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_parent_view_method_acl -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, result",
    [
        (0, False),
        # (1, True),
        # (2, True),
        # (3, True),
        # (4, True),
        # (5, True),
        # (6, True),
        # (7, True),
    ],
)
def test_parent_view_method_acl(app,client,records,users,id,result):
    login_user_via_session(client=client, email=users[id]["email"])
    url = url_for("weko_records_ui.parent_view_method", pid_value=1, _external=True)
    res = client.get(url)
    assert res.status_code == 302
    assert res.location == 'http://test_server/records/1.1'


# def set_pdfcoverpage_header():
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_set_pdfcoverpage_header_acl_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_set_pdfcoverpage_header_acl_guest(app,client,records):
    url = url_for("weko_records_ui.set_pdfcoverpage_header",_external=True)
    res = client.get(url)
    assert res.status_code == 308
    assert res.location == 'http://test_server/admin/pdfcoverpage/'

    res = client.post(url)
    assert res.status_code == 302
    assert res.location == 'http://test_server/login/?next=%2Frecords%2Fparent%3A1'

# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_set_pdfcoverpage_header_acl -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, result",
    [
        (0, False),
        # (1, True),
        # (2, True),
        # (3, True),
        # (4, True),
        # (5, True),
        # (6, True),
        # (7, True),
    ],
)
def test_set_pdfcoverpage_header_acl(app,client,records,users,id,result):
    login_user_via_session(client=client, email=users[id]["email"])
    url = url_for("weko_records_ui.set_pdfcoverpage_header",_external=True)
    res = client.get(url)
    assert res.status_code == 308
    assert res.location == 'http://test_server/admin/pdfcoverpage/'

    data = {'availability':'enable', 'header-display':'string', 'header-output-string':'Weko Univ', 'header-display-position':'center', 'pdfcoverpage_form': '',
    'header-output-image': (io.BytesIO(b"some initial text data"), 'test.png')}
    res = client.post(url,data=data)
    assert res.status_code == 302
    assert res.location == 'http://test_server/login/?next=%2Frecords%2Fparent%3A1'

    data = {'availability':'enable', 'header-display':'image', 'header-output-string':'Weko Univ', 'header-display-position':'center', 'pdfcoverpage_form': '',
    'header-output-image': (io.BytesIO(b"some initial text data"), 'test.png')}
    res = client.post(url,data=data)
    assert res.status_code == 302
    assert res.location == 'http://test_server/login/?next=%2Frecords%2Fparent%3A1'

#     def handle_over_max_file_size(error):
# def file_version_update():
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_file_version_update_acl_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_file_version_update_acl_guest(client, records):
    url = url_for("weko_records_ui.file_version_update",_external=True)
    res = client.put(url)
    assert res.status_code == 302
    assert res.location == 'http://test_server/login/?next=%2Ffile_version%2Fupdate'

# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_file_version_update_acl -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, status_code",
    [
        (0, 200),
        # (1, 302),
        # (2, 302),
        # (3, 302),
        # (4, 302),
        # (5, 302),
        # (6, 302),
        # (7, 302),
    ],
)
def test_file_version_update_acl(client, records, users, id, status_code):
    login_user_via_session(client=client, email=users[id]["email"])
    url = url_for("weko_records_ui.file_version_update",_external=True)
    res = client.put(url)
    assert res.status_code == 302
    assert res.location == 'http://test_server/login/?next=%2Ffile_version%2Fupdate'


# def citation(record, pid, style=None, ln=None):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_citation -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_citation(records):
    indexer, results = records
    record = results[0]["record"]
    assert citation(record,record.pid)==""

# def soft_delete(recid):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_soft_delete_acl_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_soft_delete_acl_guest(client, records):
    url = url_for(
        "weko_records_ui.soft_delete", recid=1, _external=True
    )
    res = client.post(url)
    assert res.status_code == 302

# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_soft_delete_acl -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, status_code",
    [
        (0, 200),
        # (1, 302),
        # (2, 302),
        # (3, 302),
        # (4, 302),
        # (5, 302),
        # (6, 302),
        # (7, 302),
    ],
)
def test_soft_delete_acl(client, records, users, id, status_code):
    login_user_via_session(client=client, email=users[id]["email"])
    url = url_for(
        "weko_records_ui.soft_delete", recid=1, _external=True
    )
    res = client.post(url)
    assert res.status_code == status_code

# def restore(recid):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_restore_acl_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_restore_acl_guest(client, records):
    url = url_for(
        "weko_records_ui.restore", recid=1, _external=True
    )
    res = client.post(url)
    assert res.status_code == 302

# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_restore_acl -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, status_code",
    [
        (0, 200),
        # (1, 302),
        # (2, 302),
        # (3, 302),
        # (4, 302),
        # (5, 302),
        # (6, 302),
        # (7, 302),
    ],
)
def test_restore_acl(client, records, users, id, status_code):
    login_user_via_session(client=client, email=users[id]["email"])
    url = url_for(
        "weko_records_ui.restore", recid=1, _external=True
    )
    res = client.post(url)
    assert res.status_code == status_code

# def init_permission(recid):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_init_permission_acl_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_init_permission_acl_guest(client, records):
    url = url_for(
        "weko_records_ui.init_permission", recid=1, _external=True
    )
    res = client.post(url)
    assert res.status_code == 302

# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_init_permission_acl -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.parametrize(
    "id, status_code",
    [
        (0, 200),
        # (1, 302),
        # (2, 302),
        # (3, 302),
        # (4, 302),
        # (5, 302),
        # (6, 302),
        # (7, 302),
    ],
)
def test_init_permission_acl(client, records, users, id, status_code):
    login_user_via_session(client=client, email=users[id]["email"])
    url = url_for(
        "weko_records_ui.init_permission", recid=1, _external=True
    )
    res = client.post(url)
    assert res.status_code == status_code


# def escape_str(s):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_escape_str -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_escape_str():
    assert escape_str("\n")==""


# def escape_newline(s):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_escape_newline -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_escape_newline():
    assert escape_newline("\r") == '<br/>'
    assert escape_newline("\r\n") == '<br/>'
    assert escape_newline("\n") == '<br/>'
    assert escape_newline("\r\r\n\n") == '<br/><br/><br/>'

# def json_string_escape(s):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_json_string_escape -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp

def test_json_string_escape():
    assert json_string_escape("\x5c") == "\\\\"
    assert json_string_escape("\x08") == "\\b"
    assert json_string_escape("\x0a") == "\\n"
    assert json_string_escape("\x0d") == "\\r"
    assert json_string_escape("\x09") == "\\t"
    assert json_string_escape("\x0c") == "\\f"


# def xml_string_escape(s):
def test_xml_string_escape():
    assert xml_string_escape("&<>") == "&amp;&lt;&gt;"


# def preview_able(file_json):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_views.py::test_url_to_link -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
