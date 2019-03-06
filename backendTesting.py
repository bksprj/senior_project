import unittest
import hello



test_group = "test_group_01"


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
        admin = "debrsa01@luther.edu"
        self.assertEqual(hello.create_group(test_group, admin), None) # no return value
        print("*=============================================================*")

    def test_get_data(self):
        print("test_get_data")
        self.assertEqual(len(hello.get_data(test_group)), 2) # as long as the return value makes sense
        print("Let's see what the return value is:")
        print(hello.get_data(test_group))
        print("*=============================================================*")

    def test_get_team_member_file(self):
        print("test_get_team_member_file")
        self.assertEqual(type(hello.get_team_member_file(test_group)), type(list()))
        print(hello.get_team_member_file(test_group))

if __name__ == '__main__':
    unittest.main()
