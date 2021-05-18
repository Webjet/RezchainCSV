from numbers import Number
import unittest
from datetime import date, datetime
from context import *
# from rezchaincsv.exceptions import ItemWrong, MapWrong


REQUIRED = {
    "reference": "Common Reference ID",
    "amount": "Amount",
    "currency": "Currency",
    "status": "Booking Status",
    "last_modified": "Last Modified Date",
}

OPTIONAL = {
    "checkin": "Check In Date",
    "checkout": "Check Out Date",
    "nights": "Number Of Nights",
    "rooms": "Number Of Rooms",
    "creation": "Booking Creation Date",
    "id": "Your Booking ID",
}


class TestStringMethods(unittest.TestCase):
    def test_required(self):
        rz = Rezchain(REQUIRED)
        self.assertEqual(set(rz.types.keys()), set(REQUIRED.keys()))

    def test_extra(self):
        # Bad timestamp
        m = REQUIRED.copy()
        m["test"] = None
        m["test_number"] = Number(null=True)
        m["test_null"] = Number(null=True)
        m["date_null"] = Date(null=True)
        rz = Rezchain(m)
        d = {
            "reference": "id",
            "amount": 1,
            "currency": "CUR",
            "status": "status",
            "last_modified": "2021-01-01 00:00:00",
            "test": 5,
            "test_number": "7",
            "test_null": "a",
            "date_null": "z",
        }
        it = rz.add_item(d)
        self.assertIsInstance(it["test"], str)
        self.assertEqual(it["test"], "5")

    def test_extra_error(self):
        # Bad timestamp
        m = REQUIRED.copy()
        m["test_number"] = Number()
        rz = Rezchain(m)
        d = {
            "reference": "id",
            "amount": 1,
            "currency": "CUR",
            "status": "status",
            "last_modified": "2021-01-01 00:00:00",
            "test_number": "a",
        }
        self.assertRaises(ValueError, rz.add_item, d)

    def test_required(self):
        self.assertRaises(MapMissing, Rezchain, {"reference": "Common Reference ID"})

    def test_bad_timestamp(self):
        # Bad timestamp
        rz = Rezchain(REQUIRED)
        d = {
            "reference": "id",
            "amount": 1,
            "currency": "CUR",
            "status": "status",
            "last_modified": "2021-01-01-bad",
        }
        self.assertRaises(ValueError, rz.add_item, d)

    def test_bad_date(self):
        # Bad timestamp
        m = REQUIRED.copy()
        m["creation"] = "Booking Creation Date"
        rz = Rezchain(m)
        d = {
            "reference": "id",
            "amount": 1,
            "currency": "CUR",
            "status": "status",
            "last_modified": "2021-01-01 00:00:00",
            "creation": "2021-01-234",
        }
        self.assertRaises(ValueError, rz.add_item, d)

    def test_unmapped(self):
        # Bad extra value
        rz = Rezchain(REQUIRED)
        it = {
            "reference": "id",
            "amount": 1,
            "currency": "CUR",
            "status": "status",
            "last_modified": "2021-01-01 00:00:00",
            "extra": "wrong"
        }
        it = rz.add_item(it)
        self.assertFalse("extra" in it)

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
