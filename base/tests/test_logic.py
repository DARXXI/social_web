from django.test import TestCase

def Calculate(x,y,z):
    if z == '+':
        return (x + y)
    if z == '-':
        return (x - y)


class LogicTestCase(TestCase):
    def test_plus(self):
        result = Calculate(1, 3, '+')
        self.assertEqual(4, result)

        