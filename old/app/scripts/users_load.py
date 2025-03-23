import csv
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

def run():
    file_path = "model/users.csv"
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=";")
        #next(reader)  # Skip the header row

        User.objects.all().delete()  # Optional: Clear existing users

        for row in reader:
            username = row[0].strip()
            password = row[1].strip()

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password=password,  # This will hash the password
                )
                user.save()
