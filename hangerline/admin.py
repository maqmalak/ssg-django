from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Count, Sum
from datetime import datetime
from django import forms
from .models import (
    Article, HangerlineEmp, OperatorDailyPerformance,
    QualityControlRepair,
    Loadinginformation, Operationinformation,
    Stylebasicinformation, EtlExtractLog, EtlQcrExtractLog,
    Size, Color, Style, LineTarget, LineTargetDetail, BreakdownCategory, Breakdown, ClientPurchaseOrder,
    TransferToPacking
)


class LineTargetDetailForm(forms.ModelForm):
    class Meta:
        model = LineTargetDetail
        fields = '__all__'


class ProductionFilter(admin.SimpleListFilter):
    title = _('Production')
    parameter_name = 'production'

    def lookups(self, request, model_admin):
        # Start with base queryset
        queryset = OperatorDailyPerformance.objects.all()

        # Apply any active date filters
        if 'odp_date__gte' in request.GET:
            queryset = queryset.filter(odp_date__gte=request.GET['odp_date__gte'])
        if 'odp_date__lte' in request.GET:
            queryset = queryset.filter(odp_date__lte=request.GET['odp_date__lte'])
        if 'odp_date__year' in request.GET:
            queryset = queryset.filter(odp_date__year=request.GET['odp_date__year'])
        if 'odp_date__month' in request.GET:
            queryset = queryset.filter(odp_date__month=request.GET['odp_date__month'])
        if 'odp_date__day' in request.GET:
            queryset = queryset.filter(odp_date__day=request.GET['odp_date__day'])

        # Calculate sums for each production category
        categories = []

        # Offline
        offline_qty = queryset.filter(oc_description='Garment Insert in Poly Bag & Close').aggregate(
            total=Sum('odpd_quantity'))['total'] or 0
        categories.append(('offline', f"{_('Offline')} (Quantity: {offline_qty})"))

        # Loading
        loading_qty = queryset.filter(oc_description='Loading/Panel Segregation').aggregate(
            total=Sum('odpd_quantity'))['total'] or 0
        categories.append(('loading', f"{_('Loading')} (Quantity: {loading_qty})"))

        # Midline
        midline_qty = queryset.filter(oc_description__icontains='midline').aggregate(
            total=Sum('odpd_quantity'))['total'] or 0
        categories.append(('midline', f"{_('QC(midline)')} (Quantity: {midline_qty})"))

        # Endline
        endline_qty = queryset.filter(oc_description__icontains='endline').aggregate(
            total=Sum('odpd_quantity'))['total'] or 0
        categories.append(('endline', f"{_('QC(endline)')} (Quantity: {endline_qty})"))

        # Final
        final_qty = queryset.filter(oc_description__icontains='final').aggregate(
            total=Sum('odpd_quantity'))['total'] or 0
        categories.append(('final', f"{_('QC(final)')} (Quantity: {final_qty})"))

        # QC
        qc_qty = queryset.filter(oc_description__startswith='QC').aggregate(
            total=Sum('odpd_quantity'))['total'] or 0
        categories.append(('qc', f"{_('QC')} (Quantity: {qc_qty})"))

        # Selected (all)
        selected_qty = queryset.aggregate(total=Sum('odpd_quantity'))['total'] or 0
        categories.append(('selected', f"{_('Selected')} (Quantity: {selected_qty})"))

        return categories

    def queryset(self, request, queryset):
        if self.value() == 'offline':
            return queryset.filter(oc_description='Garment Insert in Poly Bag & Close')
        elif self.value() == 'loading':
            return queryset.filter(oc_description='Loading/Panel Segregation')
        elif self.value() == 'midline':
            # --------replace equal  with like '%midline%' in below line--------
            return queryset.filter(oc_description__icontains='midline')
        elif self.value() == 'endline':
            # --------replace equal  with like '%endline%' in below line--------
            return queryset.filter(oc_description__icontains='endline')
        elif self.value() == 'final':
            # --------replace equal  with like '%final%' in below line--------
            return queryset.filter(oc_description__icontains='final')
        elif self.value() == 'qc':  
             # --------replace equal  with start with 'qc%' in below line--------  

            return queryset.filter(oc_description__startswith='QC')
        elif self.value() == 'selected':
            return queryset.all()
        return queryset


class QcscDescriptionFilter(admin.SimpleListFilter):
    title = _('QCSC Description')
    parameter_name = 'qcsc_description'

    def lookups(self, request, model_admin):
        # Start with base queryset
        queryset = QualityControlRepair.objects.all()

        # Apply any active date filters
        if 'qcr_date__gte' in request.GET:
            queryset = queryset.filter(qcr_date__gte=request.GET['qcr_date__gte'])
        if 'qcr_date__lte' in request.GET:
            queryset = queryset.filter(qcr_date__lte=request.GET['qcr_date__lte'])
        if 'qcr_date__year' in request.GET:
            queryset = queryset.filter(qcr_date__year=request.GET['qcr_date__year'])
        if 'qcr_date__month' in request.GET:
            queryset = queryset.filter(qcr_date__month=request.GET['qcr_date__month'])
        if 'qcr_date__day' in request.GET:
            queryset = queryset.filter(qcr_date__day=request.GET['qcr_date__day'])

        # Get distinct qcsc_description values with counts, sorted by count descending
        descriptions = (
            queryset
            .values('qcsc_description')
            .exclude(qcsc_description__isnull=True)
            .exclude(qcsc_description='')
            .annotate(count=Count('qcsc_description'))
            .order_by('-count')
        )

        return [
            (desc['qcsc_description'], f"{desc['qcsc_description']} ({desc['count']})")
            for desc in descriptions
        ]

    def queryset(self, request, queryset):
        if self.value():
            current_year = datetime.now().year
            return queryset.filter(qcsc_description=self.value(), qcr_date__year=current_year)
        return queryset


class SourceConnectionFilter(admin.SimpleListFilter):
    title = _('Source Connection')
    parameter_name = 'source_connection'

    def lookups(self, request, model_admin):
        # Start with base queryset
        queryset = OperatorDailyPerformance.objects.all()

        # Apply any active date filters
        if 'odp_date__gte' in request.GET:
            queryset = queryset.filter(odp_date__gte=request.GET['odp_date__gte'])
        if 'odp_date__lte' in request.GET:
            queryset = queryset.filter(odp_date__lte=request.GET['odp_date__lte'])
        if 'odp_date__year' in request.GET:
            queryset = queryset.filter(odp_date__year=request.GET['odp_date__year'])
        if 'odp_date__month' in request.GET:
            queryset = queryset.filter(odp_date__month=request.GET['odp_date__month'])
        if 'odp_date__day' in request.GET:
            queryset = queryset.filter(odp_date__day=request.GET['odp_date__day'])

        # Get distinct source_connection values with aggregated loading/unloading sums
        connections = (
            queryset
            .values('source_connection')
            .exclude(source_connection__isnull=True)
            .exclude(source_connection='')
            .annotate(
                total_loading=Sum('loading_qty'),
                total_unloading=Sum('unloading_qty')
            )
            .order_by('source_connection')
        )

        return [
            (conn['source_connection'],
             f"{conn['source_connection']} (on: {conn['total_loading'] or 0}, off: {conn['total_unloading'] or 0})")
            for conn in connections
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(source_connection=self.value())
        return queryset


class ShiftFilter(admin.SimpleListFilter):
    title = _('Shift')
    parameter_name = 'shift'

    def lookups(self, request, model_admin):
        # Start with base queryset
        queryset = OperatorDailyPerformance.objects.all()

        # Apply any active date filters
        if 'odp_date__gte' in request.GET:
            queryset = queryset.filter(odp_date__gte=request.GET['odp_date__gte'])
        if 'odp_date__lte' in request.GET:
            queryset = queryset.filter(odp_date__lte=request.GET['odp_date__lte'])
        if 'odp_date__year' in request.GET:
            queryset = queryset.filter(odp_date__year=request.GET['odp_date__year'])
        if 'odp_date__month' in request.GET:
            queryset = queryset.filter(odp_date__month=request.GET['odp_date__month'])
        if 'odp_date__day' in request.GET:
            queryset = queryset.filter(odp_date__day=request.GET['odp_date__day'])

        # Get distinct shift values with aggregated loading/unloading sums
        shifts = (
            queryset
            .values('shift')
            .exclude(shift__isnull=True)
            .exclude(shift='')
            .annotate(
                total_loading=Sum('loading_qty'),
                total_unloading=Sum('unloading_qty')
            )
            .order_by('shift')
        )

        return [
            (shift['shift'],
             f"{shift['shift']} (on: {shift['total_loading'] or 0}, off: {shift['total_unloading'] or 0})")
            for shift in shifts
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(shift=self.value())
        return queryset


class DateRangeFilter(admin.SimpleListFilter):
    title = _('Date Range')
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return [
            ('today', _('Today')),
            ('yesterday', _('Yesterday')),
            ('today_yesterday', _('Today + Yesterday')),
            ('all', _('All Dates')),
        ]

    def queryset(self, request, queryset):
        from datetime import date, timedelta

        today = date.today()
        yesterday = today - timedelta(days=1)

        if self.value() == 'today':
            return queryset.filter(dated__date=today)
        elif self.value() == 'yesterday':
            return queryset.filter(dated__date=yesterday)
        elif self.value() == 'today_yesterday':
            return queryset.filter(dated__date__in=[yesterday, today])
        elif self.value() == 'all':
            return queryset
        return queryset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('fg_articleno', 'basearticleno','tis_stylecollection', 'tis_stylesize', 'tis_stylecolour')
    search_fields = ('fg_articleno', 'basearticleno', 'tis_stylecollection', 'tis_stylecolour')
    list_filter = (  'tis_stylesize', 'tis_stylecolour')


@admin.register(HangerlineEmp)
class HangerlineEmpAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'title', 'desig_id', 'line_desc', 'shift', 'activestatus')
    search_fields = ('id', 'title', 'nic', 'mobile')
    list_filter = ('line_desc', 'shift', 'gender',)
    date_hierarchy = 'joindate'


@admin.register(OperatorDailyPerformance)
class OperatorDailyPerformanceAdmin(admin.ModelAdmin):
    list_display = ('odp_date', 'shift', 'odp_em_key', 'em_firstname', 'odpd_quantity', 'oc_description', 'st_id', 'odpd_lot_number', 'source_connection')
    search_fields = ('em_firstname', 'em_lastname', 'odp_em_key', 'odpd_lot_number','st_id','oc_description')
    list_filter = ('odp_date', ShiftFilter, SourceConnectionFilter, ProductionFilter, 'odpd_is_overtime')
    date_hierarchy = 'odp_date'
    readonly_fields = ('created_at',)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.dashboard_view, name='hangerline_dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """Main hangerline dashboard view"""
        from django.shortcuts import render

        context = {
            'title': 'Production Dashboard',
            'has_permission': self.has_view_permission(request),
        }

        return render(request, 'admin/hangerline/dashboard.html', context)

    # def changelist_view(self, request, extra_context=None):
    #     """Override changelist view to add dashboard links"""
    #     extra_context = extra_context or {}
    #     extra_context.update({
    #         'dashboard_links': [
    #             {
    #                 'title': '⚛️ React Dashboard',
    #                 'url': '/dashboard/',
    #                 'description': 'Modern React interface with dark theme'
    #             },
    #             {
    #                 'title': '🏭 Production Dashboard',
    #                 'url': '/production-dashboard/',
    #                 'description': 'Complete Django production analytics with charts'
    #             },
    #             {
    #                 'title': '🔧 Breakdown Dashboard',
    #                 'url': '/breakdown-dashboard/',
    #                 'description': 'Breakdown analysis and charts'
    #             }
    #         ]
    #     })
    #     return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        now = datetime.now()

        # Current month and year
        current_month = now.month
        current_year = now.year

        # Last month and year (handle January -> December of previous year)
        if current_month == 1:
            last_month = 12
            last_year = current_year - 1
        else:
            last_month = current_month - 1
            last_year = current_year

        return qs.filter(
            Q(odp_date__year=current_year, odp_date__month=current_month) |
            Q(odp_date__year=last_year, odp_date__month=last_month)
        )

    fieldsets = (
        ('Employee Info', {
            'fields': ('odp_em_key', 'em_rfid', 'em_department', 'em_firstname', 'em_lastname'),
        }),
        ('Actual and Shift In/Out', {
            'fields': (
                ('odp_actual_clock_in', 'odp_actual_clock_out'),
                ('odp_shift_clock_in', 'odp_shift_clock_out'),
                ('odp_first_hanger_time', 'odp_last_hanger_time'),
                'odp_current_station'
            ),
        }),
        ('Operation Info', {
            'fields': (
                ('odpd_wc_key', 'odpd_workstation'),
                ('odpd_start_time','oc_standard_time', 'odpd_actual_time','odpd_actual_time_from_reader'),
                ('oc_piece_rate', 'odpd_pay_rate', 'odpd_piece_rate'),
                ('odpd_oc_key', 'oc_description','odpd_quantity'),
                ('odpd_normal_pay_factor', 'odpd_is_overtime', 'odpd_overtime_factor'),
                ('odpd_stpo_key', 'odpd_standard')
            ),
        }),
        ('Style Color & Size Info', {
            'fields':(
                ('odpd_st_key', 'st_id', 'st_description', 'odpd_lot_number' ),
                ('odpd_cm_key', 'cm_description'), 
                ('odpd_sm_key','sm_description')
            )
        }),
        ('Audit', {
            'fields': ('odp_key', 'odp_date', 'shift', 'odp_lump_sum_payment', 'odp_make_up_pay_rate',
                      'odp_last_hanger_start_time', 'created_at', 'source_connection', 'efficiency',
                      'ppd_tvwh', 'odpd_edited_by', 'odpd_edited_date'),
        }),
    )


@admin.register(QualityControlRepair)
class QualityControlRepairAdmin(admin.ModelAdmin):
    list_display = ('qcr_date', 'qcr_defect_em_key', 'defect_em_firstname', 'oc_description','qcsc_description', 'st_id','cm_description','sm_description','source_connection')
    search_fields = ('defect_em_firstname', 'defect_em_lastname', 'qcsc_description', 'st_id')
    list_filter = ('qcr_date', 'source_connection', QcscDescriptionFilter)
    date_hierarchy = 'qcr_date'
    readonly_fields = ('created_at',)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        now = datetime.now()

        # Current month and year
        current_month = now.month
        current_year = now.year

        # Last month and year (handle January -> December of previous year)
        if current_month == 1:
            last_month = 12
            last_year = current_year - 1
        else:
            last_month = current_month - 1
            last_year = current_year

        return qs.filter(
            Q(qcr_date__year=current_year) 
        )


@admin.register(Loadinginformation)
class LoadinginformationAdmin(admin.ModelAdmin):
    list_display = ('dated','id', 'pono', 'item_id', 'title', 'fg_colour', 'fg_size','bundleno', 'qty', 'line_id')
    search_fields = ('pono', 'item_id', 'title', 'fg_articleno', 'barcode', 'fg_colour', 'model', 'id')
    list_filter = ('line_id', 'maindeptt_id', 'fg_colour', 'fg_size')
    date_hierarchy = 'dated'
    ordering = ['-dated']


@admin.register(Operationinformation)
class OperationinformationAdmin(admin.ModelAdmin):
    list_display = ('dated', 'basearticleno','articleno', 'suboperation_id', 'totalsmv', 'smv', 'conversionfactor','machine')
    search_fields = ('articleno', 'suboperation_id')
    list_filter = ('maindeptt_id', 'machine')
    date_hierarchy = 'dated'



@admin.register(Stylebasicinformation)
class StylebasicinformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'fg_articleno', 'model', 'category_id', 'fg_season', 'creationdate')
    search_fields = ('fg_articleno', 'model', 'id')
    list_filter = ('category_id', 'model')
    date_hierarchy = 'creationdate'


@admin.register(EtlExtractLog)
class EtlExtractLogAdmin(admin.ModelAdmin):
    list_display = ('extractlogid', 'source_connection', 'saved_count', 'starttime', 'endtime', 'success', 'status')
    search_fields = ('processlogid', 'source_connection')
    list_filter = ('success', 'status', 'source_connection')
    date_hierarchy = 'starttime'
    readonly_fields = ('starttime', 'endtime')


@admin.register(EtlQcrExtractLog)
class EtlQcrExtractLogAdmin(admin.ModelAdmin):
    list_display = ('extractlogid', 'source_connection', 'saved_count', 'starttime', 'endtime', 'success', 'status')
    search_fields = ('processlogid', 'source_connection')
    list_filter = ('success', 'status', 'source_connection')
    date_hierarchy = 'starttime'
    readonly_fields = ('starttime', 'endtime')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('sm_key', 'sm_description')
    search_fields = ('sm_key', 'sm_description')
    ordering = ('sm_key',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('cm_key', 'cm_short_description', 'cm_description')
    search_fields = ('cm_key', 'cm_short_description', 'cm_description')
    ordering = ('cm_key',)


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('style_key', 'style_description')
    search_fields = ('style_key', 'style_description')
    ordering = ('style_key',)


@admin.register(ClientPurchaseOrder)
class ClientPurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'pono', 'client_title', 'articleno', 'item_title', 'po_qty', 'clientpodate')
    search_fields = ('pono', 'client_title', 'articleno', 'item_title')
    list_filter = ('client_title', 'pono', 'articleno')
    date_hierarchy = 'clientpodate'
    ordering = ['-clientpodate']


@admin.register(BreakdownCategory)
class BreakdownCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


class LineTargetDetailInline(admin.TabularInline):
    model = LineTargetDetail
    extra = 1  # Allow manual addition of new records
    fields = ('cpo_id', 'pono', 'articleno', 'color', 'size','item_id','item_title','target_qty')
    autocomplete_fields = ['cpo_id', 'color', 'size']
    readonly_fields = ('pono','articleno','color','size','item_id','item_title')
    # Removed readonly_fields to allow editing after fetch
    can_delete = True
    show_change_link = True


@admin.register(LineTarget)
class LineTargetAdmin(admin.ModelAdmin):
    list_display = ('source_connection', 'target_date', 'total_target_qty', 'loading_qty', 'remarks')
    list_filter = ('source_connection', 'target_date')
    search_fields = ('source_connection', 'target_date')
    ordering = ('-target_date', 'source_connection')
    inlines = [LineTargetDetailInline]

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/fetch-loading-data/', self.fetch_loading_data, name='linetarget_fetch_loading_data'),
            path('dashboard/', self.dashboard_view, name='linetarget_dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """Dashboard view showing line target summary and target vs offloading"""
        from django.db.models import Sum, Count
        from django.shortcuts import render
        from datetime import datetime, date

        # Get current month's data
        today = date.today()
        current_month = today.replace(day=1)
        next_month = date(today.year + (1 if today.month == 12 else 0), (today.month % 12) + 1, 1)

        # Aggregate LineTarget data
        line_targets = LineTarget.objects.filter(
            target_date__gte=current_month,
            target_date__lte=next_month
        )

        total_targets = line_targets.aggregate(
            total_qty=Sum('total_target_qty'),
            total_lines=Count('source_connection')
        )

        # Get actual offloading data for comparison
        actual_offloading = OperatorDailyPerformance.objects.filter(
            odp_date__gte=current_month,
            odp_date__lte=next_month
        ).aggregate(
            total_offloading=Sum('unloading_qty'),
            total_loading=Sum('loading_qty')
        )

        # Calculate variances
        target_qty = total_targets['total_qty'] or 0
        offloading_qty = actual_offloading['total_offloading'] or 0
        variance = target_qty - offloading_qty
        variance_percent = (variance / target_qty * 100) if target_qty > 0 else 0

        context = {
            'title': 'Line Target Dashboard',
            'total_targets': total_targets,
            'actual_offloading': actual_offloading,
            'variance': variance,
            'variance_percent': round(variance_percent, 2),
            'current_month': current_month.strftime('%B %Y'),
            'line_targets': line_targets,
            'has_permission': True,  # Default to True for dashboard access
        }

        return render(request, 'admin/hangerline/linetarget/dashboard.html', context)

    # def changelist_view(self, request, extra_context=None):
    #     """Override changelist view to add dashboard links"""
    #     extra_context = extra_context or {}
    #     extra_context.update({
    #         'dashboard_links': [
    #             {
    #                 'title': '🏭 Production Dashboard',
    #                 'url': '/dashboard/',
    #                 'description': 'Complete Django production analytics with charts'
    #             },
    #             {
    #                 'title': '⚛️ React Dashboard',
    #                 'url': '/production-dashboard/',
    #                 'description': 'Modern React interface (experimental)'
    #             },
    #             {
    #                 'title': '🔧 Breakdown Dashboard',
    #                 'url': '/breakdown-dashboard/',
    #                 'description': 'Breakdown analysis and charts'
    #             }
    #         ]
    #     })
        return super().changelist_view(request, extra_context)

    def fetch_loading_data(self, request, pk):
        from django.shortcuts import get_object_or_404, redirect
        from django.contrib import messages
        from django.db.models import Sum

        linetarget = get_object_or_404(LineTarget, pk=pk)

        # Clear existing details
        linetarget.linetargetdetail_set.all().delete()

        # Fetch data from Loadinginformation with exact conditions
        # Compare date part of datetime field with target_date
        from django.db.models import Q
        loading_data = Loadinginformation.objects.filter(
            Q(dated__date=linetarget.target_date),
            line_id=linetarget.source_connection
        ).exclude(
            pono__isnull=True
        ).exclude(
            pono=''
        )

        # Debug: Show what we're filtering
        messages.info(request, f"Found {loading_data.count()} loading records for date {linetarget.target_date}")

        created_count = 0
        skipped_count = 0

        for loading_item in loading_data:
            pono = loading_item.pono or ''
            st_id = loading_item.fg_articleno or ''

            # Get color and size instances
            color_instance = Color.objects.filter(cm_key=loading_item.fg_colour).first() if loading_item.fg_colour else None
            size_instance = Size.objects.filter(sm_key=loading_item.fg_size).first() if loading_item.fg_size else None

            # Create LineTargetDetail for each shift
            for shift in ['Day', 'Night']:
                LineTargetDetail.objects.create(
                    linetarget=linetarget,
                    pono=pono,
                    st_id=st_id,
                    item_id=loading_item.item_id or '',
                    item_title=loading_item.title or '',
                    model=loading_item.model,
                    barcode=loading_item.barcode,
                    scrvoucher_no=loading_item.scrvoucher_no,
                    cm_key=color_instance,
                    sm_key=size_instance,
                    bundleno=loading_item.bundleno or 0,
                    target_qty=int(loading_item.qty or 0),
                    shift=shift
                )
                created_count += 1

        # Update loading_qty
        total_qty = linetarget.linetargetdetail_set.aggregate(
            total=Sum('target_qty')
        )['total'] or 0
        linetarget.loading_qty = total_qty
        linetarget.save()

        messages.success(request, f"Successfully fetched {created_count} loading data records for {linetarget} (skipped: {skipped_count})")
        return redirect('admin:hangerline_linetarget_change', pk)



    def save_model(self, request, obj, form, change):
        """Override save_model to handle fetch_after_save"""
        super().save_model(request, obj, form, change)

        # Check if we need to redirect to fetch after save
        if request.POST.get('fetch_after_save') == '1':
            from django.shortcuts import redirect
            from django.urls import reverse
            # Redirect to the fetch URL
            fetch_url = reverse('admin:hangerline_linetarget_fetch_loading_data', args=[obj.pk])
            raise redirect(fetch_url)


@admin.register(LineTargetDetail)
class LineTargetDetailAdmin(admin.ModelAdmin):
    form = LineTargetDetailForm
    list_display = ('linetarget', 'cpo_id', 'pono', 'item_title', 'articleno', 'color', 'size', 'target_qty')
    list_filter = ('linetarget__source_connection', 'linetarget__target_date', 'shift', 'color', 'size')
    search_fields = ('item_title', 'pono', 'linetarget__source_connection', 'cpo_id__pono', 'cpo_id__item_title', 'cpo_id__articleno', 'cpo_id__client_title')
    ordering = ('linetarget', 'shift', 'pono')
    readonly_fields = ('linetarget',)
    autocomplete_fields = ['cpo_id', 'color', 'size']


@admin.register(Breakdown)
class BreakdownAdmin(admin.ModelAdmin):
    list_display = ('id', 'p_date', 'line_no', 'shift', 'breakdown_category', 'time_start', 'time_end', 'get_breakdown_time_minutes', 'operator_effected', 'loss_minutes')
    search_fields = ('line_no', 'remarks')
    list_filter = ('p_date', 'line_no', 'shift', 'breakdown_category')
    date_hierarchy = 'p_date'
    ordering = ('-p_date', '-time_start')
    autocomplete_fields = ['breakdown_category']

    fieldsets = (
        ('Basic Info', {
            'fields': ('p_date', 'line_no', 'shift', 'breakdown_category')
        }),
        ('Time Details', {
            'fields': (('time_start', 'time_end'), 'remarks')
        }),
        ('Impact', {
            'fields': ('operator_effected', 'loss_minutes')
        }),
    )

    def get_breakdown_time_minutes(self, obj):
        """Display the calculated breakdown time in minutes"""
        return obj.breakdown_time_minutes
    get_breakdown_time_minutes.short_description = 'Breakdown Time (mins)'
    get_breakdown_time_minutes.admin_order_field = 'time_start'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.dashboard_view, name='breakdown_dashboard'),
        ]
        return custom_urls + urls

    # def changelist_view(self, request, extra_context=None):
    #     """Override changelist view to add dashboard links"""
    #     extra_context = extra_context or {}
    #     extra_context.update({
    #         'dashboard_links': [
    #             {
    #                 'title': '⚛️ React Dashboard',
    #                 'url': '/dashboard/',
    #                 'description': 'Modern React interface with dark theme'
    #             },
    #             {
    #                 'title': '🏭 Production Dashboard',
    #                 'url': '/production-dashboard/',
    #                 'description': 'Complete Django production analytics with charts'
    #             },
    #             {
    #                 'title': '🔧 Breakdown Dashboard',
    #                 'url': '/breakdown-dashboard/',
    #                 'description': 'Breakdown analysis and charts'
    #             }
    #         ]
    #     })
    #     return super().changelist_view(request, extra_context)

    def dashboard_view(self, request):
        """Dashboard view showing breakdown summary and pie chart by category"""
        from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, fields
        from django.db.models.functions import Extract
        from django.shortcuts import render
        from datetime import datetime, date

        # Get date range from request parameters
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # Parse dates or use current month as default
        if start_date_str:
            try:
                start_date = date.fromisoformat(start_date_str)
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = date.fromisoformat(end_date_str)
            except ValueError:
                end_date = None
        else:
            end_date = None

        # Default to current month if no dates provided
        if not start_date or not end_date:
            today = date.today()
            current_month = today.replace(day=1)
            next_month = date(today.year + (1 if today.month == 12 else 0), (today.month % 12) + 1, 1)
            start_date = current_month
            end_date = next_month
        else:
            # For display purposes, use the start date's month
            current_month = start_date.replace(day=1)

        # Get breakdown data first
        breakdowns = Breakdown.objects.filter(
            p_date__gte=start_date,
            p_date__lte=end_date
        )

        # Calculate statistics manually since we can't use database aggregation with model properties
        total_breakdowns = breakdowns.count()
        total_time = sum(b.breakdown_time_minutes for b in breakdowns)
        avg_time = total_time / total_breakdowns if total_breakdowns > 0 else 0

        total_stats = {
            'total_breakdowns': total_breakdowns,
            'total_time': total_time,
            'avg_time': avg_time
        }

        # Group by category manually
        from collections import defaultdict
        category_data = defaultdict(lambda: {'count': 0, 'total_time': 0, 'times': []})

        for breakdown in breakdowns:
            cat_name = breakdown.breakdown_category.name
            time_mins = breakdown.breakdown_time_minutes
            category_data[cat_name]['count'] += 1
            category_data[cat_name]['total_time'] += time_mins
            category_data[cat_name]['times'].append(time_mins)

        # Convert to list and calculate averages
        category_stats = []
        for cat_name, data in category_data.items():
            avg_time = data['total_time'] / data['count'] if data['count'] > 0 else 0
            category_stats.append({
                'breakdown_category__name': cat_name,
                'count': data['count'],
                'total_time': data['total_time'],
                'avg_time': avg_time
            })

        # Sort by total time descending
        category_stats.sort(key=lambda x: x['total_time'], reverse=True)

        # Calculate percentage for each category
        total_time_all = total_stats['total_time'] or 0
        for stat in category_stats:
            if total_time_all > 0:
                stat['percentage'] = round((stat['total_time'] or 0) / total_time_all * 100, 1)
            else:
                stat['percentage'] = 0.0

        # Group by line manually
        line_data = defaultdict(lambda: {'count': 0, 'total_time': 0, 'times': []})

        for breakdown in breakdowns:
            line_name = breakdown.line_no
            time_mins = breakdown.breakdown_time_minutes
            line_data[line_name]['count'] += 1
            line_data[line_name]['total_time'] += time_mins
            line_data[line_name]['times'].append(time_mins)

        # Convert to list and calculate averages
        line_stats = []
        for line_name, data in line_data.items():
            avg_time = data['total_time'] / data['count'] if data['count'] > 0 else 0
            line_stats.append({
                'line_no': line_name,
                'count': data['count'],
                'total_time': data['total_time'],
                'avg_time': avg_time
            })

        # Sort by total time descending
        line_stats.sort(key=lambda x: x['total_time'], reverse=True)

        # Calculate percentage for each line
        for stat in line_stats:
            if total_time_all > 0:
                stat['percentage'] = round((stat['total_time'] or 0) / total_time_all * 100, 1)
            else:
                stat['percentage'] = 0.0

        # Prepare data for category pie chart
        category_chart_labels = [stat['breakdown_category__name'] for stat in category_stats] if category_stats else []
        category_chart_data = [stat['total_time'] or 0 for stat in category_stats] if category_stats else []

        # Prepare data for line pie chart
        line_chart_labels = [stat['line_no'] for stat in line_stats] if line_stats else []
        line_chart_data = [stat['total_time'] or 0 for stat in line_stats] if line_stats else []

        # Colors for pie charts
        chart_colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
        ]

        # Calculate trend data (breakdown time by date and line)
        from collections import defaultdict
        trend_data = defaultdict(lambda: defaultdict(float))

        # Group breakdowns by date and line
        for breakdown in breakdowns:
            date_str = breakdown.p_date.isoformat()
            line_name = breakdown.line_no
            trend_data[date_str][line_name] += breakdown.breakdown_time_minutes

        # Prepare data for line-wise trend chart
        dates = sorted(trend_data.keys())
        lines = sorted(set(line for date_data in trend_data.values() for line in date_data.keys()))

        trend_chart_data = []
        for line in lines:
            line_data = []
            for date in dates:
                line_data.append(trend_data[date].get(line, 0))
            trend_chart_data.append({
                'label': f'Line {line}',
                'data': line_data,
                'borderColor': chart_colors[len(trend_chart_data) % len(chart_colors)],
                'backgroundColor': chart_colors[len(trend_chart_data) % len(chart_colors)].replace('1)', '0.1)'),
                'fill': False,
                'tension': 0.1
            })

        # Calculate total downtime trend data (sum across all lines per date)
        total_trend_data = []
        for date in dates:
            total_time = sum(trend_data[date].values())
            total_trend_data.append(total_time)

        total_trend_chart_data = [{
            'label': 'Total Downtime',
            'data': total_trend_data,
            'borderColor': '#dc3545',
            'backgroundColor': 'rgba(220, 53, 69, 0.1)',
            'fill': False,
            'tension': 0.1,
            'borderWidth': 3,
            'pointBackgroundColor': '#dc3545',
            'pointBorderColor': '#fff',
            'pointBorderWidth': 2,
            'pointRadius': 5
        }]

        # Calculate category-wise trend data (breakdown time by category over time)
        category_trend_data = defaultdict(lambda: defaultdict(float))

        # Group breakdowns by date and category
        for breakdown in breakdowns:
            date_str = breakdown.p_date.isoformat()
            category_name = breakdown.breakdown_category.name
            category_trend_data[date_str][category_name] += breakdown.breakdown_time_minutes

        # Prepare data for category trend chart
        # Get all unique categories across all dates
        all_categories = sorted(set(category for date_data in category_trend_data.values() for category in date_data.keys()))

        category_trend_chart_data = []
        for category_name in all_categories:
            category_line_data = []
            for date in dates:
                category_line_data.append(category_trend_data[date].get(category_name, 0))
            category_trend_chart_data.append({
                'label': category_name,
                'data': category_line_data,
                'borderColor': chart_colors[len(category_trend_chart_data) % len(chart_colors)],
                'backgroundColor': chart_colors[len(category_trend_chart_data) % len(chart_colors)].replace('1)', '0.1)'),
                'fill': False,
                'tension': 0.1,
                'borderWidth': 2,
                'pointBackgroundColor': chart_colors[len(category_trend_chart_data) % len(chart_colors)],
                'pointBorderColor': '#fff',
                'pointBorderWidth': 1,
                'pointRadius': 4
            })

        import json
        context = {
            # 'title': 'Breakdown Dashboard',
            'total_stats': total_stats,
            'category_stats': category_stats,
            'line_stats': line_stats,
            'category_chart_labels': json.dumps(category_chart_labels),
            'category_chart_data': json.dumps(category_chart_data),
            'line_chart_labels': json.dumps(line_chart_labels),
            'line_chart_data': json.dumps(line_chart_data),
            'trend_dates': json.dumps(dates),
            'trend_chart_data': json.dumps(trend_chart_data),
            'total_trend_chart_data': json.dumps(total_trend_chart_data),
            'category_trend_chart_data': json.dumps(category_trend_chart_data),
            'chart_colors': json.dumps(chart_colors),
            'current_month': current_month.strftime('%B %Y'),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'has_permission': self.has_view_permission(request),
        }

        return render(request, 'admin/hangerline/breakdown/dashboard.html', context)


@admin.register(TransferToPacking)
class TransferToPackingAdmin(admin.ModelAdmin):
    list_display = ('id', 'dated', 'proddate', 'pono', 'articleno', 'item_title', 'line_desc','qtytransferred')
    search_fields = ('pono', 'articleno', 'item_id', 'item_title', 'scrvoucher_no', 'qtytransferred', 'from_dept_name', 'to_dept_name')
    list_filter = (DateRangeFilter, 'dated', 'proddate', 'from_dept_name','to_dept_name', 'line_desc')
    date_hierarchy = 'dated'
    ordering = ['-dated']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        from datetime import date, timedelta

        # Default to showing today + yesterday data if no date_range filter is applied
        if not request.GET.get('date_range'):
            today = date.today()
            yesterday = today - timedelta(days=1)
            qs = qs.filter(dated__date__in=[yesterday, today])

        return qs
