import unittest
from process import Process
from process_steps import ExponentialStep, NormalStep, UniformStep


class TestProcess(unittest.TestCase):
    def setUp(self):
        self.process = Process()
        self.exponential_step = ExponentialStep(name="expo", rate=4)
        self.normal_step = NormalStep(name="normal", mean=12, stdev=2)
        self.uniform_step = UniformStep(name="uni", low=8, high=11)

    def test_insert_steps(self):
        self.process.insertAtEnd(self.exponential_step)
        self.process.insertAtEnd(self.normal_step)
        self.process.insertAtEnd(self.uniform_step)

        self.assertEqual(self.process.get_names(), ["expo", "normal", "uni"])

    def test_invalid_step(self):
        with self.assertRaises(TypeError):
            self.process.insertAtEnd("This is a string")

    def test_delete_step(self):
        self.process.insertAtEnd(self.exponential_step)
        self.process.insertAtEnd(self.normal_step)
        self.process.insertAtEnd(self.uniform_step)

        self.process.deleteStep("normal")
        self.assertEqual(self.process.get_names(), ["expo", "uni"])

        self.process.deleteStep("expo")
        self.assertEqual(self.process.get_names(), ["uni"])

        self.process.deleteStep("ei ole")
        self.assertEqual(self.process.get_names(), ["uni"])

        self.process.deleteStep("uni")
        self.assertEqual(self.process.get_names(), [])

    def test_simulate(self):
        self.process.insertAtEnd(self.exponential_step)
        self.process.insertAtEnd(self.normal_step)
        self.process.insertAtEnd(self.uniform_step)

        results = self.process.simulate_process(n_simulations=1000)

        self.assertEqual(list(results.columns), ["expo", "normal", "uni", "Total"])
        self.assertEqual(results.shape, (1000, 4))

    def test_update_step(self):
        self.process.insertAtEnd(self.exponential_step)
        self.process.insertAtEnd(self.normal_step)
        self.process.insertAtEnd(self.uniform_step)

        self.process.update_step("expo", rate=3)
        self.assertEqual(self.exponential_step.rate, 3)

        self.process.update_step("normal", mean=13, stdev=3)

        self.assertEqual(self.normal_step.mean, 13)
        self.assertEqual(self.normal_step.stdev, 3)

        self.process.update_step("uni", low=9, high=12)

        self.assertEqual(self.uniform_step.low, 9)
        self.assertEqual(self.uniform_step.high, 12)


if __name__ == "__main__":
    unittest.main()
