import unittest
import q3

usr = "ritvik.jain.52206"

class TestQ3(unittest.TestCase):
    def test_checksimple(self):
        user1 = q3.scrape(usr)
        try:
            res = user1.for_test()
            self.assertEqual(res, "Task Over")

        except Exception as e:
            self.assertEqual(e, "Task Over")
    
    def test_checkWork(self):
        user2 = q3.scrape(usr)
        self.assertEqual(len(user2.work), 4)

        i = 1
        for item in user2.work:
            print(f'{i}) {item[0]},{item[1]}')
            i += 1

    def test_checkFavs(self):
        
        user3 = q3.scrape(usr)
        self.assertEqual(len(user3.fav) > 15, True)

        i = 1
        for item in user3.fav:
            print(f'{i}) {item}')
            i += 1

if __name__ =='__main__':
    unittest.main()