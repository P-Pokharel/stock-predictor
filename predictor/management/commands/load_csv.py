import os
import csv
from django.core.management.base import BaseCommand
from predictor.models import StockData

class Command(BaseCommand):
    help = 'Load stock data from all CSV files in the folder'

    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str)

    def handle(self, *args, **kwargs):
        folder_path = kwargs['folder_path']

        if not os.path.isdir(folder_path):
            self.stderr.write(self.style.ERROR(f"'{folder_path}' is not a valid directory"))
            return
        
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):  
                file_path = os.path.join(folder_path, filename)
                self.stdout.write(self.style.NOTICE(f"Processing {file_path}..."))

                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            
                            obj, created = StockData.objects.get_or_create(
                                symbol=row['Symbol'],
                                date=row['Date'],
                                defaults={
                                    'open_price': row['Open'],
                                    'close_price': row['Close'],
                                    'high': row['High'],
                                    'low': row['Low'],
                                    'volume': row['Volume'].replace(',', ''),
                                    'percent_change': row['Percent Change'].replace('%', '')
                                }
                            )

                            if created:
                                self.stdout.write(self.style.SUCCESS(f"Added: {obj}"))

                        except Exception as e:
                            self.stderr.write(self.style.ERROR(f"Error processing row: {row}. Error: {e}"))

                self.stdout.write(self.style.SUCCESS(f"Data from {filename} processed successfully!"))
