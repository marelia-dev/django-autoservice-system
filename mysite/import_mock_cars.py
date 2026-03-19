# import_mock_cars.py
# -*- coding: utf-8 -*-

import os
import sys
import csv
import django

# Django nustatymas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from autoservice.models import Car


def import_cars_from_csv(csv_file_path):
    """
    import automobiliu is CSV failo Mockaroo
    """
    created = 0
    skipped = 0

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # tikrinam pavadinimus
        expected_fields = {'make', 'model', 'license_plate', 'vin_code', 'client_name'}
        if not expected_fields.issubset(reader.fieldnames):
            print("Klaida: CSV faile truksta reikalingi stulpeliai!")
            print("Laukiami:", expected_fields)
            print("Rasta:", reader.fieldnames)
            return

        cars_to_create = []

        for row in reader:
            try:
                # Проверяем уникальность license_plate и vin_code
                if Car.objects.filter(license_plate=row['license_plate']).exists():
                    skipped += 1
                    print(f"Praleistas (license_plate jau egzistuoja): {row['license_plate']}")
                    continue

                car = Car(
                    make=row['make'],
                    model=row['model'],
                    license_plate=row['license_plate'],
                    vin_code=row['vin_code'] if row['vin_code'] else None,
                    client_name=row['client_name']
                )
                cars_to_create.append(car)
                created += 1

            except Exception as e:
                print(f"Klaida eiluteje: {row}")
                print(e)
                skipped += 1

        # masinis irasymas
        Car.objects.bulk_create(cars_to_create, ignore_conflicts=True)

        print(f"\nImporto pabaiga:")
        print(f"Sukurta: {created}")
        print(f"Praleista (dubliai arba klaidos): {skipped}")
        print(f"Viso apdorota: {created + skipped}")


if __name__ == '__main__':
    # failo kelias
    csv_path = os.path.join(BASE_DIR, 'data', 'mock_cars.csv')
    import_cars_from_csv(csv_path)