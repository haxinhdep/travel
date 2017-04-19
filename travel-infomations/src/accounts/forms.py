from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Tên đăng nhập')
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
       
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Người dùng không tồn tại")
            if not user.check_password(password):
                raise forms.ValidationError("Mật khẩu không đúng !")
            if not user.is_active:
                raise forms.ValidationError("Người dùng này không còn hoạt động")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Tên đăng nhập')
    first_name = forms.CharField(label='Họ')
    last_name = forms.CharField(label='Tên hiển thị')
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    email = forms.EmailField(label='Địa chỉ email')
    email2 = forms.EmailField(label='Nhập lại email')
    type_customers = (
        ("customer", "Khách hàng"),
        ("partner", "Đối tác")
    )
    type = forms.ChoiceField(choices=type_customers, label='Loại khách hàng')
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'email2',
            'password',
            'type'
        ]

    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get('email')
    #     email2 = self.cleaned_data.get('email2')
    #     if email != email2:
    #         raise forms.ValidationError("Emails must match")
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError("This email has already been registered")

    #     return super(UserRegisterForm,self).clean(*args, **kwargs)

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Email phải trùng")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email đã đng ký.")
        return email














