from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a new CMS user with appropriate permissions'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new user')
        parser.add_argument('email', type=str, help='Email for the new user')
        parser.add_argument('--password', type=str, help='Password for the new user (will prompt if not provided)')
        parser.add_argument('--staff', action='store_true', help='Make user a staff member')
        parser.add_argument('--superuser', action='store_true', help='Make user a superuser')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        is_staff = options['staff']
        is_superuser = options['superuser']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'User "{username}" already exists.')
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'User with email "{email}" already exists.')
            )
            return

        # Prompt for password if not provided
        if not password:
            password = input('Enter password: ')
            password_confirm = input('Confirm password: ')
            if password != password_confirm:
                self.stdout.write(
                    self.style.ERROR('Passwords do not match.')
                )
                return

        try:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created user "{username}"')
            )
            
            if is_superuser:
                self.stdout.write(
                    self.style.WARNING('User has superuser privileges')
                )
            elif is_staff:
                self.stdout.write(
                    self.style.WARNING('User has staff privileges')
                )
                
        except ValidationError as e:
            self.stdout.write(
                self.style.ERROR(f'Validation error: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating user: {e}')
            ) 