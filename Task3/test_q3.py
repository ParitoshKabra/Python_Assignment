import unittest
import q3

usr = "ritvik.jain.52206"
user = q3.scrape(usr)


class TestQ3(unittest.TestCase):
    def test_checksimple(self):
        try:
            res = user.for_test()
            self.assertEqual(res, "Task Over")

        except Exception as e:
            self.assertEqual(e, "Task Over")
    
    def test_checkWork(self):
        self.assertEqual(len(user.work), 3)
        i = 1
        for item in user.work:
            print(f'{i}) {item[0]},{item[1]}')
            i += 1

    def test_checkFavs(self):

        self.assertEqual(len(user.fav) > 40, True)

        i = 1
        for item in user.fav:
            print(f'{i}) {item}')
            i += 1

if __name__ =='__main__':
    unittest.main()