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


class TestModeSwitchMethod:
    """Mode switch adds/removes labels, menus and main text."""

    def test_mode_true_removes_format_label(self):
        """Call grid_remove on format label."""
        mock_Gui = mock.MagicMock()
        mock_Gui.mode.return_value = True
        ligrarian.Gui.mode_switch(mock_Gui)

        mock_Gui.format_label.grid_remove.assert_called_once()

    def test_mode_true_removes_format_menu(self):
        """Call grid_remove on format label."""
        mock_Gui = mock.MagicMock()
        ligrarian.Gui.mode_switch(mock_Gui)

        mock_Gui.format_menu.grid_remove.assert_called_once()

    def test_mode_true_configures_main_label_to_URL(self):
        """Call configure(text='URL') on main label."""
        mock_Gui = mock.MagicMock()
        ligrarian.Gui.mode_switch(mock_Gui)

        mock_Gui.main_label.configure.assert_called_once_with(text='URL')

    def test_mode_false_grids_format_label(self):
        """Call grid on format label."""
        mock_Gui = mock.MagicMock()
        mock_Gui.mode.get.return_value = False
        ligrarian.Gui.mode_switch(mock_Gui)

        mock_Gui.format_label.grid.assert_called_once()

    def test_mode_true_grids_format_menu(self):
        """Call grid on format label."""
        mock_Gui = mock.MagicMock()
        mock_Gui.mode.get.return_value = False
        ligrarian.Gui.mode_switch(mock_Gui)

        mock_Gui.format_menu.grid.assert_called_once()

    def test_mode_true_configures_main_label_to_search(self):
        """Call configure(text='search') on main label."""
        mock_Gui = mock.MagicMock()
        mock_Gui.mode.get.return_value = False
        ligrarian.Gui.mode_switch(mock_Gui)

        mock_Gui.main_label.configure.assert_called_once_with(text='Search')
