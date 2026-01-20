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

        # Check if any date filters are applied
        has_date_filter = (
            'odp_date__gte' in request.GET or
            'odp_date__lte' in request.GET or
            'odp_date__year' in request.GET or
            'odp_date__month' in request.GET or
            'odp_date__day' in request.GET or
            request.GET.get('odp_date_range')
        )

        # If no date filters are applied, default to today
        if not has_date_filter:
            from datetime import date
            today = date.today()
            queryset = queryset.filter(odp_date=today)
        else:
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

            # Apply custom date range filter
            if request.GET.get('odp_date_range'):
                from datetime import date, timedelta
                today = date.today()
                yesterday = today - timedelta(days=1)

                odp_date_range = request.GET['odp_date_range']
                if odp_date_range == 'today':
                    queryset = queryset.filter(odp_date=today)
                elif odp_date_range == 'yesterday':
                    queryset = queryset.filter(odp_date=yesterday)
                elif odp_date_range == 'today_yesterday':
                    queryset = queryset.filter(odp_date__in=[yesterday, today])

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

        # Check if any date filters are applied
        has_date_filter = (
            'qcr_date__gte' in request.GET or
            'qcr_date__lte' in request.GET or
            'qcr_date__year' in request.GET or
            'qcr_date__month' in request.GET or
            'qcr_date__day' in request.GET
        )

        # If no date filters are applied, default to today
        if not has_date_filter:
            from datetime import date
            today = date.today()
            queryset = queryset.filter(qcr_date=today)
        else:
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

        # Check if any date filters are applied
        has_date_filter = (
            'odp_date__gte' in request.GET or
            'odp_date__lte' in request.GET or
            'odp_date__year' in request.GET or
            'odp_date__month' in request.GET or
            'odp_date__day' in request.GET or
            request.GET.get('odp_date_range')
        )

        # If no date filters are applied, default to today
        if not has_date_filter:
            from datetime import date
            today = date.today()
            queryset = queryset.filter(odp_date=today)
        else:
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

            # Apply custom date range filter
            if request.GET.get('odp_date_range'):
                from datetime import date, timedelta
                today = date.today()
                yesterday = today - timedelta(days=1)

                odp_date_range = request.GET['odp_date_range']
                if odp_date_range == 'today':
                    queryset = queryset.filter(odp_date=today)
                elif odp_date_range == 'yesterday':
                    queryset = queryset.filter(odp_date=yesterday)
                elif odp_date_range == 'today_yesterday':
                    queryset = queryset.filter(odp_date__in=[yesterday, today])

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

        # Check if any date filters are applied
        has_date_filter = (
            'odp_date__gte' in request.GET or
            'odp_date__lte' in request.GET or
            'odp_date__year' in request.GET or
            'odp_date__month' in request.GET or
            'odp_date__day' in request.GET or
            request.GET.get('odp_date_range')
        )

        # If no date filters are applied, default to today
        if not has_date_filter:
            from datetime import date
            today = date.today()
            queryset = queryset.filter(odp_date=today)
        else:
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

            # Apply custom date range filter
            if request.GET.get('odp_date_range'):
                from datetime import date, timedelta
                today = date.today()
                yesterday = today - timedelta(days=1)

                odp_date_range = request.GET['odp_date_range']
                if odp_date_range == 'today':
                    queryset = queryset.filter(odp_date=today)
                elif odp_date_range == 'yesterday':
                    queryset = queryset.filter(odp_date=yesterday)
                elif odp_date_range == 'today_yesterday':
                    queryset = queryset.filter(odp_date__in=[yesterday, today])

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


class ODPDateRangeFilter(admin.SimpleListFilter):
    title = _('Date Range')
    parameter_name = 'odp_date_range'

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
            return queryset.filter(odp_date=today)
        elif self.value() == 'yesterday':
            return queryset.filter(odp_date=yesterday)
        elif self.value() == 'today_yesterday':
            return queryset.filter(odp_date__in=[yesterday, today])
        elif self.value() == 'all':
            return queryset
        return queryset


class AttendanceDateFilter(admin.SimpleListFilter):
    title = _('Attendance Date')
    parameter_name = 'attendance_date'

    def lookups(self, request, model_admin):
        from datetime import date, timedelta
        today = date.today()

        # Create options for the last 7 days
        options = []
        for i in range(7):
            check_date = today - timedelta(days=i)
            if i == 0:
                label = _('Today')
            elif i == 1:
                label = _('Yesterday')
            else:
                label = check_date.strftime('%b %d')  # Format like "Jan 07"

            options.append((check_date.isoformat(), label))

        # Add custom date option
        options.append(('custom', _('Custom Date')))

        return options

    def queryset(self, request, queryset):
        # For HangerlineEmp model, this filter only provides date selection
        # The actual attendance filtering is handled by AttendanceStatusFilter
        return queryset


class AttendanceStatusFilter(admin.SimpleListFilter):
    title = _('Attendance Status')
    parameter_name = 'attendance_status'

    def lookups(self, request, model_admin):
        return [
            ('present', _('Present')),
            ('absent', _('Absent')),
        ]

    def queryset(self, request, queryset):
        # Get the selected attendance date
        attendance_date = request.GET.get('attendance_date')
        if not attendance_date:
            return queryset

        # Parse the date
        from datetime import date
        try:
            if attendance_date in ['today', 'yesterday']:
                today = date.today()
                if attendance_date == 'today':
                    check_date = today
                else:  # yesterday
                    check_date = today.replace(day=today.day - 1)
            else:
                # ISO format date string
                check_date = date.fromisoformat(attendance_date)
        except (ValueError, AttributeError):
            return queryset

        # Get employee IDs that have production records for the selected date
        present_employee_ids = set(
            OperatorDailyPerformance.objects.filter(
                odp_date=check_date
            ).values_list('odp_em_key', flat=True)
        )

        if self.value() == 'present':
            # Filter to employees who have records (Present)
            return queryset.filter(id__in=present_employee_ids)
        elif self.value() == 'absent':
            # Filter to employees who don't have records (Absent)
            return queryset.exclude(id__in=present_employee_ids)

        return queryset


class LineDescFilter(admin.SimpleListFilter):
    """Custom filter to show only line-21 to line-32"""
    title = _('Line')
    parameter_name = 'line_desc'

    def lookups(self, request, model_admin):
        # Define the lines we want to show (line-21 to line-32)
        lines = [f'line-{i}' for i in range(21, 33)]

        # Query for counts
        queryset = HangerlineEmp.objects.filter(line_desc__in=lines)

        # Get employee counts per line
        line_counts = {}
        for line in lines:
            count = queryset.filter(line_desc=line).count()
            if count > 0:  # Only include lines that have employees
                line_counts[line] = count

        # Return as lookups with counts
        return [(line, f'{line.upper()} ({count})') for line, count in sorted(line_counts.items())]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(line_desc=self.value())
        return queryset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('fg_articleno', 'basearticleno','tis_stylecollection', 'tis_stylesize', 'tis_stylecolour')
    search_fields = ('fg_articleno', 'basearticleno', 'tis_stylecollection', 'tis_stylecolour')
    list_filter = (  'tis_stylesize', 'tis_stylecolour')


@admin.register(HangerlineEmp)
class HangerlineEmpAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'title', 'desig_id', 'line_desc', 'shift', 'activestatus', 'attendance_status')
    search_fields = ('id', 'title', 'nic', 'mobile')
    list_filter = (AttendanceDateFilter, AttendanceStatusFilter, LineDescFilter, 'shift', 'gender',)
    date_hierarchy = 'joindate'
    change_list_template = 'admin/hangerline/hangerlineemp/changelist_result.html'

    def attendance_status(self, obj):
        """Check if employee was present/absent on selected date"""
        from datetime import date

        # Get the selected attendance date from request
        request = getattr(self, '_request', None)
        if not request:
            return 'N/A'

        selected_date = request.GET.get('attendance_date')
        if not selected_date:
            return 'N/A'

        # Handle different date formats
        if selected_date == 'custom':
            # For custom date, we might need additional handling
            return 'N/A'
        else:
            try:
                # Parse the date
                if selected_date in ['today', 'yesterday']:
                    # These are labels, get actual dates
                    today = date.today()
                    if selected_date == 'today':
                        check_date = today
                    else:  # yesterday
                        check_date = today.replace(day=today.day - 1)
                else:
                    # ISO format date string
                    check_date = date.fromisoformat(selected_date)

                # Check if employee has any production records for this date
                has_records = OperatorDailyPerformance.objects.filter(
                    odp_em_key=obj.id,
                    odp_date=check_date
                ).exists()

                return 'Present' if has_records else 'Absent'
            except (ValueError, AttributeError):
                return 'N/A'

    attendance_status.short_description = 'Attendance Status'

    def changelist_view(self, request, extra_context=None):
        """Store request for use in attendance_status method and add attendance summary"""
        self._request = request

        extra_context = extra_context or {}

        # Calculate attendance summary for selected date
        attendance_date = request.GET.get('attendance_date')
        if attendance_date:
            from datetime import date
            try:
                # Parse the date
                if attendance_date in ['today', 'yesterday']:
                    today = date.today()
                    if attendance_date == 'today':
                        check_date = today
                    else:  # yesterday
                        check_date = today.replace(day=today.day - 1)
                else:
                    # ISO format date string
                    check_date = date.fromisoformat(attendance_date)

                # Get all employees for the selected date's line/shift combinations
                line_filter = request.GET.get('line_desc')
                shift_filter = request.GET.get('shift')

                # Start with all employees, but restrict to lines 21-32 for summary cards
                target_lines = [f'line-{i}' for i in range(21, 33)]
                employees_query = HangerlineEmp.objects.filter(line_desc__in=target_lines)

                # Apply additional line and shift filters if selected
                if line_filter:
                    employees_query = employees_query.filter(line_desc=line_filter)
                if shift_filter:
                    employees_query = employees_query.filter(shift=shift_filter)

                total_employees = employees_query.count()

                # Get employee IDs that have production records for the selected date
                present_employee_ids = set(
                    OperatorDailyPerformance.objects.filter(
                        odp_date=check_date
                    ).values_list('odp_em_key', flat=True)
                )

                # Calculate present/absent counts
                present_count = employees_query.filter(id__in=present_employee_ids).count()
                absent_count = total_employees - present_count

                # Calculate line-wise attendance - only show lines 21-32
                from django.db.models import Count, Q

                # Define lines we want to show (21-32)
                target_lines = [f'line-{i}' for i in range(21, 33)]

                line_attendance = []
                # Always show line breakdown for lines 21-32, but filter based on selected line if any
                if not line_filter:
                    # No specific line selected - show all lines 21-32
                    lines_to_show = target_lines
                else:
                    # Specific line selected - only show that line if it's in our target range
                    lines_to_show = [line_filter] if line_filter in target_lines else []

                for line_name in lines_to_show:
                    line_employees = employees_query.filter(line_desc=line_name)
                    line_total = line_employees.count()

                    if line_total > 0:  # Only include lines that have employees
                        # Get present count for this line
                        line_present_ids = set(
                            OperatorDailyPerformance.objects.filter(
                                odp_date=check_date,
                                odp_em_key__in=line_employees.values_list('id', flat=True)
                            ).values_list('odp_em_key', flat=True)
                        )
                        line_present_count = len(line_present_ids)
                        line_absent_count = line_total - line_present_count

                        line_attendance.append({
                            'line': line_name,
                            'total': line_total,
                            'present': line_present_count,
                            'absent': line_absent_count,
                            'present_percent': round((line_present_count / line_total * 100), 1) if line_total > 0 else 0
                        })

                extra_context.update({
                    'attendance_summary': {
                        'date': check_date,
                        'total_employees': total_employees,
                        'present_count': present_count,
                        'absent_count': absent_count,
                        'present_percent': round((present_count / total_employees * 100), 1) if total_employees > 0 else 0,
                        'line_attendance': line_attendance
                    }
                })

            except (ValueError, AttributeError):
                pass  # Invalid date, don't show summary

        return super().changelist_view(request, extra_context)


@admin.register(OperatorDailyPerformance)
class OperatorDailyPerformanceAdmin(admin.ModelAdmin):
    list_display = ('odp_date', 'shift', 'odp_em_key', 'em_firstname', 'odpd_quantity', 'oc_description', 'st_id', 'odpd_lot_number', 'source_connection')
    search_fields = ('em_firstname', 'em_lastname', 'odp_em_key', 'odpd_lot_number','st_id','oc_description')
    list_filter = (ODPDateRangeFilter, 'odp_date', ShiftFilter, SourceConnectionFilter, ProductionFilter, 'odpd_is_overtime')
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Only apply default today filter if no date range filter is active
        if not request.GET.get('odp_date_range'):
            from datetime import date
            today = date.today()
            qs = qs.filter(odp_date=today)

        return qs

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
    list_display = ('dated','id', 'pono', 'item_id', 'title','bundleno', 'qty','line_desc')
    search_fields = ('pono', 'item_id', 'title', 'fg_articleno', 'barcode')
    list_filter = ('dated','line_desc', 'item_id')
    date_hierarchy = 'dated'
    ordering = ['-dated']

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
            Q(dated__month=current_month) 
        )


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


class POProductionDateFilter(admin.SimpleListFilter):
    title = _('Production Activity Date')
    parameter_name = 'po_production_date'

    def lookups(self, request, model_admin):
        from datetime import date, timedelta
        today = date.today()

        # Create options for the last 7 days
        options = []
        for i in range(7):
            check_date = today - timedelta(days=i)
            if i == 0:
                label = 'Today'
            elif i == 1:
                label = 'Yesterday'
            else:
                label = check_date.strftime('%b %d')  # Format like "Jan 07"

            options.append((check_date.isoformat(), label))

        # Add custom date option
        options.append(('custom', 'Custom Date'))

        return options

    def queryset(self, request, queryset):
        return queryset  # No filtering on the main queryset, used only for context


@admin.register(ClientPurchaseOrder)
class ClientPurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'pono', 'client_title', 'articleno', 'item_title', 'po_qty', 'clientpodate')
    search_fields = ('pono', 'client_title', 'articleno', 'item_title')
    list_filter = ('client_title',  POProductionDateFilter,'pono', 'articleno',)
    date_hierarchy = 'clientpodate'
    ordering = ['-clientpodate']
    change_list_template = 'admin/hangerline/clientpurchaseorder/change_list.html'


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
            Q(clientpodate__year=current_year) 
        )




    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add PO summary dashboard link"""
        extra_context = extra_context or {}

        # Get the selected production date filter value
        selected_date = request.GET.get('po_production_date', '')

        # Build the URL with the selected date parameter if available
        base_url = '/admin/hangerline/clientpurchaseorder/po-summary/'
        if selected_date and selected_date != 'custom':
            url = f'{base_url}?po_production_date={selected_date}'
        else:
            url = base_url

        extra_context.update({
            'dashboard_links': [
                {
                    'title': '📦 PO Progress Summary',
                    'url': url,
                    'description': f'View PO progress with summary cards and progress bars{f" (filtered by: {selected_date})" if selected_date and selected_date != "custom" else ""}'
                }
            ]
        })
        return super().changelist_view(request, extra_context)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('po-summary/', self.po_summary_view, name='po_summary_dashboard'),
        ]
        return custom_urls + urls

    def po_summary_view(self, request):
        """PO Progress Summary Dashboard with summary cards and progress bars"""
        from django.db.models import Sum, Min, Q
        from django.shortcuts import render
        from datetime import date, timedelta

        # Get PO summary data using Django ORM equivalent of the SQL query
        po_data = []

        # Get date range from request parameters, default to today and yesterday
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # Parse dates or use defaults
        if start_date_str:
            try:
                start_date = date.fromisoformat(start_date_str)
            except (ValueError, AttributeError):
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = date.fromisoformat(end_date_str)
            except (ValueError, AttributeError):
                end_date = None
        else:
            end_date = None

        # Default to today and yesterday if no dates provided
        if not start_date or not end_date:
            today = date.today()
            yesterday = today - timedelta(days=1)
            start_date = yesterday
            end_date = today

        # Get the selected production date from filter (for backward compatibility)
        selected_date = request.GET.get('po_production_date')
        if selected_date and selected_date != 'custom':
            try:
                # If a specific date is selected, override the date range
                filter_date = date.fromisoformat(selected_date)
                start_date = filter_date
                end_date = filter_date
            except (ValueError, AttributeError):
                pass  # Keep the existing date range

        # Get POs that have production records in the selected date range
        pos_with_recent_production = OperatorDailyPerformance.objects.filter(
            odp_date__gte=start_date,
            odp_date__lte=end_date,
            unloading_qty__gt=0
        ).values_list('odpd_lot_number', flat=True).distinct()

        # Get all POs with their quantities, but only those with recent production
        pos = ClientPurchaseOrder.objects.filter(
            pono__in=pos_with_recent_production
        ).annotate(
            po_start_date=Min('clientpodate')
        ).values('pono', 'po_start_date').annotate(
            po_qty=Sum('po_qty')
        ).order_by('pono')

        for po in pos:
            pono = po['pono']
            po_start_date = po['po_start_date']
            po_qty = po['po_qty'] or 0

            # Skip POs with null start dates or handle them with a fallback
            if po_start_date is None:
                # Use a very old date as fallback for POs with no start date
                from datetime import date
                po_start_date = date(2000, 1, 1)  # Fallback date

            # Get cumulative produced quantity from PO start to today
            produced_qty = OperatorDailyPerformance.objects.filter(
                odpd_lot_number=pono,
                odp_date__gte=po_start_date,
                odp_date__lte=date.today(),
                unloading_qty__gt=0
            ).aggregate(total=Sum('unloading_qty'))['total'] or 0

            # Get cumulative transferred quantity from PO start to today
            transferred_qty = TransferToPacking.objects.filter(
                pono=pono,
                proddate__gte=po_start_date,
                proddate__lte=date.today()
            ).aggregate(total=Sum('qtytransferred'))['total'] or 0

            # Calculate derived values
            pending_po_qty = po_qty - produced_qty
            in_hand_sewing = produced_qty - transferred_qty

            # Calculate completion percentage
            completion_percent = round((produced_qty / po_qty * 100), 1) if po_qty > 0 else 0

            po_data.append({
                'pono': pono,
                'po_start_date': po_start_date,
                'po_qty': po_qty,
                'todate_produced': produced_qty,
                'todate_transfer': transferred_qty,
                'pending_po_qty': max(0, pending_po_qty),  # Ensure not negative
                'in_hand_sewing': max(0, in_hand_sewing),  # Ensure not negative
                'completion_percent': completion_percent
            })

        # Calculate summary statistics
        total_pos = len(po_data)
        total_po_qty = sum(po['po_qty'] for po in po_data)
        total_produced = sum(po['todate_produced'] for po in po_data)
        total_transferred = sum(po['todate_transfer'] for po in po_data)
        total_pending = sum(po['pending_po_qty'] for po in po_data)
        total_in_hand = sum(po['in_hand_sewing'] for po in po_data)

        # Calculate overall completion percentage
        overall_completion = round((total_produced / total_po_qty * 100), 1) if total_po_qty > 0 else 0

        summary_stats = {
            'total_pos': total_pos,
            'total_po_qty': total_po_qty,
            'total_produced': total_produced,
            'total_transferred': total_transferred,
            'total_pending': total_pending,
            'total_in_hand': total_in_hand,
            'overall_completion': overall_completion
        }

        context = {
            'title': 'PO Progress Summary',
            'po_data': po_data,
            'summary_stats': summary_stats,
            'has_permission': self.has_view_permission(request),
        }

        return render(request, 'admin/hangerline/clientpurchaseorder/po_summary.html', context)


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
    list_display = ('source_connection', 'target_date', 'shift', 'total_target_qty', 'loading_qty', 'remarks')
    list_filter = ('source_connection', 'target_date', 'shift')
    search_fields = ('source_connection', 'target_date')
    ordering = ('-target_date', 'source_connection', 'shift')
    inlines = [LineTargetDetailInline]
    change_list_template = 'admin/hangerline/linetarget/change_list.html'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/fetch-loading-data/', self.fetch_loading_data, name='linetarget_fetch_loading_data'),
            path('dashboard/', self.dashboard_view, name='linetarget_dashboard'),
            path('bulk-generate/', self.bulk_generate_view, name='linetarget_bulk_generate'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """Dashboard view showing line target summary and target vs offloading"""
        from django.db.models import Sum, Count
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

        # Aggregate LineTarget data for the date range
        line_targets = LineTarget.objects.filter(
            target_date__gte=start_date,
            target_date__lte=end_date
        ).select_related()

        total_targets = line_targets.aggregate(
            total_qty=Sum('total_target_qty'),
            total_lines=Count('source_connection', distinct=True)
        )

        # Get actual offloading data for the date range
        actual_offloading = OperatorDailyPerformance.objects.filter(
            odp_date__gte=start_date,
            odp_date__lte=end_date
        ).aggregate(
            total_offloading=Sum('unloading_qty'),
            total_loading=Sum('loading_qty')
        )

        # Calculate line-wise performance data
        line_performance = []
        for line_target in line_targets:
            # Get actual offloading for this specific line, date, and shift
            actual_qty = OperatorDailyPerformance.objects.filter(
                source_connection=line_target.source_connection,
                odp_date=line_target.target_date,
                shift=line_target.shift
            ).aggregate(
                total=Sum('unloading_qty')
            )['total'] or 0

            # Calculate variance and achievement percentage
            target_qty = line_target.total_target_qty or 0
            variance = target_qty - actual_qty
            achievement_percent = round((actual_qty / target_qty * 100), 1) if target_qty > 0 else 0

            line_performance.append({
                'line': line_target.source_connection,
                'date': line_target.target_date,
                'shift': line_target.shift,
                'target_qty': target_qty,
                'actual_qty': actual_qty,
                'variance': variance,
                'achievement_percent': achievement_percent,
            })

        # Calculate overall variances
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
            'line_performance': line_performance,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'has_permission': True,  # Default to True for dashboard access
        }

        return render(request, 'admin/hangerline/linetarget/dashboard.html', context)

    def bulk_generate_view(self, request):
        """Bulk generate LineTarget records for date range"""
        from django.shortcuts import render, redirect
        from django.contrib import messages
        from datetime import datetime, timedelta, date
        from .models import LineTarget

        if request.method == 'POST':
            # Get form data
            line = request.POST.get('line')
            fromdate_str = request.POST.get('fromdate')
            todate_str = request.POST.get('todate')
            target_qty = request.POST.get('target_qty')

            try:
                # Parse dates
                fromdate = datetime.strptime(fromdate_str, '%Y-%m-%d').date()
                todate = datetime.strptime(todate_str, '%Y-%m-%d').date()
                target_qty = int(target_qty)

                # Validate inputs
                if fromdate > todate:
                    messages.error(request, "From date cannot be after to date.")
                    return redirect('admin:linetarget_bulk_generate')

                if target_qty <= 0:
                    messages.error(request, "Target quantity must be positive.")
                    return redirect('admin:linetarget_bulk_generate')

                if target_qty % 2 != 0:
                    messages.error(request, "Target quantity must be even (divisible by 2).")
                    return redirect('admin:linetarget_bulk_generate')

                # Calculate per-shift target
                per_shift_target = target_qty // 2

                # Generate date range
                current_date = fromdate
                created_count = 0
                skipped_count = 0

                while current_date <= todate:
                    # Check if records already exist for this date/line/shift combination
                    existing_day = LineTarget.objects.filter(
                        source_connection=line,
                        target_date=current_date,
                        shift='Day'
                    ).exists()

                    existing_night = LineTarget.objects.filter(
                        source_connection=line,
                        target_date=current_date,
                        shift='Night'
                    ).exists()

                    if not existing_day:
                        LineTarget.objects.create(
                            source_connection=line,
                            target_date=current_date,
                            shift='Day',
                            total_target_qty=per_shift_target,
                            remarks=f'Bulk generated - {target_qty} total target'
                        )
                        created_count += 1
                    else:
                        skipped_count += 1

                    if not existing_night:
                        LineTarget.objects.create(
                            source_connection=line,
                            target_date=current_date,
                            shift='Night',
                            total_target_qty=per_shift_target,
                            remarks=f'Bulk generated - {target_qty} total target'
                        )
                        created_count += 1
                    else:
                        skipped_count += 1

                    current_date += timedelta(days=1)

                messages.success(request,
                    f"Successfully created {created_count} LineTarget records. "
                    f"Skipped {skipped_count} existing records."
                )
                return redirect('admin:hangerline_linetarget_changelist')

            except ValueError as e:
                messages.error(request, f"Invalid input: {str(e)}")
                return redirect('admin:linetarget_bulk_generate')

        # GET request - show form
        context = {
            'title': 'Bulk Generate Line Targets',
            'has_permission': self.has_view_permission(request),
            'line_choices': LineTarget.LINE_CHOICES,
        }

        return render(request, 'admin/hangerline/linetarget/bulk_generate.html', context)

    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add bulk generate link"""
        extra_context = extra_context or {}
        extra_context.update({
            'dashboard_links': [
                {
                    'title': '⚡ Bulk Generate Targets',
                    'url': '/admin/hangerline/linetarget/bulk-generate/',
                    'description': 'Generate line targets for date ranges with Day/Night shifts'
                },
                {
                    'title': '📊 Dashboard',
                    'url': '/admin/hangerline/linetarget/dashboard/',
                    'description': 'View line target dashboard with charts'
                }
            ]
        })
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
    change_list_template = 'admin/hangerline/breakdown/change_list.html'

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

    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add dashboard links"""
        extra_context = extra_context or {}
        extra_context.update({
            'dashboard_links': [
                {
                    'title': '🔧 Breakdown Dashboard',
                    'url': '/breakdown-dashboard/',
                    'description': 'Breakdown analysis and charts'
                },
                {
                    'title': '🏭 Production Dashboard',
                    'url': '/hangerline/dashboard/',
                    'description': 'Complete Django production analytics with charts'
                },
                {
                    'title': '📦 PO Progress Summary',
                    'url': '/admin/hangerline/clientpurchaseorder/po-summary/',
                    'description': 'View PO progress with summary cards and progress bars'
                }
            ]
        })
        return super().changelist_view(request, extra_context)

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
