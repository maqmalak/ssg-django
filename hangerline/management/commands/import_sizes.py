"""
Django management command to import sizes data.
Usage: python manage.py import_sizes
"""
from django.core.management.base import BaseCommand
from hangerline.models import Size


class Command(BaseCommand):
    help = 'Import sizes data into the Size model'

    def handle(self, *args, **options):
        self.stdout.write("Starting size data import...")

        # Size data as provided
        size_data = [
            ('63', '104'),
            ('64', 'M'),
            ('65', 'S'),
            ('66', 'XXL'),
            ('67', 'XL'),
            ('68', '01'),
            ('69', '02'),
            ('70', '00'),
            ('72', 'Senior'),
            ('73', 'Junior'),
            ('74', '116'),
            ('75', '128'),
            ('76', '140'),
            ('77', '152'),
            ('78', '164'),
            ('79', 'L'),
            ('82', '4XL'),
            ('81', '3XL'),
            ('83', '27'),
            ('84', '28'),
            ('85', '29'),
            ('86', '30'),
            ('87', '24'),
            ('88', '25'),
            ('89', '26'),
            ('92', '134'),
            ('91', '158'),
            ('93', '122'),
            ('94', '136'),
            ('95', '146'),
            ('96', '104'),
            ('97', '110'),
            ('98', '102'),
            ('99', '94'),
            ('100', '98'),
            ('101', '106'),
            ('102', '34'),
            ('103', '44'),
            ('104', '40'),
            ('105', '42'),
            ('106', '36'),
            ('107', '38'),
            ('108', '34'),
            ('109', '104'),
            ('110', ''),
            ('111', '110/116'),
            ('112', '122/128'),
            ('113', '134/140'),
            ('114', '146/152'),
            ('115', '46'),
            ('116', '5XL'),
            ('117', '5XL'),
            ('118', '48'),
            ('119', 'XXS'),
            ('120', '30'),
        ]

        created_count = 0
        existing_count = 0
        updated_count = 0

        for sm_key, sm_description in size_data:
            # Clean the description
            sm_description = sm_description.strip() if sm_description else ''

            # Try to get or create the size
            obj, created = Size.objects.get_or_create(
                sm_key=sm_key,
                defaults={'sm_description': sm_description}
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {sm_key} - {sm_description}"))
            else:
                # Update if description is different
                if obj.sm_description != sm_description:
                    obj.sm_description = sm_description
                    obj.save()
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f"Updated: {sm_key} - {sm_description}"))
                else:
                    existing_count += 1
                    self.stdout.write(f"Already exists: {sm_key} - {sm_description}")

        total_processed = len(size_data)
        self.stdout.write(self.style.SUCCESS(
            f"\nImport complete! "
            f"Total: {total_processed}, "
            f"Created: {created_count}, "
            f"Updated: {updated_count}, "
            f"Already existed: {existing_count}"
        ))
