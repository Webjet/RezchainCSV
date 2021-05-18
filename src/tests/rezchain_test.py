import unittest
from datetime import date, datetime
from context import Rezchain, MapMissing
# from rezchaincsv import Rezchain


REQUIRED = {
    "Common Reference ID": "reference",
    "Amount": "amount",
    "Currency": "currency",
    "Booking Status": "status",
    "Last Modified Date": "last_modified",
}

OPTIONAL = {
    "Check In Date": "checkin",
    "Check Out Date": "checkout",
    "Number Of Nights": "nights",
    "Number Of Rooms": "rooms",
    "Booking Creation Date": "creation",
    "Your Booking ID": "id",
}


class TestStringMethods(unittest.TestCase):
    def test_required(self):
        rz = Rezchain(REQUIRED)
        self.assertEqual(set(rz.types.keys()), set(REQUIRED.values()))

    def test_optional(self):
        self.assertRaises(MapMissing, Rezchain, OPTIONAL)

    def test_csv(self):
        rz = Rezchain({**REQUIRED, **OPTIONAL})
        for i in range(100):
            it = {
                "reference": i,
                "amount": i * 100,
                "currency": f"CU{i}",
                "status": "CONFIRMED",
                "rooms": i,
            }
            if i % 2 == 0:
                # test native times
                it["last_modified"] = datetime.utcnow()
                it["creation"] = date.today()
            else:
                # test iso times
                it["last_modified"] = datetime.utcnow().isoformat()
                it["creation"] = date.today().isoformat()
            rz.add_item(it)
        rz.to_csv("test.csv")


if __name__ == '__main__':
    unittest.main()
