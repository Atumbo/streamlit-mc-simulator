import unittest
from process_steps import ExponentialStep, NormalStep, UniformStep


class TestExponentialStep(unittest.TestCase):
    def test_valid_inputs(self):
        step = ExponentialStep("exp", 4)
        self.assertEqual(step.name, "exp")
        self.assertEqual(step.rate, 4)

    def test_invalid_name(self):
        with self.assertRaises(AssertionError):
            ExponentialStep(123, 4)

    def test_invalid_type_rate(self):
        with self.assertRaises(AssertionError):
            ExponentialStep("exp", "kolme")

    def test_invalid_rate(self):
        with self.assertRaises(AssertionError):
            ExponentialStep("exp", 0)


class TestNormalStep(unittest.TestCase):
    def test_valid_inputs(self):
        step = NormalStep("nor", 10, 1)
        self.assertEqual(step.name, "nor")
        self.assertEqual(step.mean, 10)
        self.assertEqual(step.stdev, 1)

    def test_invalid_name(self):
        with self.assertRaises(AssertionError):
            NormalStep(name=159, mean=10, stdev=1)

    def test_invalid_mean(self):
        with self.assertRaises(AssertionError):
            NormalStep(name="nor", mean=-1, stdev=1)

    def test_invalid_type_mean(self):
        with self.assertRaises(AssertionError):
            NormalStep(name="nor", mean="yksi", stdev=1)

    def test_invalid_stdev(self):
        with self.assertRaises(AssertionError):
            NormalStep(name="nor", mean=1, stdev=-5)

    def test_invalid_type_stdev(self):
        with self.assertRaises(AssertionError):
            NormalStep(name="nor", mean=1, stdev="kolme")


class TestUniformStep(unittest.TestCase):
    def test_valid_inputs(self):
        step = UniformStep("uni", 5, 10)
        self.assertEqual(step.name, "uni")
        self.assertEqual(step.low, 5)
        self.assertEqual(step.high, 10)

    def test_invalid_low(self):
        with self.assertRaises(AssertionError):
            UniformStep(name="uni", low="numperi", high=10)

    def test_invalid_high(self):
        with self.assertRaises(AssertionError):
            UniformStep(name="uni", low=5, high="numperi")

    def test_invalid_high_2(self):
        with self.assertRaises(AssertionError):
            UniformStep(name="uni", low=6, high=5)

    def test_invalid_name(self):
        with self.assertRaises(AssertionError):
            UniformStep(name=123123, low=1, high=2)

    def test_invalid_name2(self):
        with self.assertRaises(AssertionError):
            UniformStep(name=0.1, low=1, high=2)


if __name__ == "__main__":
    unittest.main()
