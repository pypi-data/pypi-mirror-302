# test_file_utils.py

import unittest
from my_package123.file_utils import read_file, write_file, append_file

class TestFileUtils(unittest.TestCase):
    
    def test_read_file(self):
        with open('test_file.txt', 'w') as f:
            f.write("Hello, World!")
        
        content = read_file('test_file.txt')
        self.assertEqual(content, "Hello, World!")
    
    def test_write_file(self):
        write_file('test_file.txt', "New Content")
        content = read_file('test_file.txt')
        self.assertEqual(content, "New Content")
    
    def test_append_file(self):
        append_file('test_file.txt', " Appended Text")
        content = read_file('test_file.txt')
        self.assertEqual(content, "New Content Appended Text")

if __name__ == '__main__':
    unittest.main()
