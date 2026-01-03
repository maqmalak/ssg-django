"""
Django management command to import styles data.
Usage: python manage.py import_styles
"""
from django.core.management.base import BaseCommand
from hangerline.models import Style


class Command(BaseCommand):
    help = 'Import styles data into the Style model'

    def handle(self, *args, **options):
        self.stdout.write("Starting style data import...")

        # Style data as provided - parsed from the input
        style_data = [
            ('9350', 'JACKET'),
            ('9250', 'PolyesterPant'),
            ('BMI9350', 'JACKET'),
            ('9250_1', 'Polyester Pant'),
            ('4233', 'T_Shirt'),
            ('2618', 'Vest-2618'),
            ('2619', 'vest-2619'),
            ('2623', 'SA2623-008'),
            ('2616', 'Bib'),
            ('SA2623-023', 'SA2623-023-Vest'),
            ('SA2623-026', 'SA2623-026-Vest'),
            ('Test-2616', 'Test_2616'),
            ('EX4239', 'Shirt 4239'),
            ('Test 4333', 'Test 4333'),
            ('TR11044YL', 'TR11044YL'),
            ('', 'TR11044YL - Bib Vest'),
            ('TR11949O/G', 'TR11949O/G'),
            ('', 'TR11949O/G -2618'),
            ('TR11045O/G', 'TR11045O/G'),
            ('', 'TR11045O/G -2618'),
            ('TR11950Y/B', 'TR11950Y/B'),
            ('', 'TR11950Y/B -2618'),
            ('TR11046Y/B', 'TR11046Y/B'),
            ('', 'TR11046Y/B -West ss'),
            ('LV2616', 'LV2616-VEST CLASSIC'),
            ('TR11043OR', 'TR11043OR'),
            ('', 'TR11043OR -  Vest 2616'),
            ('2616_1', '2616-Bib Vest'),
            ('MZ2616', 'MAINZ 05 Classic'),
            ('8850', 'SWEATER CLASSICO'),
            ('9322', 'Jacket Performance'),
            ('SS1360', 'Festival Hoodie'),
            ('4212', 'T-Shirt 4212'),
            ('9250S', 'Polyester Trouser 9250S'),
            ('9250', 'PRO Polyester Trouser'),
            ('Test-4233', 'Test 4233'),
            ('9250_27', 'TROUSERS CLASSICO'),
            ('4233', 'Jersey Team Shirt'),
            ('1003078', 'Base Layer Shirt'),
            ('4233D', 'Jersey Women S/S'),
            ('4333', 'Long Shirt Full Arm'),
            ('Test-', 'Test-'),
            ('D4233', 'SMU Trikot Team Shirt'),
            ('6479', 'Longsleeve Function Shirt'),
            ('U_103J251', 'SANTARO OVERSIZE HOODIE'),
            ('ISP4233', 'ISP Jersey Team Shirt'),
            ('K4211-8928845', 'JAKO ID Trikot'),
            ('K4221-8821190', 'JAKO ID Jersey S/S'),
            ('K4321-21501385', 'JAKO ID Trikot LA'),
            ('K4241-9031852', 'JAKO ID Handball'),
            ('K4211', 'JAKO ID Trikot'),
            ('K4221-9051708', 'Wurzburger Kickers'),
            ('K4221-22308528', 'TRIKOT KA'),
            ('K4212-8689679', 'TrikotTeamsport Erfurt'),
            ('K8921', 'JAKO ID TW-Trikot'),
            ('B4233', 'Jersey Team T-Shirt'),
            ('D4290', 'TSV Kareth-L appersdorf'),
            ('final test', 'final test'),
            ('9223', 'Power Pant Polyester'),
            ('9200', 'Polyester Trousers one'),
            ('TEST3', 'TEST3'),
            ('test', 'test'),
            ('9200-24', 'Polyester Pant 24'),
            ('TEST', 'TEST'),
            ('TEST2', 'TEST2'),
            ('8936', 'GK- PAD Pant'),
            ('9300', 'Polyester Jacket TL-26'),
            ('TEST4', 'TEST4'),
            ('6823', 'Hooded Jacket'),
            ('TEST5', 'TEST5'),
            ('9200-29', 'Polyester Pant 29'),
            ('Test-9300', 'Test-9300'),
            ('Test-6823', 'Test-6823'),
            ('Hanger Testing', 'Hanger Testing'),
            ('Test-9200', 'Test-9200'),
            ('8935', 'GK- Kelver Pant'),
            ('9300', 'Jacket TL-26'),
            ('Test-8936', 'Test-8936'),
            ('8939', 'GK-Shorts Striker'),
            ('9218', 'Polyester trousers com'),
            ('9323-25', 'Polyester Jacket Power S-25'),
            ('9218-27', 'Polyester trousers com-27'),
            ('ISP8450', 'Training trouser Classico'),
            ('9326', 'TL-26 Jacket'),
            ('9200L-29', 'Polyester Pant L 29'),
            ('9200S-29', 'Polyester Pant S 29'),
            ('7402', 'Rain Jacket'),
            ('TEST 27', 'TEST 27'),
            ('Test Hanger', 'Test Hanger'),
            ('9324', 'Polyester Jacket'),
            ('9300-22', 'Polyester Jacket TL-22'),
            ('Hanger Testing', 'Hanger Testing'),
            ('9289', 'Polyester Allround'),
            ('M_103B251', 'High performance short'),
            ('M_104B251', 'Aozora 365 short'),
            ('9300-25', 'Jacket TL-25'),
            ('6276', 'Running Double Shorts'),
            ('TEST6', 'TEST6'),
            ('6824', 'Jacket Hooded 24'),
            ('9218', 'Terry Pant'),
            ('9300-28', 'Polyester Jacket TL-26'),
            ('9323-23', 'Polyester Jacket Power S'),
            ('M-101B251', 'HYBRID KANZAI SHORT'),
            ('M9150-23', 'Polyester tracksuit CLA'),
            ('8489', 'Trainingshose Allround'),
            ('8450', 'Training trouser Classico'),
            ('9250D', 'Polyester trousers Lady'),
            ('9250L', 'TROUSERS CLASSICO LONG'),
        ]

        created_count = 0
        existing_count = 0
        updated_count = 0

        for style_key, style_description in style_data:
            # Skip empty keys
            if not style_key or not style_key.strip():
                continue

            # Clean the description
            style_description = style_description.strip() if style_description else ''

            # Try to get or create the style
            obj, created = Style.objects.get_or_create(
                style_key=style_key,
                defaults={'style_description': style_description}
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"Created: {style_key} - {style_description}"
                ))
            else:
                # Update if description is different
                if obj.style_description != style_description:
                    obj.style_description = style_description
                    obj.save()
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(
                        f"Updated: {style_key} - {style_description}"
                    ))
                else:
                    existing_count += 1
                    self.stdout.write(f"Already exists: {style_key} - {style_description}")

        total_processed = len([item for item in style_data if item[0] and item[0].strip()])
        self.stdout.write(self.style.SUCCESS(
            f"\nImport complete! "
            f"Total: {total_processed}, "
            f"Created: {created_count}, "
            f"Updated: {updated_count}, "
            f"Already existed: {existing_count}"
        ))
