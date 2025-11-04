"""
Formularios para la gestión de autenticación y usuarios
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, UserRole


class UserLoginForm(forms.Form):
    """
    Formulario para inicio de sesión
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario o correo electrónico',
            'id': 'login-username',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'login-password',
            'autocomplete': 'current-password',
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'remember-me',
        })
    )


class UserRegistrationForm(UserCreationForm):
    """
    Formulario para registro de nuevos usuarios
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'id': 'register-email',
            'autocomplete': 'email',
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre',
            'id': 'register-first-name',
            'autocomplete': 'given-name',
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido',
            'id': 'register-last-name',
            'autocomplete': 'family-name',
        })
    )
    phone_number = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+573001234567',
            'id': 'register-phone',
            'autocomplete': 'tel',
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario',
                'id': 'register-username',
                'autocomplete': 'username',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'register-password1',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'id': 'register-password2',
            'autocomplete': 'new-password',
        })
    
    def clean_email(self):
        """Validar que el email sea único"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email
    
    def clean_username(self):
        """Validar que el username sea único"""
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return username
    
    def save(self, commit=True):
        """Guardar el usuario con los datos adicionales"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Formulario para editar el perfil del usuario"""
    
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña actual (opcional)'
        }),
        label='Contraseña Actual'
    )
    
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña (opcional)'
        }),
        label='Nueva Contraseña'
    )
    
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña'
        }),
        label='Confirmar Contraseña'
    )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'bio', 'avatar', 'address', 'city', 'country', 'postal_code']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+57 300 123 4567'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Cuéntanos sobre ti...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'País'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código Postal'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password or confirm_password:
            if not current_password:
                raise forms.ValidationError('Debe ingresar su contraseña actual para cambiarla.')
            
            if new_password != confirm_password:
                raise forms.ValidationError('Las contraseñas nuevas no coinciden.')
            
            if not self.instance.check_password(current_password):
                raise forms.ValidationError('La contraseña actual es incorrecta.')
            
            # Verificar que la nueva contraseña sea diferente de la actual
            if self.instance.check_password(new_password):
                raise forms.ValidationError('La nueva contraseña debe ser diferente a la contraseña actual.')
        
        return cleaned_data


class UserRoleAssignmentForm(forms.Form):
    """
    Formulario para asignar roles a usuarios (solo administradores)
    """
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    role = forms.ModelChoiceField(
        queryset=UserRole.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )


class ChangePasswordForm(forms.Form):
    """
    Formulario para cambiar contraseña desde el perfil del usuario
    Requiere contraseña actual y cierra la sesión después del cambio
    """
    current_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña actual',
            'id': 'current-password',
            'autocomplete': 'current-password',
        }),
        label='Contraseña Actual'
    )
    
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña',
            'id': 'new-password',
            'autocomplete': 'new-password',
        }),
        label='Nueva Contraseña',
        help_text='Debe tener 8-20 caracteres, mayúsculas, minúsculas y caracteres especiales.'
    )
    
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña',
            'id': 'confirm-password',
            'autocomplete': 'new-password',
        }),
        label='Confirmar Nueva Contraseña'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        """Validar que la contraseña actual sea correcta"""
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise ValidationError('La contraseña actual es incorrecta.')
        return current_password
    
    def clean_new_password(self):
        """Validar que la nueva contraseña cumpla con todos los requisitos"""
        new_password = self.cleaned_data.get('new_password')
        
        # Validar con los validadores configurados en Django
        from django.contrib.auth.password_validation import validate_password
        try:
            validate_password(new_password, self.user)
        except ValidationError as e:
            # Re-lanzar los errores de validación
            raise ValidationError(e.messages) from e
        
        return new_password
    
    def clean(self):
        """Validar que las contraseñas coincidan y sean diferentes"""
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError('Las contraseñas nuevas no coinciden.')
            
            # Verificar que la nueva contraseña sea diferente de la actual
            if current_password and self.user.check_password(new_password):
                raise ValidationError('La nueva contraseña debe ser diferente a la contraseña actual.')
        
        return cleaned_data
