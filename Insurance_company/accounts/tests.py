from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.urls import reverse

from accounts.models import Customer
from accounts.forms import CustomUserForm, CustomerForm

User = get_user_model()


class CustomerPeselTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', first_name='John', last_name='Doe')

    # Ensure that valid PESEL passes validation
    def test_valid_pesel(self):
        valid_pesel = '44051401458'
        customer = Customer.objects.create(user=self.user, pesel=valid_pesel)
        self.assertIsNone(customer.clean())

    # Ensure that invalid PESEL with valid checksum raises ValidationError
    def test_invalid_pesel_with_valid_checksum(self):
        invalid_pesel_with_valid_checksum = '22222222222'
        customer = Customer(user=self.user, pesel=invalid_pesel_with_valid_checksum)
        with self.assertRaises(ValidationError):
            customer.full_clean()

    # Ensure that PESEL with invalid checksum raises ValidationError
    def test_invalid_pesel_with_invalid_checksum(self):
        invalid_pesel_with_invalid_checksum = '12345678900'
        customer = Customer(user=self.user, pesel=invalid_pesel_with_invalid_checksum)
        with self.assertRaises(ValidationError):
            customer.full_clean()


class UserDataTestCase(TestCase):
    def test_correct_user_data(self):
        valid_user_data = {
            'username': 'test_user',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        valid_customer_data = {
            'pesel': '44051401458',
            'address': 'Test City',
            'phone_number': '123456789',
            'privacy_policy_accepted': True,
            'marketing_agreement': False
        }

        user_form = CustomUserForm(data=valid_user_data)
        customer_form = CustomerForm(data=valid_customer_data)
        self.assertTrue(user_form.is_valid() and customer_form.is_valid())

    def test_invalid_user_data(self):
        invalid_user_data = {
            # Invalid because first_name is missing
            'username': 'test_user',
            'last_name': 'Doe',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        invalid_customer_data = {
            # Invalid because pesel is too short
            'pesel': '123',
            'address': 'Test City',
            'phone_number': '123456789',
            'privacy_policy_accepted': True,
            'marketing_agreement': False
        }

        user_form = CustomUserForm(data=invalid_user_data)
        customer_form = CustomerForm(data=invalid_customer_data)
        self.assertFalse(user_form.is_valid() and customer_form.is_valid())


class RegisterViewTest(TestCase):
    def setUp(self):
        # Client() allows us to simulate GET and POST requests
        self.client = Client()
        self.register_url = reverse('register')

    def test_get_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['user_form'], CustomUserForm)
        self.assertIsInstance(response.context['customer_form'], CustomerForm)

    def test_post_valid_data(self):
        data = {
            'username': 'test_user',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'test_password',
            'password2': 'test_password',
            'pesel': '44051401458',
            'address': 'Test City',
            'phone_number': '123456789',
            'privacy_policy_accepted': True,
            'marketing_agreement': False
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # 302 being the code for redirect
        self.assertRedirects(response, reverse('login'))

        self.assertTrue(User.objects.filter(username='test_user').exists())
        self.assertTrue(Customer.objects.filter(user__username='test_user').exists())

    def test_post_invalid_data(self):
        data = {
            'username': '',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'test_password',
            'password2': 'test_password',
            'pesel': '123',
            'address': 'Test City',
            'phone_number': '123456789',
            'privacy_policy_accepted': True,
            'marketing_agreement': False
        }
        response = self.client.post(self.register_url, data)
        # 200 being the code for success - because register.html is rendered again in case of incorrect data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

        self.assertFormError(response.context['user_form'], 'username', 'This field is required.')
        self.assertFormError(response.context['customer_form'], 'pesel', 'PESEL must contain 11 digits.')


class CustomerCreationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            first_name='John',
            last_name='Doe',
            password='test_password'
        )
        self.customer_data = {
            'pesel': '44051401458',
            'address': 'Test City',
            'phone_number': '123456789',
            'privacy_policy_accepted': True,
            'marketing_agreement': False
        }

    def test_customer_creation(self):
        self.customer = Customer.objects.create(
            user=self.user,
            **self.customer_data
        )

        created_customer = Customer.objects.get(user=self.user)

        self.assertEqual(created_customer.pesel, self.customer_data['pesel'])
        self.assertEqual(created_customer.address, self.customer_data['address'])
        self.assertEqual(created_customer.phone_number, self.customer_data['phone_number'])
        self.assertEqual(created_customer.privacy_policy_accepted, self.customer_data['privacy_policy_accepted'])
        self.assertEqual(created_customer.marketing_agreement, self.customer_data['marketing_agreement'])
        self.assertEqual(str(created_customer), f"Customer profile of {self.user.username}")


class CustomerDetailViewTest(TestCase):
    def setUp(self):
        # This will create our test customer and their details site
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            first_name='John',
            last_name='Doe',
            password='test_password'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            pesel='44051401458',
            address='Test City',
            phone_number='123456789',
            privacy_policy_accepted=True,
            marketing_agreement=False
        )
        self.detail_url = reverse('customer_detail', args=[self.customer.pk])

    def test_get_customer_detail_authenticated(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/customer_detail.html')
        self.assertEqual(response.context['customer'], self.customer)

    def test_get_customer_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')

    def test_get_customer_detail_different_user(self):
        self.another_user = User.objects.create_user(
            username='another_test_user',
            first_name='Jane',
            last_name='Doe',
            password='test_password'
        )
        self.another_customer = Customer.objects.create(
            user=self.another_user,
            pesel='44051401459',
            address='Another Test City',
            phone_number='987654321',
            privacy_policy_accepted=True,
            marketing_agreement=False
        )

        self.client.login(username='another_test_user', password='test_password')
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')


class CustomerUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            first_name='John',
            last_name='Doe',
            password='test_password'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            pesel='44051401458',
            address='Test City',
            phone_number='123456789',
            privacy_policy_accepted=True,
            marketing_agreement=False
        )
        self.update_url = reverse('customer_update', args=[self.customer.pk])

    def test_get_customer_update_authenticated(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/customer_update.html')
        self.assertIsInstance(response.context['form'], CustomerForm)
        self.assertEqual(response.context['customer'], self.customer)

    def test_get_customer_update_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')

    def test_get_customer_update_different_user(self):
        self.another_user = User.objects.create_user(
            username='another_test_user',
            first_name='Jane',
            last_name='Doe',
            password='test_password'
        )
        self.another_customer = Customer.objects.create(
            user=self.another_user,
            pesel='44051401459',
            address='Another Test City',
            phone_number='987654321',
            privacy_policy_accepted=True,
            marketing_agreement=False
        )

        self.client.login(username='another_test_user', password='test_password')
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')

    def test_post_customer_update_valid_data(self):
        self.client.login(username='test_user', password='test_password')
        data = {
            'pesel': '44051401458',
            'address': 'Updated City',
            'phone_number': '123456789',
            'privacy_policy_accepted': True,
            'marketing_agreement': False
        }
        response = self.client.post(self.update_url, data)

        self.assertRedirects(response, reverse('customer_detail', args=[self.customer.pk]))
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.pesel, data['pesel'])
        self.assertEqual(self.customer.address, data['address'])
        self.assertEqual(self.customer.phone_number, data['phone_number'])
        self.assertEqual(self.customer.privacy_policy_accepted, data['privacy_policy_accepted'])
        self.assertEqual(self.customer.marketing_agreement, data['marketing_agreement'])

class CustomerPasswordChangeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            first_name='John',
            last_name='Doe',
            password='test_password'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            pesel='44051401458',
            address='Test City',
            phone_number='123456789',
            privacy_policy_accepted=True,
            marketing_agreement=False
        )
        self.password_change_url = reverse('password_change', args=[self.customer.pk])

    def test_get_customer_password_change_authenticated(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(self.password_change_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_change.html')
        self.assertIsInstance(response.context['form'], SetPasswordForm)

    def test_get_customer_password_change_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.password_change_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')

    def test_get_customer_password_change_different_user(self):
        self.another_user = User.objects.create_user(
            username='another_test_user',
            first_name='Jane',
            last_name='Doe',
            password='test_password'
        )
        self.another_customer = Customer.objects.create(
            user=self.another_user,
            pesel='44051401459',
            address='Another Test City',
            phone_number='987654321',
            privacy_policy_accepted=True,
            marketing_agreement=False
        )

        self.client.login(username='another_test_user', password='test_password')
        response = self.client.get(self.password_change_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')

    def test_post_customer_password_change_valid_data(self):
        self.client.login(username='test_user', password='test_password')
        data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        }
        response = self.client.post(self.password_change_url, data)

        self.assertRedirects(response, reverse('login'))