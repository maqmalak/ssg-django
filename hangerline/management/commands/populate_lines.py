from django.core.management.base import BaseCommand
from hangerline.models import Line


class Command(BaseCommand):
    help = 'Populate Line model with records for lines 21-32'

    def handle(self, *args, **options):
        # Line mapping following the SQL CASE pattern
        line_mapping = {
            '021': 'line-21',
            '022': 'line-22',
            '023': 'line-23',
            '024': 'line-24',
            '025': 'line-25',
            '026': 'line-26',
            '027': 'line-27',
            '028': 'line-28',
            '029': 'line-29',
            '030': 'line-30',
            '031': 'line-31',
            '032': 'line-32',
        }

        created_count = 0
        updated_count = 0

        for code, name in line_mapping.items():
            # Determine line type - alternating between 6r and 7a
            line_number = int(code)
            line_type = '6r' if line_number % 2 == 1 else '7a'

            # Create or update the line record
            line, created = Line.objects.update_or_create(
                code=code,
                defaults={
                    'type': line_type,
                    'name': name,
                    'server_ip': f"192.168.1.{int(code)}",
                    'server_name': f"Production Server {name}",
                    'active': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {line.code} - {line.name} (Type: {line.type})')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    f'Updated: {line.code} - {line.name} (Type: {line.type})'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(line_mapping)} lines. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )
