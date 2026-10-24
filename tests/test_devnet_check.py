import io
import unittest
from unittest.mock import patch
import devnet_check as checker


class Tests(unittest.TestCase):
    def test_result(self):
        self.assertEqual(checker.parse_rpc_result({'result': 123}, 'getSlot'), 123)

    def test_reject_rpc_error(self):
        with self.assertRaisesRegex(ValueError, 'RPC error'):
            checker.parse_rpc_result({'error': {'code': -1}}, 'getSlot')

    def test_reject_missing_result(self):
        with self.assertRaisesRegex(ValueError, 'no result'):
            checker.parse_rpc_result({}, 'getSlot')

    @patch.object(checker, 'rpc', side_effect=[checker.DEVNET_GENESIS, 12345])
    def test_good_devnet(self, rpc):
        with patch('sys.stdout', new_callable=io.StringIO) as out:
            self.assertEqual(checker.main([]), 0)
        self.assertIn('PASS:', out.getvalue())
        self.assertEqual(rpc.call_count, 2)

    @patch.object(checker, 'rpc', return_value='bad-genesis')
    def test_reject_wrong_chain_before_balance(self, rpc):
        with patch('sys.stderr', new_callable=io.StringIO):
            self.assertEqual(checker.main(['--address', '11111111111111111111111111111111']), 2)
        self.assertEqual(rpc.call_count, 1)

    @patch.object(checker, 'rpc', side_effect=[checker.DEVNET_GENESIS, 999, {'value': 250000000}])
    def test_balance(self, rpc):
        with patch('sys.stdout', new_callable=io.StringIO) as out:
            self.assertEqual(checker.main(['--address', '11111111111111111111111111111111']), 0)
        self.assertIn('0.250000000 Devnet SOL', out.getvalue())


if __name__ == '__main__':
    unittest.main()
