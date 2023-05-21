import unittest
from Nba import (
    Nba,
    NbaBoxScore
)


class NbaInstanceTestCase(unittest.TestCase):
    
    @classmethod
    def setUp(cls):
        "Hook method for setting fixture before running tests in the class"
        cls.driver = 'test'


    @classmethod
    def tearDown(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class"


    def testGetClassInstance(self):
        """__init__ 테스트 메소드"""

        # None 입력시 ValueError 발생하는지 확인하는 테스트
        with self.assertRaises(ValueError) as cm:
            Nba(None)
        exception = cm.exception
        self.assertEqual(str(exception), "Missing idx")

        # int 입력시 TypeError 발생하는지 확인하는 테스트
        with self.assertRaises(TypeError) as cm:
            Nba(1)
        exception = cm.exception
        self.assertEqual(str(exception), "Idx should be a string")


class NbaTestCase(unittest.TestCase):
    
    @classmethod
    def setUp(cls):
        "Hook method for setting fixture before running tests in the class"
        cls.driver = 'test'
        cls.instance = Nba('401547683')
        cls.idx = '401547683'


    @classmethod
    def tearDown(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class"


    def testGetIdx(self):
        """__init__ 테스트 메소드"""
        
        self.assertTrue(self.instance.idx, str)
        self.assertEqual(self.instance.idx, '401547683')


    def testGetUrl(self):
        """_get_url 함수 테스트 메소드"""
        
        # boxscore 입력시 url을 맞게 생성하는지 확인하는 테스트
        page_typ = 'boxscore'
        self.instance._get_url(page_typ)
        self.assertTrue(self.instance.url, str)
        self.assertEqual(
            self.instance.url,
            f"https://www.espn.com/nba/{page_typ}/_/gameId/{self.idx}"
        )

        # game 입력시 url을 맞게 생성하는지 확인하는 테스트
        page_typ = 'game'
        self.instance._get_url(page_typ)
        self.assertTrue(self.instance.url, str)
        self.assertEqual(
            self.instance.url,
            f"https://www.espn.com/nba/{page_typ}/_/gameId/{self.idx}"
        )

        # None 입력시 ValueError 발생하는지 확인하는 테스트
        page_typ = None
        self.assertRaises(ValueError, self.instance._get_url, page_typ)

        # 빈 배열 입력시 ValueError 발생하는지 확인하는 테스트
        page_typ = []
        self.assertRaises(ValueError, self.instance._get_url, page_typ)

        # int 입력시 TypeError 발생하는지 확인하는 테스트
        page_typ = 1
        self.assertRaises(TypeError, self.instance._get_url, page_typ)

        # boolean 입력시 TypeError 발생하는지 확인하는 테스트
        page_typ = True
        self.assertRaises(TypeError, self.instance._get_url, page_typ)

        # list 입력시 TypeError 발생하는지 확인하는 테스트
        page_typ = ['boxscore']
        self.assertRaises(TypeError, self.instance._get_url, page_typ)




if __name__ == '__main__':
    unittest.main()