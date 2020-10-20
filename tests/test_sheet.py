#!/usr/bin/env python3

import pytest
import unittest.mock as mock

import ligrarian


def test_first_blank_row():
    """Return row where cell.value is an empty string."""

    class FakeCell:
        """A fake version of openpyxl's workbook.sheet.cell."""

        def __init__(self, row, column):
            """Use row to simulate different values in different cells."""
            if row == 3:
                self.value = ''
            else:
                self.value = 'not blank'

    mock_sheet = mock.MagicMock()
    mock_sheet.cell.side_effect = [
            FakeCell(1, 1), FakeCell(2, 1), FakeCell(3, 1)
    ]
    assert ligrarian.first_blank_row(mock_sheet) == 3

