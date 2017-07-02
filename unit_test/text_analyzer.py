import unittest
import os
class TextAnalysisTests(unittest.TestCase):
    """tests for the analyze_text function"""

    def setUp(self):
        "fixture that creates a file for the text method to use"
        self.filename='text_analysis_test_file.txt'
        with open(self.filename,'w') as f:
            f.write('now we are engaged in a great civil war,\n'
            'testing wheather that nation,\n'
            'or any nation so conceived and so dedicated,\n'
            'can long endure')

    def tearDown(self):
        "Fixture that deletes the files used by the test methods."
        try:
            os.remove(self.filename)
        except OSError:
            pass
    def test_function_runs(self):
        analyze_text(self.filename)

    def test_line_count(self):
        #"check line count is correct"
        self.assertEqual(analyze_text(self.filename)[0],4)

    def test_character_count(self):
        # check the character count is correct
        self.assertEqual(analyze_text(self.filename)[1],131)

    def test_no_such_file(self):
        "check the proper exception is thrown for a missing file"
        with self.assertRaises(IOError):
            analyze_text('foobar')

    def test_no_deletion(self):
        "check that the function does not delete the input file"
        analyze_text(self.filename)
        self.assertTrue(os.path.exists(self.filename))



def analyze_text(filename):
    """calculate the number of lines and character in a filename
    Args:
        filename: the name of the file to analyze
    raises:
         IOError: if filename does not exist or cannot be read
    Returns: A tuple where the first
    element is the number of lines in the files
    and the second element is the num of char
    """

    lines=0
    chars=0
    with open(filename,'r') as f:
        for line in f:
            lines +=1
            chars +=len(line)

        return (lines,chars)
if __name__=='__main__':
    unittest.main()
