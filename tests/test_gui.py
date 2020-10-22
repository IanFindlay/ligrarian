#!/usr/bin/env python3

"""Tests for ligrarian's GUI-related functions."""

import unittest.mock as mock

import ligrarian


@mock.patch('ligrarian.tk')
class TestCreateGUI:
    """Test function creates and returns GUI instance correctly."""

    def test_tk_called(self, mock_tk):
        """tk.Tk() create tkinter instance and should be called."""
        ligrarian.create_gui(mock.MagicMock())
        mock_tk.Tk.assert_called_once()

    def test_gui_instance_created(self, mock_tk):
        """Returned object should be instance of GUI class."""
        gui_instance = ligrarian.create_gui(mock.MagicMock())
        assert isinstance(gui_instance, ligrarian.Gui)


class TestGuiModeDetailsEdits:
    """Test funtion modifies gui.info and returns correctly."""

    class FakeGui:
        """A fake version of ligrarian's Gui class."""

        def __init__(self):
            self.mode = True
            self.info = {'main': "fake main"}


    def test_mode_true_moves_main_to_url(self):
        """True should lead to info['main'] copied to info['url']."""
        mock_gui = self.FakeGui()
        info = ligrarian.gui_mode_details_edits(mock_gui)
        assert info['url'] == "fake main"

    def test_mode_false_moves_main_to_search(self):
        """False should lead to info['main'] copied to info['search']."""
        mock_gui = self.FakeGui()
        mock_gui.mode = False
        info = ligrarian.gui_mode_details_edits(mock_gui)
        assert info['search'] == "fake main"

    def test_main_deleted(self):
        """gui.info['main'] should be deleted."""
        mock_gui = self.FakeGui()
        info = ligrarian.gui_mode_details_edits(mock_gui)
        assert 'main' not in info

    def test_info_dict_returned(self):
        """gui.info should be returned."""
        mock_gui = self.FakeGui()
        info = ligrarian.gui_mode_details_edits(mock_gui)
        assert info == {'url': "fake main"}
