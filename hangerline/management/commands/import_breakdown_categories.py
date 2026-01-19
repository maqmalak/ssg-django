"""
Django management command to import breakdown categories from Excel file.
Usage: python manage.py import_breakdown_categories /path/to/file.xlsx
"""
from django.core.management.base import BaseCommand
import pandas as pd
from hangerline.models import BreakdownCategory


class Command(BaseCommand):
    help = 'Import unique operation titles from Excel file as breakdown categories'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')
        parser.add_argument(
            '--column',
            type=str,
            default='Title',
            help='Column name containing the category names (default: Title)'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        column_name = options['column']

        self.stdout.write(f"Reading Excel file: {file_path}")

        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            self.stdout.write(f"Found {len(df)} rows in Excel file")
            self.stdout.write(f"Columns: {list(df.columns)}")

            if column_name not in df.columns:
                self.stdout.write(
                    self.style.ERROR(f"Column '{column_name}' not found in Excel file")
                )
                return

            # Get unique values from the specified column
            unique_titles = df[column_name].dropna().unique()
            self.stdout.write(f"Found {len(unique_titles)} unique values in '{column_name}' column")

            created_count = 0
            existing_count = 0

            for title in unique_titles:
                title = str(title).strip()
                if title:
                    obj, created = BreakdownCategory.objects.get_or_create(
                        name=title,
                        defaults={'description': f'Imported from Excel - {title}', 'active': True}
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Created: {title}"))
                    else:
                        existing_count += 1
                        self.stdout.write(f"Already exists: {title}")

            self.stdout.write(self.style.SUCCESS(
                f"\nImport complete! Created: {created_count}, Already existed: {existing_count}"
            ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
