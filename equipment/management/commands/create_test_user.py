from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Create a test user for development'

    def handle(self, *args, **kwargs):
        username = 'testuser'
        password = 'testpass123'
        email = 'test@example.com'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists'))
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            self.stdout.write(self.style.SUCCESS(f'Successfully created user "{username}"'))
        
        token, created = Token.objects.get_or_create(user=user)
        
        self.stdout.write(self.style.SUCCESS(f'\nLogin credentials:'))
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Token: {token.key}')
