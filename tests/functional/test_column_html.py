import django_tables2 as tables
import pytest
from bs4 import BeautifulSoup

from django_crispy_tableselect.columns import CheckBoxColumn


class MyTable(tables.Table):
    pass


class MockHelper:
    allow_select_all = True

    def get_accessible_label(self, *args, **kwargs):
        return "mock_label"

    def get_select_all_checkbox_attrs(self, *args, **kwargs):
        return {}


@pytest.mark.parametrize("allow_select_all", (True, False))
def test_render_column_header_allow_select_all(allow_select_all):
    """Check that the column header renders a select-all checkbox when needed."""

    helper = MockHelper()
    helper.allow_select_all = allow_select_all

    table = MyTable(
        data=[],
        extra_columns=[
            (
                "foo",
                CheckBoxColumn(
                    verbose_name="",
                    input_name="test_input_name",
                    helper=helper,
                    selected_values=[],
                ),
            )
        ],
    )

    soup = BeautifulSoup(table.columns["foo"].header, "html.parser")

    if allow_select_all:
        assert soup.select('input[type="checkbox"]')
    else:
        assert not soup.select('input[type="checkbox"]')


@pytest.mark.parametrize("allow_select_all", (True, False))
def test_render_column_header_always_has_narrator_element(allow_select_all):
    """Check that the column header renders always renders an invisible element used by the frontend for accessibility purposes."""

    helper = MockHelper()
    helper.allow_select_all = allow_select_all

    table = MyTable(
        data=[],
        extra_columns=[
            (
                "foo",
                CheckBoxColumn(
                    verbose_name="",
                    input_name="test_input_name",
                    helper=helper,
                    selected_values=[],
                ),
            )
        ],
    )

    soup = BeautifulSoup(table.columns["foo"].header, "html.parser")

    assert soup.select("[data-tableselect-narrator]")
