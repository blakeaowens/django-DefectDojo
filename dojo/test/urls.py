from django.urls import re_path

from dojo.test import views

urlpatterns = [
    #  tests
    re_path(r"^calendar/tests$", views.test_calendar, name="test_calendar"),
    re_path(
        r"^test/(?P<test_id>\d+)$",
        views.ViewTest.as_view(),
        name="view_test",
    ),
    re_path(r"^test/(?P<tid>\d+)/ics$", views.test_ics,
        name="test_ics"),
    re_path(r"^test/(?P<tid>\d+)/edit$", views.edit_test,
        name="edit_test"),
    re_path(r"^test/(?P<tid>\d+)/delete$", views.delete_test,
        name="delete_test"),
    re_path(r"^test/(?P<tid>\d+)/copy$", views.copy_test,
        name="copy_test"),
    re_path(
        r"^test/(?P<test_id>\d+)/add_findings$",
        views.AddFindingView.as_view(),
        name="add_findings"),
    re_path(r"^test/(?P<tid>\d+)/add_findings/(?P<fid>\d+)$",
        views.add_temp_finding, name="add_temp_finding"),
    re_path(r"^test/(?P<tid>\d+)/search$", views.search, name="search"),
    re_path(
        r"^test/(?P<test_id>\d+)/re_import_scan_results",
        views.ReImportScanResultsView.as_view(),
        name="re_import_scan_results"),
]
