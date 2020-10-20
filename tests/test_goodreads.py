#!/usr/bin/env python3

import pytest
import unittest.mock as mock

import ligrarian


class TestCreateDriver:
    """Test function creates appropriate driver and message.

    Testing of the webdriver object is done via capturing the call arguments
    to a mocked webdriver. A call with no arguments is indicative of the
    default, non-headless webdriver.
    """

    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_driver(self, mocked_driver):
        """Headless False should create non-headless (no call args) driver."""
        ligrarian.create_driver(False)
        assert mocked_driver.call_args == ''

    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_headless_driver(self, mocked_driver):
        """Headless True should create headless (call args) driver."""
        ligrarian.create_driver(True)
        assert mocked_driver.call_args != ''

    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_driver_message(self, mocked_driver, capsys):
        """Headless False should print non-headless message."""
        ligrarian.create_driver(False)
        captured_stdout = capsys.readouterr()[0]
        assert "headless" not in captured_stdout

    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_driver_headless_message(self, mocked_driver, capsys):
        """Headless True should print headless message."""
        ligrarian.create_driver(True)
        captured_stdout = capsys.readouterr()[0]
        assert "headless" in captured_stdout


class TestCategoryAndGenre:
    """Test function returns right category, genre tuple."""

    def test_category_and_genre_nonfiction(self):
        """Nonfiction in shelves should lead to Nonfiction category return."""
        assert ligrarian.category_and_genre(
                ["Genre", "Nonfiction"]) == ("Nonfiction", "Genre")

    def test_category_and_genre_fiction(self):
        """No Nonfiction in shelves should lead to Fiction category return."""
        assert ligrarian.category_and_genre(
                ["No Category", "Genre"]) == ("Fiction", "No Category")

