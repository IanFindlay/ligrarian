#!/usr/bin/env python3

import pytest
import unittest.mock as mock

import ligrarian


class FakeCell:
    """A fake version of openpyxl's workbook.sheet.cell."""

    def __init__(self, row, column):
        """Use row to simulate different values in different cells."""
        if row == 3:
            self.value = ''
        else:
            self.value = 'not blank'


def test_first_blank_row():
    """Return row where cell.value is an empty string."""
    mock_sheet = mock.MagicMock()
    mock_sheet.cell.side_effect = [
            FakeCell(1, 1), FakeCell(2, 1), FakeCell(3, 1)
    ]
    assert ligrarian.first_blank_row(mock_sheet) == 3


class TestCheckYearSheetExists:
    """create_sheet only if no year_sheet in workbook, return workbook."""

    @mock.patch('ligrarian.create_sheet')
    @mock.patch('ligrarian.openpyxl')
    def test_year_sheet_exists_no_create_call(self, mock_pyxl, mock_create):
        """No call to create_sheet."""
        mock_pyxl.load_workbook.return_value.sheetnames = ['2019', '2020']
        ligrarian.check_year_sheet_exists('', '2020')

        mock_create.assert_not_called()

    @mock.patch('ligrarian.create_sheet')
    @mock.patch('ligrarian.openpyxl')
    def test_year_sheet_not_exist_create_call(self, mock_pyxl, mock_create):
        """One call to create_sheet."""
        mock_pyxl.load_workbook.return_value.sheetnames = ['2018', '2019']
        ligrarian.check_year_sheet_exists('', '2020')

        mock_create.assert_called_once()

    @mock.patch('ligrarian.openpyxl')
    def test_workbook_returned(self, mock_pyxl):
        """Mocked workbook (load_workbook()) returned."""
        mock_workbook = mock_pyxl.load_workbook()
        mock_pyxl.load_workbook.return_value.sheetnames = ['2020']
        returned_workbook = ligrarian.check_year_sheet_exists('', '2020')

        assert returned_workbook == mock_workbook


class TestCreateSheet:
    """Copies then renames sheet, blanks all but first, sets date function."""

    @mock.patch('ligrarian.first_blank_row', return_value=0)
    @mock.patch('ligrarian.openpyxl')
    def test_copies_sheet(self, mock_pyxl, mock_first):
        """Should call copy_worksheet on workbook object."""
        ligrarian.create_sheet(mock_pyxl, 'copy', 'new')

        mock_pyxl.copy_worksheet.assert_called_once()

    @mock.patch('ligrarian.first_blank_row', return_value=0)
    @mock.patch('ligrarian.openpyxl')
    def test_names_sheet(self, mock_pyxl, mock_first):
        """Should name sheet to new_sheet_name argument."""
        ligrarian.create_sheet(mock_pyxl, 'copy', 'new')

        assert mock_pyxl.copy_worksheet.return_value.title == 'new'

    @mock.patch('ligrarian.first_blank_row', return_value=2)
    @mock.patch('ligrarian.openpyxl')
    def test_first_row_cells_not_modified(self, mock_pyxl, mock_first):
        """First row not accessed by cell call for .value modification.

        Cells are blanked by setting their .value attributes to None. This
        requires the cell to be accessed via a call with row and column args;
        so no call to row 1 column 2 indicates that the first row hasn't been
        set to None.

        """
        mock_sheet = mock_pyxl.copy_worksheet
        ligrarian.create_sheet(mock_pyxl, 'copy', 'new')
        cell_calls = mock_sheet.return_value.cell.call_args_list

        assert mock.call(row=1, column=2) not in cell_calls

    @mock.patch('ligrarian.first_blank_row', return_value=2)
    @mock.patch('ligrarian.openpyxl')
    def test_other_row_cells_modified(self, mock_pyxl, mock_first):
        """Other rows cell's value attributes changed to None."""
        fake_two_one = FakeCell(2, 1)
        mock_pyxl.copy_worksheet.return_value.cell.side_effect = [
                fake_two_one,
                FakeCell(2, 2),
                FakeCell(2, 3),
                FakeCell(2, 4),
                FakeCell(2, 5),
                FakeCell(2, 6),
                FakeCell(5, 8),
        ]
        ligrarian.create_sheet(mock_pyxl, 'copy', 'new')
        assert fake_two_one.value == None

    @mock.patch('ligrarian.first_blank_row', return_value=2)
    @mock.patch('ligrarian.openpyxl')
    def test_date_formula_written_to_last_cell(self, mock_pyxl, mock_first):
        """Cell 5, 8 equal to date formula."""
        fake_last_call = FakeCell(5, 8)
        mock_pyxl.copy_worksheet.return_value.cell.side_effect = [
                FakeCell(2, 1),
                FakeCell(2, 2),
                FakeCell(2, 3),
                FakeCell(2, 4),
                FakeCell(2, 5),
                FakeCell(2, 6),
                fake_last_call,
        ]
        ligrarian.create_sheet(mock_pyxl, 'copy', 'new')
        assert fake_last_call.value == "=(TODAY()-DATE(new,1,1))/7"








