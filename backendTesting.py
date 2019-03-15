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
        admin = "debrsa01@luther.edu"
        test_group = "test_group_01"
        self.assertEqual(hello.create_group(test_group, admin), None) # no return value
        print("*=============================================================*")

    def test_get_data(self):
        print("test_get_data")
        test_group = "test_group_01"
        self.assertEqual(len(hello.get_data(test_group)), 2) # as long as the return value makes sense
        print("Let's see what the return value is:")
        print(hello.get_data(test_group))
        print("*=============================================================*")

    # def test_get_team_member_file(self):
    # not yet implemented
    #     print("test_get_team_member_file")
    #     test_group = "test_group_01"
    #     self.assertEqual(type(hello.get_team_member_file(test_group)), type(list()))
    #     print(hello.get_team_member_file(test_group))

    def test_delete_team(self):
        print("test_delete_team")
        test_group = "test_group_01"
        self.assertEqual(type(hello.delete_group(test_group)),type(list()))
        # I need to be logged in so that I can delete it; admin privileges needed


if __name__ == '__main__':
    unittest.main()
