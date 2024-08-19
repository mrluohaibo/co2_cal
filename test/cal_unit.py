import unittest

from co2_cal import Co2_Cal


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
    def test_cal(self):
        co2_cal_obj = Co2_Cal()
        ele_id = "electric"
        ele_input = 2
        result = co2_cal_obj.do_cal(ele_id, ele_input)
        expect_output = 1
        actual_output = result["output_val"]
        self.assertEqual(expect_output,actual_output)

if __name__ == '__main__':
    unittest.main()
