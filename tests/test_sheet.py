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


