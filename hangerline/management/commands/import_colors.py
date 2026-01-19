"""
Django management command to import colors data.
Usage: python manage.py import_colors
"""
from django.core.management.base import BaseCommand
from hangerline.models import Color


class Command(BaseCommand):
    help = 'Import colors data into the Color model'

    def handle(self, *args, **options):
        self.stdout.write("Starting color data import...")

        # Color data as provided
        color_data = [
            ('31', 'Stone', 'Stone Grey-40'),
            ('32', 'Red', 'Sport Red-01'),
            ('33', 'Neon Green', 'Neon Green-656'),
            ('34', 'Sport Red', 'Sport Red-661'),
            ('35', 'Neon Yello', 'Neon Yellow/Royal-03'),
            ('36', 'Blue', 'Blue-656'),
            ('37', 'White', 'White-657'),
            ('38', 'Neon Orang', 'Neon Orange-19'),
            ('39', 'Yellow', 'Yellow'),
            ('40', 'Orange', 'Orange'),
            ('41', 'Orange', 'Orange/Green'),
            ('42', 'Yellow', 'Yellow/Blue'),
            ('43', 'Purple', 'Purple-45'),
            ('44', 'BLUE', 'BLUE'),
            ('45', 'BLACK', 'BLACK-02'),
            ('20', 'Stone Grey', 'Stone Grey-660'),
            ('46', 'GREEN', 'GREEN'),
            ('47', 'Red-01', 'Red-01'),
            ('23', 'Neon Green', 'Neon Green-02'),
            ('24', 'Neon Yello', 'Neon Yellow/Royal-03'),
            ('25', 'Neon ', 'Neon Orange/st-19'),
            ('26', 'Neon', 'Neon Yellow-03'),
            ('27', 'Neon', 'Neon Yellow-657'),
            ('28', 'Neon', 'Neon Orange-658'),
            ('29', 'SKY BLUE', 'SKY BLUE-659'),
            ('30', 'SKY', 'SKY BLUE-45'),
            ('48', 'White-000', 'White-000'),
            ('49', 'Black-08-', ''),
            ('50', 'Royal-400', 'Royal-400'),
            ('51', 'Royal-04', 'Sport Royal-04'),
            ('79', 'BLACK', 'BLACK-800'),
            ('53', 'Sport', 'SPORT GREEN-06'),
            ('54', 'Seablue', 'Seablue-900'),
            ('55', 'Citro', 'Citro-03'),
            ('56', 'Night', 'Night Blue-42'),
            ('57', 'neon orang', '-19'),
            ('58', 'Navy', 'Navy-09'),
            ('59', 'SKY', 'SKY BLUE-430'),
            ('60', 'Seablue', 'Seablue-09'),
            ('80', 'SAGE', 'SAGE-08'),
            ('81', 'MAUVE', 'MAUVE-06'),
            ('82', 'TERRA COTT', 'TERRA COTTA-04'),
            ('83', 'Navy', 'Navy-kau10-0809'),
            ('65', 'Neon', 'Neon Green-25'),
            ('66', 'Flame', 'Flame-18'),
            ('67', 'White', 'White-00'),
            ('68', 'Jako', 'Jako Blue-89'),
            ('69', 'deep', 'deep Pink-170'),
            ('70', 'Purple', 'Purple-485'),
            ('71', 'Lime', 'Lime-23'),
            ('72', 'Black-08', 'Black-08'),
            ('84', 'Black-', 'Black-KAU10-0809'),
            ('85', 'Black', 'Black-KAU10-0809'),
            ('75', 'Mint White', 'Mint White JAKO Logo-663'),
            ('76', 'Mint Black', 'Mint Black JAKO Logo-662'),
            ('77', 'Coral', 'Coral-365'),
            ('78', 'mint', 'mint-251'),
            ('86', 'Flame', 'Flame-370'),
            ('87', 'Lime', 'Lime-270'),
            ('88', '#19541', '#19541 sport red-665'),
            ('89', 'Green', 'Green'),
            ('90', 'PPJ ', 'PPJ Helsinki nEON-664'),
            ('91', 'Black', 'Black/red-207'),
            ('92', 'Blue', 'Blue-656'),
            ('93', 'Navy', 'Navy,auqa-656'),
            ('94', 'LightBlue', 'LightBlue/skyblue-657'),
            ('95', 'Royal', 'Royal-656'),
            ('96', 'White', 'White-657'),
            ('97', 'Fuchsia', 'Fuchsia-658'),
            ('98', 'sport', 'sport ryal - home-656'),
            ('99', 'yellow', 'yellow - away-657'),
            ('100', 'Konfigurat', 'Konfigurator-6'),
            ('101', 'Baller', 'Ballermann Hits-656'),
            ('102', 'blue/', 'blue/green-656'),
            ('104', 'Royal', 'K4321-22879689-680L'),
            ('105', 'maroon', 'maroon ( dyed )-666'),
            ('106', 'purple', 'purple-656'),
            ('107', 'Konfigurat', 'Konfigurator-680'),
            ('108', 'Away', 'Away - Black-657'),
            ('109', 'Sport Red', 'Sport Red - Home-656'),
            ('110', 'Irish Moos', 'Irish Moos-02'),
            ('111', 'Purple', 'TSV K-L,purple-656'),
            ('112', 'Black', 'Black-800'),
            ('113', 'schwarz', 'schwarztonal-880'),
            ('114', 'RED/BLACK', 'RED/BLACK'),
            ('115', 'SPORT', 'SPORT GREEN-200'),
            ('116', 'Seablue', 'Seablue/Chili Red-901'),
            ('123', 'white/', 'WHITE/RED-004'),
            ('125', 'bLACK', 'Black/Citro-803'),
            ('126', 'Violet', 'Violet-486'),
            ('128', 'Red', 'Red-100'),
            ('129', 'Red', 'Red/Wine red-103'),
            ('130', 'Bordeaux', 'Bordeaux-155'),
            ('131', 'royal', 'royal/seablue-403'),
            ('132', 'Grey', 'Grey-825'),
            ('133', 'Black', 'Black/ANTHRA-801'),
            ('135', 'Navy', 'Navy-930'),
            ('136', 'seablue/', 'seablue/sky blue-910'),
            ('137', 'Anthracite', 'Anthracite-830'),
            ('138', 'Yellow', 'Yellow-335'),
            ('139', 'White', 'White/soft Grey-016'),
            ('146', 'Jako', 'Jako Blue-440'),
            ('147', 'Royal/', 'Royal/Black-408'),
            ('148', 'Wine', 'Wine red-01'),
            ('103', 'orange', 'orange/lila/grun-657'),
            ('117', 'Stone Grey', 'Stone Grey-840'),
            ('118', 'Soft Grey', 'Soft Grey/Dusky pink-851'),
            ('127', 'Black', 'Black/Neon Orange-807'),
            ('142', 'Soft Green', 'Soft Green/Sports Green-222'),
            ('151', 'Black', 'Black-01'),
            ('152', 'Royal', 'Royal-04'),
            ('153', 'Night', 'Night Blue/citro-42'),
            ('154', 'Maroon', 'Maroon-14'),
            ('155', 'Purple', 'Purple-10'),
            ('119', 'Navy', 'Navy/Citro-941'),
            ('121', 'Flame/', 'Flame/seablue-375'),
            ('144', 'anthra', 'anthra Light/mint green-852'),
            ('150', 'Black', 'Black/Red-812'),
            ('120', 'Royal', 'Royal-400'),
            ('122', 'Black/soft', 'Black/soft yellow-808'),
            ('124', 'seablue/', 'seablue/jakoblue-914'),
            ('149', 'seablue/re', 'seablue/red-909'),
            ('134', 'Neon', 'Neon Orange-350'),
            ('140', 'White', 'White-000'),
            ('141', 'Neon ora', 'Neon orange-350'),
            ('143', 'Borde aux', 'Borde aux-155'),
            ('145', 'Navy/', 'Navy/citro-941'),
        ]

        created_count = 0
        existing_count = 0
        updated_count = 0

        for cm_key, cm_short_description, cm_description in color_data:
            # Clean the descriptions
            cm_short_description = cm_short_description.strip() if cm_short_description else ''
            cm_description = cm_description.strip() if cm_description else ''

            # Try to get or create the color
            obj, created = Color.objects.get_or_create(
                cm_key=cm_key,
                defaults={
                    'cm_short_description': cm_short_description,
                    'cm_description': cm_description
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"Created: {cm_key} - {cm_short_description} - {cm_description}"
                ))
            else:
                # Update if descriptions are different
                if (obj.cm_short_description != cm_short_description or
                    obj.cm_description != cm_description):
                    obj.cm_short_description = cm_short_description
                    obj.cm_description = cm_description
                    obj.save()
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(
                        f"Updated: {cm_key} - {cm_short_description} - {cm_description}"
                    ))
                else:
                    existing_count += 1
                    self.stdout.write(f"Already exists: {cm_key} - {cm_short_description}")

        total_processed = len(color_data)
        self.stdout.write(self.style.SUCCESS(
            f"\nImport complete! "
            f"Total: {total_processed}, "
            f"Created: {created_count}, "
            f"Updated: {updated_count}, "
            f"Already existed: {existing_count}"
        ))
