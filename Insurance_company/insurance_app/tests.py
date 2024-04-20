from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from datetime import date, timedelta

from insurance_app.models import CarPolicyType, HousePolicyType, CarInsurance, HouseInsurance, CarPolicyFactors, HousePolicyFactors
from insurance_app.forms import CarInsuranceModelForm, HouseInsuranceModelForm
from insurance_app.logic_temp import PolicyPriceCalculator, HousePolicyPriceCalculator
from accounts.models import Customer

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test_user', first_name='John', last_name='Doe')
        self.customer = Customer.objects.create(user=self.user)
        self.valid_date = date.today() + timedelta(days=7)

        self.car_policy_type = CarPolicyType.objects.create(
            policy_type='Car Test Policy',
            policy_description='Car Test Policy Description',
            type_factor=1.0
        )

        self.house_policy_type = HousePolicyType.objects.create(
            policy_type='House Test Policy',
            policy_description='House Test Policy Description',
            type_factor=1.0
        )

        self.car_policy_factors = CarPolicyFactors.objects.create(
            base=600,
            age_factor=0.1,
            mileage_factor_1=0.002,
            mileage_factor_2=0.003,
            mileage_factor_3=0.004,
            avg_year_mileage_1=0.05,
            avg_year_mileage_2=0.07,
            avg_year_mileage_3=0.09,
            avg_year_mileage_4=0.1,
            rented_factor_1=1,
            rented_factor_2=3,
            owners_factor_1=1,
            owners_factor_2=1.2,
            owners_factor_3=1.8,
            owners_factor_4=2
        )

        self.house_policy_factors = HousePolicyFactors.objects.create(
            base=600,
            house_area_factor_1=1.5,
            house_area_factor_2=1.8,
            house_area_factor_3=2,
            house_owners_factor_1=1,
            house_owners_factor_2=1.2,
            house_owners_factor_3=1.8,
            house_owners_factor_4=2,
            house_value_factor_1=1,
            house_value_factor_2=1.2,
            house_value_factor_3=1.8,
            house_value_factor_4=2
        )

class InsuranceModelTestCase(BaseTestCase):
    def test_car_insurance_creation(self):
        car_insurance = CarInsurance.objects.create(
            policy_type=self.car_policy_type,
            customer=self.customer,
            valid_to=self.valid_date,
            price=600.00,
            car_mark_model='Toyota Corolla',
            production_year=2022,
            fuel_type='Gasoline',
            mileage=50000,
            average_year_mileage=3,
            is_rented=False,
            number_of_owners=1,
            driver_under_26=False
        )

        self.assertEqual(car_insurance.customer, self.customer)
        self.assertEqual(car_insurance.policy_type, self.car_policy_type)
        self.assertEqual(car_insurance.valid_to, self.valid_date)

    def test_house_insurance_creation(self):
        house_insurance = HouseInsurance.objects.create(
            policy_type=self.house_policy_type,
            customer=self.customer,
            valid_to=self.valid_date,
            price=600.00,
            house_type='Dom',
            number_of_owners=1,
            house_area=150,
            house_city='Test City',
            house_value=200000.00
        )

        self.assertEqual(house_insurance.customer, self.customer)
        self.assertEqual(house_insurance.policy_type, self.house_policy_type)
        self.assertEqual(house_insurance.valid_to, self.valid_date)


class CarDataFormValidation(BaseTestCase):
    def test_correct_car_data(self):
        form_data = {
            'policy_type': self.car_policy_type,
            'valid_to': date.today() + timedelta(days=7),
            'car_mark_model': 'Toyota Corolla',
            'production_year': 2022,
            'fuel_type': 'Gasoline',
            'mileage': 50000,
            'average_year_mileage': 3,
            'is_rented': False,
            'number_of_owners': 1,
            'driver_under_26': False
        }

        form = CarInsuranceModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_car_data(self):
        form_data = {
            'policy_type': self.house_policy_type,
            'valid_to': date.today() - timedelta(days=7),  # wrong date
            'car_mark_model': 'Toyota Corolla',
            'production_year': 2099,  # wrong date
            'fuel_type': 'Gasoline',
            'mileage': 50000,
            'average_year_mileage': 3,
            'is_rented': False,
            'number_of_owners': 1,
            'driver_under_26': False
        }

        form = CarInsuranceModelForm(data=form_data)
        self.assertFalse(form.is_valid())


class HouseDataFormValidation(BaseTestCase):
    def test_correct_house_data(self):
        form_data = {
            'policy_type': self.house_policy_type,
            'valid_to': date.today() + timedelta(days=7),
            'house_type': 'Dom',
            'number_of_owners': 1,
            'house_area': 150,
            'house_city': 'Test City',
            'house_value': 200000.00
        }

        form = HouseInsuranceModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_house_data(self):
        form_data = {
            'policy_type': self.house_policy_type,
            'valid_to': 'last Tuesday',
            'house_type': 'The palatial estate of his royal majesty',
            'number_of_owners': -1,
            'house_area': 150000000,
            'house_city': 'Test City',
            'house_value': 200000.00
        }

        form = HouseInsuranceModelForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestPolicyPriceCalculator(BaseTestCase):
    def test_car_policy_price_calculation(self):
        calculator = PolicyPriceCalculator(
            production_year=2022,
            fuel_factor=1.2,
            fuel_type='Gasoline',
            mileage=50000,
            average_year_mileage=3,
            is_rented=False,
            number_of_owners=1,
            policy_type=self.car_policy_type.policy_type
        )
        expected_price = 1200.02
        self.assertAlmostEqual(calculator.calculate_price(), expected_price, places=2)

    def test_house_policy_price_calculation(self):
        calculator = HousePolicyPriceCalculator(
            house_type='Dom',
            number_of_owners=1,
            house_area=150,
            house_value=200000,
            policy_type=self.house_policy_type.policy_type
        )
        expected_price = 222.0
        self.assertAlmostEqual(calculator.calculate_price(), expected_price, places=2)


class MainPageViewTest(TestCase):
    def test_main_page_view(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')


class PolicyListViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.car_insurance = CarInsurance.objects.create(
            customer=self.customer,
            policy_type=self.car_policy_type,
            valid_to='2024-05-01',
            price=600.00,
            car_mark_model='Toyota Corolla',
            production_year=2022,
            fuel_type='Gasoline',
            mileage=50000,
            average_year_mileage=3,
            is_rented=False,
            number_of_owners=1,
            driver_under_26=False
        )

        self.house_insurance = HouseInsurance.objects.create(
            customer=self.customer,
            policy_type=self.house_policy_type,
            valid_to='2024-05-01',
            price=600.00,
            house_type='Dom',
            number_of_owners=1,
            house_area=150,
            house_city='Test City',
            house_value=200000.00
        )

    def test_policy_list_view(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        response = self.client.get(reverse('policy_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'policy_list.html')

    def test_policy_list_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('policy_list'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=/insurance_app/policy_list/')

class PolicyCarCreateViewTest(BaseTestCase):

    def test_get_request(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('policy_car_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'policy_car_create.html')

    def test_post_valid_form(self):
        self.client.force_login(self.user)
        data = {
            'policy_type': self.car_policy_type.pk,
            'valid_to': self.valid_date,
            'car_mark_model': 'Toyota Corolla',
            'production_year': 2020,
            'fuel_type': 'Gasoline',
            'mileage': 50000,
            'average_year_mileage': 2,
            'is_rented': False,
            'number_of_owners': 1,
            'driver_under_26': False
        }
        response = self.client.post(reverse('policy_car_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('policy_car_confirm'))

    def test_post_invalid_form(self):
        self.client.force_login(self.user)
        data = {
            'policy_type': self.car_policy_type.pk,
            'valid_to': '2020-01-01',
            'car_mark_model': 'Toyota Corolla',
            'production_year': 2030,
            'fuel_type': 'Gasoline',
            'mileage': 50000,
            'average_year_mileage': 2,
            'is_rented': False,
            'number_of_owners': 1,
            'driver_under_26': False
        }
        response = self.client.post(reverse('policy_car_create'), data)
        form = response.context['car_policy_form']
        self.assertEqual(response.status_code, 200)
        self.assertFormError(form, 'valid_to', 'The date must be in the future.')
        self.assertFormError(form, 'production_year', 'You must choose a present or past year.')


