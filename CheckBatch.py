import unittest



def check_Batch(details, nominal, tolerance):
    if tolerance < 0:
        raise ValueError("нельзя отрицательную")

    if len(details) > 100:
        raise ValueError("больше ста")

    lowerLimit = nominal - tolerance
    upperLimit = nominal + tolerance

    good = []
    rejected = []

    belowLower = 0
    aboveUpper = 0

    sizes=[]
    deviations = []

    for detail_id, size in details:
        deviation = size - nominal

        sizes.append(size)
        deviations.append(deviation)

        if size < lowerLimit:
            belowLower+=1
            rejected.append({
                "id": detail_id,
                "size": size,
                "deviation": deviation,
                "reason": "ниже нижней границы"
            })
        elif size > upperLimit:
            aboveUpper +=1
            rejected.append({
                "id": detail_id,
                "size": size,
                "deviation": deviation,
                "reason": "выше верхней границы"
            })
        else:
            good.append({
                "id": detail_id,
                "size": size,
                "deviation": deviation,
            })

    total = len(details)

    summary = {
        "total":total,
        "good":len(good),
        "rejected":len(rejected),
        "belowLower":belowLower,
        "aboveUpper":aboveUpper,

        "goodShare": len(good) / total if total else 0.0,
        "belowShare": belowLower / total if total else 0.0,
        "upperShare": aboveUpper / total if total else 0.0,

        "lowerLimit": lowerLimit,
        "upperLimit": upperLimit,

        "minSize": min(sizes) if sizes else None,
        "maxSize": max(sizes) if sizes else None,

        "minDeviation": min(deviations) if deviations else None,
        "maxDeviation": max(deviations) if deviations else None,
    }

    return {
        "good": good,
        "rejected": rejected,
        "summary":summary
    }



# тесты. запускаете и там типо тесты проводятся и всё хорошо и победа ураураураура
class TestCheckBatch(unittest.TestCase):
    def test_boundry_is_good(self):
        result = check_Batch(
            [
                ("A", 9.5),
                ("B",10.5)
            ],
            nominal=10,
            tolerance=0.5
        )

        self.assertEqual(result["summary"]["good"],2)
        self.assertEqual(result["summary"]["rejected"], 0)

    def test_below_and_above(self):
        result = check_Batch(
            [
                ("A", 9.4),
                ("B", 10.6)
            ],
            nominal=10,
            tolerance=0.5
        )

        self.assertEqual(result["summary"]["good"], 0)
        self.assertEqual(result["summary"]["rejected"], 2)

        self.assertEqual(result["rejected"][0]["reason"],"ниже нижней границы")
        self.assertEqual(result["rejected"][1]["reason"], "выше верхней границы")

    def test_summary_and_extremes(self):
        result = check_Batch(
            [
                ("A", 9),
                ("B", 10),
                ("C", 11)
            ],
            nominal=10,
            tolerance=0.5
        )

        s = result["summary"]
        self.assertEqual(s["total"],3)
        self.assertEqual(s["good"],1)
        self.assertEqual(s["rejected"],2)

        self.assertAlmostEqual(s["goodShare"],1/3)
        self.assertAlmostEqual(s["belowShare"], 1 / 3)
        self.assertAlmostEqual(s["upperShare"], 1 / 3)

        self.assertEqual(s["maxDeviation"],1.0)
        self.assertEqual(s["minDeviation"], -1.0)

    def test_empty(self):
        result = check_Batch(
            [],
            nominal=10,
            tolerance=0.5
        )

        s = result["summary"]
        self.assertEqual(s["total"], 0)
        self.assertEqual(s["good"], 0)
        self.assertEqual(s["rejected"], 0)

        self.assertEqual(s["minSize"], None)



print(check_Batch(
    [
        ("A", 9),
        ("B", 10),
        ("C", 11),

    ],
    nominal=10,
    tolerance=0.5))