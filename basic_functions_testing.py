import unittest
import hello

hello.useremail = "test@admin.com"

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

    # It seems that the order to tests run is determined by the order of all the
    # tests in alphabetical order. The tests are run in ascending alphabetical order

    # the naming scheme will be:
    # test_order_user-defined-function-name

    def test_a_create_group(self):
        print("test_create_group")
        admin = "test@admin.com"
        test_group = "test_group_01"
        self.assertEqual(hello.create_group(test_group, admin), [f"The team {test_group} has been created"]) 
        print("*=============================================================*")

    def test_b_get_data(self):
        print("test_get_data")
        test_group = "test_group_01"
        result = hello.get_data(test_group)
        self.assertEqual(result, [[[{'Notifications': []}, {'Files': []}, {'Tasks': []}], []], True])
        # print("Let's see what the return value is:")
        # print(result)
        print("*=============================================================*")

    def test_bb_add_members(self):
        print("test_add_members")
        test_group = "test_group_01"
        test_members = "Admin:debrsa01@luther.edu|Standard:standarduser@gmail.com"
        hello.add_new_members(test_group,test_members)
        result = hello.get_data(test_group)
        print(f"the result of adding members is: {result}")
        self.assertEqual(hello.get_members(test_group), \
        [['Admin', ['test@admin.com', 'debrsa01@luther.edu']], ['Standard', ['standarduser@gmail.com']]])
        print("*=============================================================*")

    def test_c_delete_team(self):
        print("test_delete_team")
        test_group = "test_group_01"
        self.assertEqual(hello.delete_group(test_group),[f"The group {test_group} has been deleted."])
        print("*=============================================================*")

    def test_d_delete_team_after_delete_team(self):
        print("test_delete_team_after_delete_team")
        test_group = "test_group_01"
        self.assertEqual(hello.delete_group(test_group), [f'The group {test_group} does not exist.'])
        print("*=============================================================*")

    def test_dd_get_data_after_team_deletion(self):
        print("test_get_data_after_team_deletion")
        test_group = "test_group_01"
        result = hello.get_data(test_group)
        self.assertEqual(result, [[f'The group: {test_group} does not exist.'], False])
        print("*=============================================================*")



if __name__ == '__main__':
    unittest.main()
