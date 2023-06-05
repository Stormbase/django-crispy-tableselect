import django_tables2 as tables
import pytest
from django.contrib.staticfiles.finders import find
from django.core import exceptions

from django_crispy_tableselect import TableSelectHelper
from django_crispy_tableselect.columns import CheckBoxColumn
from tests.testapp.models import Book
from tests.testapp.tables import BookTable

BOOKS_DICT = [
    {"title": "Sans Famille", "id": 123, "author": "Hector Malot"},
    {"title": "How to Become King", "id": 456, "author": "Jan Terlouw"},
]


def test_select_all_defaults_to_false():
    """Check that - when not specified -the ``allow_select_all`` option defaults to False."""
    helper = TableSelectHelper(
        "foo", table_class=BookTable, table_data=[], label_field="foo"
    )
    assert not helper.allow_select_all


def test_accessible_label__dictionary(books_tableselect):
    """Check that the default implementation of get_accessible_label includes the value of ``label_field``."""
    helper = books_tableselect(table_data=BOOKS_DICT, label_field="title")

    assert BOOKS_DICT[0]["title"] in helper.get_accessible_label(BOOKS_DICT[0])
    assert BOOKS_DICT[1]["title"] in helper.get_accessible_label(BOOKS_DICT[1])


@pytest.mark.django_db
def test_accessible_label__queryset(books_tableselect, book_factory):
    """Check that the default implementation of get_accessible_label includes the value of ."""
    book = book_factory(title="The Witches by Roahl Dahl")
    qs = Book.objects.all()

    helper = books_tableselect(table_data=qs)
    assert str(book) in helper.get_accessible_label(book)


def test_table_class_derived_from_table():
    """Check that an exception is raised when the given table class is not actually a table."""

    class NotDerivedFromTableClass:
        pass

    class DerivedFromTableClass(tables.Table):
        pass

    with pytest.raises(exceptions.ImproperlyConfigured):
        TableSelectHelper(
            "foo",
            table_class=NotDerivedFromTableClass,
            table_data=[],
            label_field="foo",
        )

    TableSelectHelper(
        "foo", table_class=DerivedFromTableClass, table_data=[], label_field="foo"
    )


def test_media():
    """Check that the media attribute is present on the helper and that it contains a valid reference to a javascript file."""
    helper = TableSelectHelper(
        "foo", table_class=BookTable, table_data=[], label_field="foo"
    )
    assert helper.media
    assert helper.media._js

    # Check that Django's staticfiles app can find the javascript file
    assert find(helper.media._js[0])


@pytest.mark.django_db
def test_checkbox_column(books_tableselect):
    """Check that the checkbox column is added and added at the start of the table."""
    helper = books_tableselect()

    table = helper.get_table("foo", [])
    # Checkbox column is present
    assert "selected_books" in table.columns
    bound_column = table.columns["selected_books"]
    assert isinstance(bound_column.column, CheckBoxColumn)
    # Checkbox column is first column in sequence
    assert table.sequence[0] == "selected_books"


@pytest.mark.django_db
def test_choices__queryset(books_tableselect):
    """Check that the helper generates the expected choices tuple in the right order when given a QuerySet."""
    helper = books_tableselect()

    assert len(helper.choices) == len(
        helper.table_data
    ), "No all table data presented as choices"

    choices = helper.choices

    # The choices should follow the same ordering as the table data. Hence index-based iteration.
    for idx, book in enumerate(helper.table_data):
        assert choices[idx][0] == book.pk
        assert choices[idx][1] == book.title


def test_choices__dictionaries(books_tableselect):
    """Check that the helper generates the expected choices tuple in the right order when given a dictionary."""
    helper = books_tableselect(table_data=BOOKS_DICT)

    assert len(helper.choices) == len(
        helper.table_data
    ), "No all table data presented as choices"

    choices = helper.choices

    # The choices should follow the same ordering as the table data. Hence index-based iteration.
    for idx, book in enumerate(helper.table_data):
        assert choices[idx][0] == book["id"]
        assert choices[idx][1] == book["title"]


def test_get_table_extra_columns_respected(books_tableselect):
    """Check that the get_table method respects the extra_columns argument."""
    helper = books_tableselect(
        table_data=BOOKS_DICT,
        table_kwargs={"extra_columns": [("date_created", tables.DateColumn())]},
    )
    table = helper.get_table(input_name="foo", selected_values=[])

    assert "date_created" in table.columns
    # It is an extra column, not a base one
    assert "date_created" not in table.base_columns


def test_get_table_kwarg_attrs_respected(books_tableselect):
    """Check that the get_table method respects the ``attrs`` key passed to table_kwargs."""
    helper = books_tableselect(
        table_data=BOOKS_DICT,
        table_kwargs={"attrs": {"needle": ""}},
    )
    table = helper.get_table(input_name="foo", selected_values=[])

    assert "needle" in table.attrs


def test_get_table_meta_attrs_respected(books_tableselect):
    """Check that the get_table method respects the attrs Meta attribute."""

    class BookTableWithAttrs(BookTable):
        class Meta:
            attrs = {"needle": ""}

    helper = books_tableselect(
        table_class=BookTableWithAttrs,
        table_data=BOOKS_DICT,
    )
    table = helper.get_table(input_name="foo", selected_values=[])

    assert "needle" in table.attrs


def test_get_table__no_rows_selected(books_tableselect):
    """Check that the get_table method returns a table with no checkboxes selected by default."""
    helper = books_tableselect(table_data=BOOKS_DICT)

    table = helper.get_table(input_name="foo", selected_values=[])

    for idx in range(len(helper.table_data)):
        # Get the html for the cell
        cell_html = table.rows[idx].get_cell("selected_books")
        # Should NOT contain checked attribute
        assert "checked" not in cell_html


def test_get_table__single_row_checked(books_tableselect):
    """Check that the get_table method returns a table with the right rows checked when ``selected_values`` is set."""
    helper = books_tableselect(table_data=BOOKS_DICT)

    # Select the first row
    selected_values = [str(BOOKS_DICT[0]["id"])]
    table = helper.get_table(input_name="foo", selected_values=selected_values)

    cell_html = table.rows[0].get_cell("selected_books")
    # This is the first row and it should be checked.
    # Its value is present in selected_values argument.
    assert "checked" in cell_html

    cell_html = table.rows[1].get_cell("selected_books")
    # This is the second row and it should NOT be checked.
    # Its value is NOT present in selected_values argument.
    assert "checked" not in cell_html


def test_table_class_meta_sequence_respected():
    """Check that the table class' Meta.sequence property is respected."""

    class SequencedBookTable(BookTable):
        class Meta:
            sequence = ("author", "...")

    expected_sequence = ("selected_books", "author", "...")
    helper = TableSelectHelper(
        column_name="selected_books",
        table_class=SequencedBookTable,
        table_data=[],
        label_field="title",
    )

    assert expected_sequence == helper._construct_sequence()


def test_table_class_kwarg_sequence_respected():
    """Check that the table class' Meta.sequence property is respected."""
    expected_sequence = ("selected_books", "author", "...")
    helper = TableSelectHelper(
        column_name="selected_books",
        table_class=BookTable,
        table_data=[],
        label_field="title",
        table_kwargs={"sequence": ("author", "...")},
    )

    assert expected_sequence == helper._construct_sequence()


@pytest.mark.parametrize(
    "selected_values,expect_checked", [([], False), (["1"], False), (["1", "2"], True)]
)
def test_table_select_all_checkbox_attrs(
    books_tableselect, selected_values, expect_checked
):
    """Check that the select_all_checkbox_attrs method only returns 'checked' when all rows are selected."""

    data = [{"id": 1, "title": "ABC"}, {"id": 2, "title": "DEF"}]
    helper = books_tableselect(table_data=data, allow_select_all=False)
    # Never return attributes when allow_select_all is False
    helper.get_select_all_checkbox_attrs(selected_values) == {}

    helper = books_tableselect(table_data=data, allow_select_all=True)
    attrs = helper.get_select_all_checkbox_attrs(selected_values)

    # Checked attribute should only be present when we expect it
    assert expect_checked == bool("checked" in attrs)
