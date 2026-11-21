
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.password_validation import validate_password
from .models import User


class CustomUserCreationForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password, self.instance)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        "user_id",
        "email",
        "first_name",
        "last_name",
        "created_at",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("user_id",)

    readonly_fields = (
        "user_id",
        "created_at",
    )

    fieldsets = (
        ("User Information", {
            "fields": (
                "user_id",
                "email",
                "password",
                "first_name",
                "last_name",
                "created_at",
            )
        }),
    )

    add_fieldsets = (
        ("Create User", {
            "classes": ("wide",),
            "fields": (
                "email",
                "password",
            ),
        }),
    )
