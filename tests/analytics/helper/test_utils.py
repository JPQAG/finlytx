
def test_raises(self, result, raisesErrorText):
    with self.assertRaises(Exception) as context:
        result
    self.assertEqual(context.exception.args[0], raisesErrorText)