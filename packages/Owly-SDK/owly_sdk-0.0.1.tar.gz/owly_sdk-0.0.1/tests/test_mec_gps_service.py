"""

export PYTHONPATH=/home/foreur/Desktop/thomas/owly-sdk

"""

import unittest
import src.vim.vim_manager as vim

VIM_FILE = "/home/foreur/Desktop/thomas/blueprints/mec-gps-service/vim-edge.yaml"

class TestMECNSManagement(unittest.TestCase):
    
    def setUp(self):
        """Setup initial conditions."""
        self.vim_name = "edge"
        
        # Check if the VIM exists
        self.existing_vims = vim.list_vims()
        self.assertIsInstance(self.existing_vims, list, "The return value should be a list")
        # Delete the VIM if it exists
        if any(vim["name"] == self.vim_name for vim in self.existing_vims):
            vim.remove_vim(self.vim_name)
            
            
    def tearDown(self):
        """Clean up after the test."""
        # Delete all VIMs
        for v in vim.list_vims():
            vim.remove_vim(v["name"])
            

    def test_list_vims_returns_list(self):
        """Test that list_vims returns a list."""
        vims = vim.list_vims()
        self.assertIsInstance(vims, list, "The return value should be a list")

    def test_list_vims_returns_list_of_dicts(self):
        """Test that list_vims returns a list of dictionaries."""
        vims = vim.list_vims()
        for v in vims:
            self.assertIsInstance(v, dict, "Each element in the list should be a dictionary")
            
    def test_add_vim(self):
        """Test that add_vim adds a VIM."""
        res = vim.add_vim(VIM_FILE)
        
        vims = vim.list_vims()
        # Check if the VIM was added
        self.vim_name = "edge"
        self.assertTrue(any(v["name"] == self.vim_name for v in vims), "The VIM should have been added")
        
    def test_remove_vim(self):
        """Test that remove_vim removes a VIM."""
        res = vim.add_vim(VIM_FILE)
        
        vims = vim.list_vims()
        # Check if the VIM was added
        self.vim_name = "edge"
        self.assertTrue(any(v["name"] == self.vim_name for v in vims), "The VIM should have been added")
        
        res = vim.remove_vim(self.vim_name)
        
        vims = vim.list_vims()
        # Check if the VIM was removed
        self.assertFalse(any(v["name"] == self.vim_name for v in vims), "The VIM should have been removed")

if __name__ == "__main__":
    unittest.main()