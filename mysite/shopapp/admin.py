from io import TextIOWrapper
from django.contrib import admin

from .common import save_csv_products
from .models import Product, Order, ProductImage
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm
from django.shortcuts import render, redirect
from django.urls import path


class OrderInLine(admin.TabularInline):
    model = Product.orders.through


class ProductInLine(admin.StackedInline):
    model = ProductImage


@admin.action(description='Archived products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Rearchived products')
def remark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = 'shopapp/products_changelist.html'
    actions = [
        mark_archived, remark_archived, 'export_csv',
    ]
    inlines = [
        OrderInLine, ProductInLine
    ]
    #list_display = 'pk', 'name', 'description', 'price', 'discount'
    list_display = 'pk', 'name', 'description_short', 'price', 'discount_short', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'description'
    fieldsets = [
        ('Main', {
            'fields': ('name', 'description')
        }), ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse'),
        }),
        ('Images', {
            'fields': ('preview',),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archived" is for soft delete',
        })
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 10:
            return obj.description
        return obj.description[:10] + '...'

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)
        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding
        )
        # reader = DictReader(csv_file)
        # products = [
        #     Product(**row) for row in reader
        # ]
        # Product.objects.bulk_create(products)
        save_csv_products(file=form.files['csv_file'].file, encoding=request.encoding)
        self.message_user(request, 'Data from CSV was imported')
        return redirect('..')


    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-products-csv/',
                self.import_csv,
                name='import_products_csv'
            )
        ]
        return new_urls + urls


#admin.site.register(Product, ProductAdmin)


class ProductInLine(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'
    inlines = [
        ProductInLine,
    ]

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

