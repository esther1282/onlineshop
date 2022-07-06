# admin / gotshop123!
from django import forms
from django.contrib import admin
from .models import Category, Product, ProductImage
from django.core.exceptions import ValidationError

class ProductAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'] = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Product
        exclude = ('deleted_at', )

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock<0 or stock>999:
            raise forms.ValidationError("stock: only 0 ~ 999")
        return stock

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Check Price again please")
        return price


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    add_form_template = 'admin/post_form.html'

    def get_form(self, request, obj=None, **kwargs):
        try:
            instance = kwargs['instance']
            return ProductAdminForm(instance=instance)
        except KeyError:
            return ProductAdminForm

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = self.get_form(request)
        return super(ProductAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        post = Product.objects.get(id=object_id)
        extra_context["form"] = self.get_form(instance=post, request=request)
        return super(ProductAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
            images = request.FILES.getlist('images')
            for image in images:
                if ProductImage.objects.filter(product=obj).exists():
                    ProductImage.objects.create(product=obj, image=image)
                else:
                    ProductImage.objects.create(product=obj, image=image, is_represent=True)
            return super().save_model(request, obj, form, change)
        except:
            raise forms.ValidationError("Here")


class ProductImageAdminForm(forms.ModelForm):

    class Meta:
        model = ProductImage
        fields = '__all__'

    def clean_is_represent(self):
        product = self.cleaned_data['product']
        is_represent = self.cleaned_data['is_represent']
        if is_represent:
            if ProductImage.objects.filter(product=product, is_represent=True).exists():
                raise forms.ValidationError("Represent image already exists.")
        return is_represent


class ProductImageAdmin(admin.ModelAdmin):
    form = ProductImageAdminForm


admin.site.register(Category)
admin.site.register(ProductImage, ProductImageAdmin)
#admin.site.register(Product)
