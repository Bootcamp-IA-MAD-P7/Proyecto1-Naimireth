import unittest
# Importamos la función con su nuevo nombre desde taximetrov1.py
from taximetrov1 import calculate_fare 

class TestCalculateFare(unittest.TestCase):
    
    # --- TEST 1: Probar solo tiempo parado (stopped) ---
    def test_only_stopped(self):
        # 10 segundos * 0.02 = 0.20
        result = calculate_fare(10, 0)
        self.assertEqual(result, 0.20)

    # --- TEST 2: Probar solo tiempo en movimiento (moving) ---
    def test_only_moving(self):
        # 10 segundos * 0.05 = 0.50
        result = calculate_fare(0, 10)
        self.assertEqual(result, 0.50)

    # --- TEST 3: Probar ambos combinados (combined) ---
    def test_combined_fare(self):
        # (10 * 0.02) + (10 * 0.05) = 0.20 + 0.50 = 0.70
        result = calculate_fare(10, 10)
        self.assertEqual(result, 0.70)

if __name__ == '__main__':
    unittest.main()