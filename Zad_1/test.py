import unittest
from .main import Calc, Node

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.root = Node(5)
        self.lvl_1_l = Node(3)
        self.lvl_1_r = Node(7)
        self.lvl_2_ll = Node(2)
        self.lvl_2_lr = Node(5)
        self.lvl_2_rl = Node(1)
        self.lvl_2_rr = Node(0)
        self.lvl_3_l = Node(2)
        self.lvl_3_r = Node(8)
        self.lvl_4 = Node(5)
        self.root.children.extend([self.lvl_1_l, self.lvl_1_r])
        self.lvl_1_l.children.extend([self.lvl_2_ll, self.lvl_2_lr])
        self.lvl_1_r.children.extend([self.lvl_2_rl, self.lvl_2_rr])
        self.lvl_2_rr.children.extend([self.lvl_3_l, self.lvl_3_r])
        self.lvl_3_r.children.append(self.lvl_4)
        self.cal = Calc()

    def testSum(self):
        self.assertEqual(self.cal.sum(self.lvl_1_l), 10)
        self.assertEqual(self.cal.sum(self.lvl_1_r), 23)

    def testAvg(self):
        self.assertEqual(self.cal.avgValue(self.lvl_1_r), 23/6) #3,8(3)
        self.assertEqual(self.cal.avgValue(self.lvl_2_rr), 3.75)

    def testMedian(self):
        self.assertEqual(self.cal.median(self.root), 4)
        self.assertEqual(self.cal.median(self.lvl_1_l), 3)

if __name__ == '__main__':
    unittest.main()