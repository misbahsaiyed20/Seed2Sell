from django import forms
from django.core.exceptions import ValidationError
from .models import Product


# ================= PRODUCT FORM =================
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'name',
            'cost_price',
            'price',
            'image',
            'description',
            'category',
            'is_bestseller',
            'unit',
        ]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Product name must be at least 3 characters.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Selling price must be greater than 0.")
        return price

    def clean_cost_price(self):
        cost_price = self.cleaned_data.get('cost_price')
        if cost_price < 0:
            raise forms.ValidationError("Cost price cannot be negative.")
        return cost_price

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        cost_price = cleaned_data.get('cost_price')
        if price and cost_price:
            if price < cost_price:
                raise forms.ValidationError(
                    "Selling price cannot be less than cost price."
                )
        return cleaned_data


# ================= SIGNUP FORM =================
class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    role = forms.ChoiceField(
        choices=[('customer', 'Customer'), ('farmer', 'Farmer')],
        required=True
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Import here to avoid circular import
        from accounts.models import CustomUser
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            raise ValidationError("Phone must contain only digits.")
        if len(phone) != 10:
            raise ValidationError("Phone must be exactly 10 digits.")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data