import unittest
import hello

class TestStringMethods(unittest.TestCase):

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

    def test_create_group(self):
        print("test_create_group")
        test_group = "test_group_01"
        admin = "debrsa01@luther.edu"
        self.assertEqual(hello.create_group(test_group, admin), None) # no return value
        print("*=============================================================*")

    def test_get_data(self):
        print("test_get_data")
        test_group = "test_group_01"
        self.assertEqual(len(hello.get_data(test_group)), 2) # as long as the return value makes sense
        print("Let's see what the return value is:")
        print(hello.get_data(test_group))
        print("*=============================================================*")

if __name__ == '__main__':
    unittest.main()
