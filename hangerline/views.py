from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from .models import OperatorDailyPerformance, LineTarget, Breakdown, BreakdownCategory, QualityControlRepair, HangerlineEmp, Operationinformation
# from .batch_api import fetch_batch_no


def django_dashboard(request):
    """Django production dashboard view with summary cards and charts"""
    import json
    from django.db.models import Sum, Count
    from datetime import datetime

    # Get date range from request parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    line_filter = request.GET.get('line')
    shift_filter = request.GET.get('shift')

    # Parse dates or use current month as default
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = None
    else:
        start_date = None

    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = None
    else:
        end_date = None

    # Default to current date if no dates provided
    if not start_date or not end_date:
        today = datetime.now().date()
        start_date = today
        end_date = today

    # Debug: Check if database has any data at all
    total_records = OperatorDailyPerformance.objects.count()
    print(f"DEBUG: Total OperatorDailyPerformance records: {total_records}")

    if total_records == 0:
        print("DEBUG: No data in OperatorDailyPerformance table")
    else:
        # Check data for the selected date range
        date_filtered_count = OperatorDailyPerformance.objects.filter(
            odp_date__gte=start_date,
            odp_date__lte=end_date
        ).count()
        print(f"DEBUG: Records in date range {start_date} to {end_date}: {date_filtered_count}")

        # If no data for today, try to find data from recent days
        if date_filtered_count == 0:
            print("DEBUG: No data found for selected dates, trying broader range")
            # Look for data in the last 30 days
            end_date_30 = today
            start_date_30 = today - timedelta(days=30)
            recent_count = OperatorDailyPerformance.objects.filter(
                odp_date__gte=start_date_30,
                odp_date__lte=end_date_30
            ).count()
            print(f"DEBUG: Records in last 30 days: {recent_count}")

            if recent_count > 0:
                print("DEBUG: Found data in last 30 days, using that range")
                start_date = start_date_30
                end_date = end_date_30

    try:
        # Get summary statistics
        queryset = OperatorDailyPerformance.objects.filter(
            odp_date__gte=start_date,
            odp_date__lte=end_date
        )

        # Apply line filter if provided
        if line_filter:
            queryset = queryset.filter(source_connection=line_filter)

        # Apply shift filter if provided
        if shift_filter:
            queryset = queryset.filter(shift=shift_filter)

        # Calculate totals
        totals = queryset.aggregate(
            total_loading=Sum('loading_qty'),
            total_offloading=Sum('unloading_qty'),
            total_quantity=Sum('odpd_quantity')
        )

        # Calculate WIP (Loading - Offloading)
        total_loading = totals['total_loading'] or 0
        total_offloading = totals['total_offloading'] or 0
        total_wip = total_loading - total_offloading

        # Get line count
        line_count = queryset.values('source_connection').distinct().count()

        # Get shift count
        shift_count = queryset.values('shift').distinct().exclude(shift__isnull=True).exclude(shift='').count()

        # ========== LINE TARGET DATA ==========
        target_queryset = LineTarget.objects.filter(
            target_date__gte=start_date,
            target_date__lte=end_date
        )
        if line_filter:
            target_queryset = target_queryset.filter(source_connection=line_filter)

        # Get total target
        total_target = target_queryset.aggregate(total=Sum('total_target_qty'))['total'] or 0

        # Get all available lines from production data for the date range
        all_lines = queryset.values_list('source_connection', flat=True).distinct().exclude(
            source_connection__isnull=True
        ).exclude(source_connection='').order_by('source_connection')

        # Calculate variance (target - offloading)
        variance = total_offloading - total_target
        variance_percent = round((variance / total_target * 100), 1) if total_target > 0 else 0

        # Achievement percentage
        achievement_percent = round((total_offloading / total_target * 100), 1) if total_target > 0 else 0

        # Efficiency (offloading / loading * 100)
        efficiency = round((total_offloading / total_loading * 100), 1) if total_loading > 0 else 0

        # ========== DEFECT DATA ==========
        defect_queryset = QualityControlRepair.objects.filter(
            qcr_date__gte=start_date,
            qcr_date__lte=end_date
        )

        # Apply line filter if provided
        if line_filter:
            defect_queryset = defect_queryset.filter(source_connection=line_filter)

        # Apply shift filter if provided
        if shift_filter:
            defect_queryset = defect_queryset.filter(shift=shift_filter)

        # Calculate total defects
        total_defects = defect_queryset.aggregate(
            total=Sum('qcr_defect_quantity')
        )['total'] or 0

        # Calculate defect variance (defect rate as percentage of offloading)
        defect_variance = round((total_defects / total_offloading * 100), 1) if total_offloading > 0 else 0

        # ========== WORKFORCE DATA ==========
        # Active workers (total employees with active status)
        # Note: activestatus is now IntegerField in model, but stored as 1/0 in DB
        active_workers = HangerlineEmp.objects.filter(activestatus=1).count()

        # Present workers (distinct employees who worked in the selected date range)
        present_workers = queryset.values('odp_em_key').distinct().count()

        # Attendance percentage
        attendance_percentage = round((present_workers / active_workers * 100), 1) if active_workers > 0 else 0

        # ========== BREAKDOWN DATA ==========
        # Use last 30 days for breakdown data (independent of main dashboard filters)
        end_date_30 = datetime.now().date()
        start_date_30 = end_date_30 - timedelta(days=60)

        breakdown_queryset = Breakdown.objects.filter(
            p_date__gte=start_date_30,
            p_date__lte=end_date_30
        )

        # Calculate total breakdown time
        total_breakdown = sum(b.breakdown_time_minutes for b in breakdown_queryset) or 0

        # Breakdown by category
        category_breakdown = breakdown_queryset.values('breakdown_category__name').annotate(
            total_time=Sum('loss_minutes')
        ).order_by('-total_time')

        breakdown_categories_labels = json.dumps([item['breakdown_category__name'] for item in category_breakdown] or ["No Data"])
        breakdown_categories_data = json.dumps([item['total_time'] or 0 for item in category_breakdown] or [0])

        # Breakdown by line
        line_breakdown = breakdown_queryset.values('line_no').annotate(
            total_time=Sum('loss_minutes')
        ).order_by('-total_time')

        breakdown_lines_labels = json.dumps([item['line_no'] for item in line_breakdown] or ["No Data"])
        breakdown_lines_data = json.dumps([item['total_time'] or 0 for item in line_breakdown] or [0])

        # ========== UNIFIED LINE-WISE DATA ==========
        # Create dictionaries for all metrics by line
        line_loading_dict = {
            item['source_connection']: item['total'] or 0
            for item in queryset.values('source_connection')
            .exclude(source_connection__isnull=True)
            .exclude(source_connection='')
            .annotate(total=Sum('loading_qty'))
        }

        line_offloading_dict = {
            item['source_connection']: {
                'offload_total': item['offload_total'] or 0,
                'load_total': item['load_total'] or 0
            }
            for item in queryset.values('source_connection')
            .exclude(source_connection__isnull=True)
            .exclude(source_connection='')
            .annotate(
                offload_total=Sum('unloading_qty'),
                load_total=Sum('loading_qty')
            )
        }

        # Get target data by line
        targets_by_line_dict = {
            item['source_connection']: item['target_qty'] or 0
            for item in target_queryset.values('source_connection').annotate(
                target_qty=Sum('total_target_qty')
            )
        }

        # Calculate efficiency using SQL query logic: article-wise → line-wise → total averaging

        # Get SMV data indexed by article (latest by applicabledate)
        smv_data = {}
        for op in Operationinformation.objects.filter(applicabledate__isnull=False).order_by('articleno', '-applicabledate'):
            if op.articleno and op.articleno not in smv_data:
                # Clean article number (remove suffix after - or _)
                article_key = op.articleno.split('-')[0].split('_')[0]
                smv_data[article_key] = {
                    'totalsmv': op.totalsmv or 0,
                    'conversionfactor': op.conversionfactor or 1
                }

        # Step 1: Calculate article-wise efficiencies (per date/line/style)
        article_efficiencies = []
        style_employee_counts = {}

        # Group production data by date, line, and style
        grouped_production = {}
        for prod in queryset:
            key = (prod.odp_date, prod.source_connection, prod.st_id or '')
            if key not in grouped_production:
                grouped_production[key] = {'offloading': 0, 'employees': set()}

            grouped_production[key]['offloading'] += prod.unloading_qty or 0
            if prod.odp_em_key and str(prod.odp_em_key).startswith('10613'):
                grouped_production[key]['employees'].add(prod.odp_em_key)

        # Calculate efficiency for each date/line/style group
        for (prod_date, source_conn, st_id), data in grouped_production.items():
            offloading_qty = data['offloading']
            employee_count = len(data['employees']) or 1

            if offloading_qty > 0:
                # Get SMV for this style using REGEXP_REPLACE pattern
                article_key = st_id.split('-')[0].split('_')[0] if st_id else ''
                smv_info = smv_data.get(article_key, {'totalsmv': 1.5, 'conversionfactor': 1.0})

                # Efficiency % = (SMV × Conversion Factor × Unloading Qty) / (Employee Count × 480) × 100
                produced_minutes = smv_info['totalsmv'] * smv_info['conversionfactor'] * offloading_qty
                available_minutes = employee_count * 480

                if available_minutes > 0:
                    efficiency_pct = round((produced_minutes / available_minutes) * 100, 2)
                    efficiency_pct = min(efficiency_pct, 200)  # Cap at reasonable maximum

                    article_efficiencies.append({
                        'date': prod_date,
                        'line': source_conn,
                        'style': st_id,
                        'efficiency': efficiency_pct,
                        'offloading': offloading_qty
                    })

        # Step 2: Calculate line-wise average efficiencies
        line_efficiency_data = {}
        for line in all_lines:
            line_articles = [art for art in article_efficiencies if art['line'] == line]
            if line_articles:
                # Weighted average by offloading quantity
                total_weighted_eff = sum(art['efficiency'] * art['offloading'] for art in line_articles)
                total_offloading = sum(art['offloading'] for art in line_articles)
                avg_efficiency = round(total_weighted_eff / total_offloading, 1) if total_offloading > 0 else 0
            else:
                avg_efficiency = 0

            line_efficiency_data[line] = avg_efficiency

        # Step 3: Calculate total average efficiency across all lines
        if line_efficiency_data:
            total_efficiency = round(sum(line_efficiency_data.values()) / len(line_efficiency_data), 1)
            print(f"DEBUG: Line efficiencies: {line_efficiency_data}")
            print(f"DEBUG: Total efficiency: {total_efficiency}%")
        else:
            total_efficiency = 0
            print("DEBUG: No line efficiency data available")

        # Create unified line performance data
        line_performance = []
        for line in all_lines:
            # Loading data
            loading_qty = line_loading_dict.get(line, 0)
            loading_pct = round(loading_qty / total_loading * 100, 1) if total_loading > 0 else 0

            # Offloading data
            offload_data = line_offloading_dict.get(line, {'offload_total': 0, 'load_total': 0})
            offloading_qty = offload_data['offload_total']
            load_for_eff = offload_data['load_total']
            offloading_pct = round(offloading_qty / total_offloading * 100, 1) if total_offloading > 0 else 0

            # Use calculated efficiency from SQL logic
            efficiency = line_efficiency_data.get(line, 0)

            # WIP data
            wip_qty = loading_qty - offloading_qty
            total_wip_calc = max(total_wip, 1)
            wip_pct = round(abs(wip_qty) / abs(total_wip_calc) * 100, 1) if total_wip != 0 else 0

            # Target data
            target_qty = targets_by_line_dict.get(line, 0)
            variance = offloading_qty - target_qty
            achievement_pct = round(offloading_qty / target_qty * 100, 1) if target_qty > 0 else 0

            line_performance.append({
                'line': line,
                'loading_qty': loading_qty,
                'loading_pct': loading_pct,
                'offloading_qty': offloading_qty,
                'offloading_pct': offloading_pct,
                'efficiency': line_efficiency_data.get(line, 0),
                'wip_qty': wip_qty,
                'wip_pct': min(wip_pct, 100),
                'target_qty': target_qty,
                'variance': variance,
                'achievement_pct': achievement_pct,
            })

        # Sort by total production (loading + offloading) descending
        line_performance.sort(key=lambda x: x['loading_qty'] + x['offloading_qty'], reverse=True)

    except Exception as e:
        # Database connection failed - use dynamic queries with empty result handling
        print(f"Database error: {e}, using dynamic queries with empty data handling")

        # Initialize all variables to handle empty data gracefully
        totals = {'total_loading': 0, 'total_offloading': 0, 'total_quantity': 0}
        total_loading = 0
        total_offloading = 0
        total_wip = 0
        line_count = 0
        shift_count = 0
        total_target = 0
        variance = 0
        variance_percent = 0
        achievement_percent = 0
        efficiency = 0

        # Get all lines from LineTarget (may be empty if no targets set)
        all_lines = []

        # Workforce data - will be 0 if no data
        active_workers = 0
        present_workers = 0
        attendance_percentage = 0

        # Defect data - will be 0 if no data
        total_defects = 0
        defect_variance = 0

        # Breakdown data - will be empty arrays if no data
        total_breakdown = 0
        breakdown_categories_labels = json.dumps([])
        breakdown_categories_data = json.dumps([])
        breakdown_lines_labels = json.dumps([])
        breakdown_lines_data = json.dumps([])

        # Line-wise data - will be empty lists if no data
        line_loading = []
        line_offloading = []
        line_wip = []
        line_targets = []

    context = {
        'title': 'Production Dashboard',
        'total_loading': total_loading,
        'total_offloading': total_offloading,
        'total_wip': total_wip,
        'total_quantity': totals['total_quantity'] or 0,
        'line_count': line_count,
        'shift_count': shift_count,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'current_month': start_date.strftime('%B %Y'),
        # Additional summary cards data
        'total_defects': total_defects,
        'defect_variance': defect_variance,
        'active_workers': active_workers,
        'present_workers': present_workers,
        'attendance_percentage': attendance_percentage,
        'total_target': total_target,
        'variance': variance,
        'variance_percent': variance_percent,
        'achievement_percent': achievement_percent,
        'total_breakdown': total_breakdown,
        'efficiency': total_efficiency,
        # Unified line performance data
        'line_performance': line_performance,
        # Breakdown chart data (JSON strings)
        'breakdown_categories_labels': breakdown_categories_labels,
        'breakdown_categories_data': breakdown_categories_data,
        'breakdown_lines_labels': breakdown_lines_labels,
        'breakdown_lines_data': breakdown_lines_data,
    }

    return render(request, 'admin/hangerline/django_dashboard.html', context)


def chart_data_by_shift(request):
    """API endpoint for shift summary data"""
    # Get date range from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    queryset = OperatorDailyPerformance.objects.all()

    if start_date:
        queryset = queryset.filter(odp_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(odp_date__lte=end_date)
    else:
        # Default: current date (same as main dashboard)
        today = datetime.now().date()
        start_date = today
        end_date = today
        queryset = queryset.filter(odp_date__gte=start_date, odp_date__lte=end_date)
    
    data = (
        queryset
        .values('shift')
        .exclude(shift__isnull=True)
        .exclude(shift='')
        .annotate(
            total_loading=Sum('loading_qty'),
            total_unloading=Sum('unloading_qty'),
            total_wip=Sum('loading_qty') - Sum('unloading_qty')
        )
        .order_by('shift')
    )
    
    labels = [d['shift'] for d in data]
    loading = [d['total_loading'] or 0 for d in data]
    unloading = [d['total_unloading'] or 0 for d in data]
    wip = [(d['total_loading'] or 0) - (d['total_unloading'] or 0) for d in data]
    
    return JsonResponse({
        'labels': labels,
        'datasets': [
            {'label': 'Loading', 'data': loading, 'backgroundColor': 'rgba(54, 162, 235, 0.8)', 'stack': 'Stack 0'},
            {'label': 'Offloading', 'data': unloading, 'backgroundColor': 'rgba(255, 99, 132, 0.8)', 'stack': 'Stack 0'},
            {'label': 'WIP', 'data': wip, 'backgroundColor': 'rgba(255, 206, 86, 0.8)', 'stack': 'Stack 0'},
        ]
    })


@staff_member_required
def chart_data_by_source(request):
    """API endpoint for source connection summary data"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    queryset = OperatorDailyPerformance.objects.all()

    if start_date:
        queryset = queryset.filter(odp_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(odp_date__lte=end_date)
    else:
        # Default: current date (same as main dashboard)
        today = datetime.now().date()
        start_date = today
        end_date = today
        queryset = queryset.filter(odp_date__gte=start_date, odp_date__lte=end_date)
    
    data = (
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
    
    labels = [d['source_connection'] for d in data]
    loading = [d['total_loading'] or 0 for d in data]
    unloading = [d['total_unloading'] or 0 for d in data]
    wip = [(d['total_loading'] or 0) - (d['total_unloading'] or 0) for d in data]
    
    return JsonResponse({
        'labels': labels,
        'datasets': [
            {'label': 'Loading', 'data': loading, 'backgroundColor': 'rgba(54, 162, 235, 0.8)', 'stack': 'Stack 0'},
            {'label': 'Offloading', 'data': unloading, 'backgroundColor': 'rgba(255, 99, 132, 0.8)', 'stack': 'Stack 0'},
            {'label': 'WIP', 'data': wip, 'backgroundColor': 'rgba(255, 206, 86, 0.8)', 'stack': 'Stack 0'},
        ]
    })


@staff_member_required
def chart_data_by_production(request):
    """API endpoint for production category summary data"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    queryset = OperatorDailyPerformance.objects.all()

    if start_date:
        queryset = queryset.filter(odp_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(odp_date__lte=end_date)
    else:
        # Default: current date (same as main dashboard)
        today = datetime.now().date()
        start_date = today
        end_date = today
        queryset = queryset.filter(odp_date__gte=start_date, odp_date__lte=end_date)
    
    # Production categories
    categories = {
        'Loading': queryset.filter(oc_description='Loading/Panel Segregation').aggregate(total=Sum('odpd_quantity'))['total'] or 0,
        'Offloading': queryset.filter(oc_description='Garment Insert in Poly Bag & Close').aggregate(total=Sum('odpd_quantity'))['total'] or 0,
        'QC(midline)': queryset.filter(oc_description__icontains='midline').aggregate(total=Sum('odpd_quantity'))['total'] or 0,
        'QC(endline)': queryset.filter(oc_description__icontains='endline').aggregate(total=Sum('odpd_quantity'))['total'] or 0,
        'QC(final)': queryset.filter(oc_description__icontains='final').aggregate(total=Sum('odpd_quantity'))['total'] or 0,
    }
    
    labels = list(categories.keys())
    values = list(categories.values())
    
    colors = [
        'rgba(102, 126, 234, 0.8)',  # Purple for Loading (matches Total Loading stat card)
        'rgba(240, 147, 251, 0.8)',  # Pink/Red for Offloading (matches Total Offloading stat card)
        'rgba(255, 206, 86, 0.7)',   # Yellow for QC(midline)
        'rgba(75, 192, 192, 0.7)',   # Teal for QC(endline)
        'rgba(153, 102, 255, 0.7)',  # Purple variant for QC(final)
    ]
    
    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': 'Quantity',
            'data': values,
            'backgroundColor': colors,
        }]
    })


@staff_member_required
def chart_data_line(request):
    """API endpoint for daily trend line chart"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    queryset = OperatorDailyPerformance.objects.all()

    # if start_date:
    #     queryset = queryset.filter(odp_date__gte=start_date)
    # if end_date:
    #     queryset = queryset.filter(odp_date__lte=end_date)
    # else:
        # Default: last 30 days
    end = datetime.now().date()
    start = end - timedelta(days=30)
    queryset = queryset.filter(odp_date__gte=start, odp_date__lte=end)

    data = (
        queryset
        .values('odp_date')
        .annotate(
            total_loading=Sum('loading_qty'),
            total_unloading=Sum('unloading_qty'),
            # total_quantity=Sum('odpd_quantity')
        )
        .order_by('odp_date')
    )

    labels = [d['odp_date'].strftime('%Y-%m-%d') for d in data]
    loading = [d['total_loading'] or 0 for d in data]
    unloading = [d['total_unloading'] or 0 for d in data]
    wip = [(d['total_loading'] or 0) - (d['total_unloading'] or 0) for d in data]

    return JsonResponse({
        'labels': labels,
        'datasets': [
            {'label': 'Loading', 'data': loading, 'borderColor': 'rgba(54, 162, 235, 1)', 'fill': False},
            {'label': 'Offloading', 'data': unloading, 'borderColor': 'rgba(255, 99, 132, 1)', 'fill': False},
            {'label': 'WIP', 'data': wip, 'borderColor': 'rgba(255, 206, 86, 1)', 'fill': False},
        ]
    })


@staff_member_required
def chart_data_by_line_offloading(request):
    """API endpoint for line-wise offloading summary with percentages"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    queryset = OperatorDailyPerformance.objects.all()

    if start_date:
        queryset = queryset.filter(odp_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(odp_date__lte=end_date)
    else:
        # Default: current date (same as main dashboard)
        today = datetime.now().date()
        start_date = today
        end_date = today
        queryset = queryset.filter(odp_date__gte=start_date, odp_date__lte=end_date)

    data = (
        queryset
        .values('source_connection')
        .exclude(source_connection__isnull=True)
        .exclude(source_connection='')
        .annotate(
            total_offloading=Sum('unloading_qty')
        )
        .order_by('-total_offloading')
    )

    # Calculate total offloading for percentages
    total_offloading = sum(d['total_offloading'] or 0 for d in data)

    labels = [d['source_connection'] for d in data]
    values = [d['total_offloading'] or 0 for d in data]
    percentages = [(v / total_offloading * 100) if total_offloading > 0 else 0 for v in values]

    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': 'Offloading Sum',
            'data': values,
            'backgroundColor': [
                'rgba(52, 152, 219, 0.8)',
                'rgba(231, 76, 60, 0.8)',
                'rgba(46, 204, 113, 0.8)',
                'rgba(155, 89, 182, 0.8)',
                'rgba(243, 156, 18, 0.8)',
                'rgba(26, 188, 156, 0.8)',
                'rgba(149, 165, 166, 0.8)',
                'rgba(44, 62, 80, 0.8)',
            ],
            'borderColor': [
                'rgba(52, 152, 219, 1)',
                'rgba(231, 76, 60, 1)',
                'rgba(46, 204, 113, 1)',
                'rgba(155, 89, 182, 1)',
                'rgba(243, 156, 18, 1)',
                'rgba(26, 188, 156, 1)',
                'rgba(149, 165, 166, 1)',
                'rgba(44, 62, 80, 1)',
            ],
            'borderWidth': 2,
            'borderRadius': 8,
            'borderSkipped': False,
        }],
        'percentages': percentages,
        'total_offloading': total_offloading
    })


@staff_member_required
def chart_data_by_line_loading(request):
    """API endpoint for line-wise loading summary with percentages"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    queryset = OperatorDailyPerformance.objects.all()

    if start_date:
        queryset = queryset.filter(odp_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(odp_date__lte=end_date)
    else:
        # Default: current date (same as main dashboard)
        today = datetime.now().date()
        start_date = today
        end_date = today
        queryset = queryset.filter(odp_date__gte=start_date, odp_date__lte=end_date)

    data = (
        queryset
        .values('source_connection')
        .exclude(source_connection__isnull=True)
        .exclude(source_connection='')
        .annotate(
            total_loading=Sum('loading_qty')
        )
        .order_by('-total_loading')
    )

    # Calculate total loading for percentages
    total_loading = sum(d['total_loading'] or 0 for d in data)

    labels = [d['source_connection'] for d in data]
    values = [d['total_loading'] or 0 for d in data]
    percentages = [(v / total_loading * 100) if total_loading > 0 else 0 for v in values]

    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': 'Loading Sum',
            'data': values,
            'backgroundColor': [
                'rgba(52, 152, 219, 0.8)',
                'rgba(231, 76, 60, 0.8)',
                'rgba(46, 204, 113, 0.8)',
                'rgba(155, 89, 182, 0.8)',
                'rgba(243, 156, 18, 0.8)',
                'rgba(26, 188, 156, 0.8)',
                'rgba(149, 165, 166, 0.8)',
                'rgba(44, 62, 80, 0.8)',
            ],
            'borderColor': [
                'rgba(52, 152, 219, 1)',
                'rgba(231, 76, 60, 1)',
                'rgba(46, 204, 113, 1)',
                'rgba(155, 89, 182, 1)',
                'rgba(243, 156, 18, 1)',
                'rgba(26, 188, 156, 1)',
                'rgba(149, 165, 166, 1)',
                'rgba(44, 62, 80, 1)',
            ],
            'borderWidth': 2,
            'borderRadius': 8,
            'borderSkipped': False,
        }],
        'percentages': percentages,
        'total_loading': total_loading
    })


@staff_member_required
def chart_data_line_target_summary(request):
    """API endpoint for line target summary data"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    queryset = LineTarget.objects.all()

    if start_date:
        queryset = queryset.filter(target_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(target_date__lte=end_date)
    else:
        # Default: last 90 days (same as main dashboard)
        today = datetime.now().date()
        start_date = today - timedelta(days=90)
        end_date = today
        queryset = queryset.filter(target_date__gte=start_date, target_date__lte=end_date)

    # Aggregate line target data
    targets_data = queryset.aggregate(
        total_targets=Sum('total_target_qty'),
        target_lines=Count('id')
    )

    # Get actual offloading data for the same period
    odp_queryset = OperatorDailyPerformance.objects.all()
    if start_date:
        odp_queryset = odp_queryset.filter(odp_date__gte=start_date)
    if end_date:
        odp_queryset = odp_queryset.filter(odp_date__lte=end_date)
    else:
        # Default: current date (same as main dashboard)
        today = datetime.now().date()
        start_date = today
        end_date = today
        odp_queryset = odp_queryset.filter(odp_date__gte=start_date, odp_date__lte=end_date)

    actual_data = odp_queryset.aggregate(
        total_offloading=Sum('unloading_qty')
    )

    # Calculate variance and achievement rate
    target_qty = targets_data['total_targets'] or 0
    offloading_qty = actual_data['total_offloading'] or 0
    variance = target_qty - offloading_qty
    achievement_rate = (offloading_qty / target_qty * 100) if target_qty > 0 else 0

    return JsonResponse({
        'total_targets': target_qty,
        'total_offloading': offloading_qty,
        'variance': variance,
        'achievement_rate': round(achievement_rate, 1),
        'target_lines': targets_data['target_lines'] or 0,
    })


@staff_member_required
def chart_data_line_wise_targets(request):
    """API endpoint for line-wise target summary with percentages"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Get line targets
    target_queryset = LineTarget.objects.all()
    if start_date:
        target_queryset = target_queryset.filter(target_date__gte=start_date)
    if end_date:
        target_queryset = target_queryset.filter(target_date__lte=end_date)
    else:
        # Default: current date (same as main dashboard)
        today = datetime.now().date()
        start_date = today
        end_date = today
        target_queryset = target_queryset.filter(target_date__gte=start_date, target_date__lte=end_date)

    # Get actual offloading by line
    odp_queryset = OperatorDailyPerformance.objects.all()
    if start_date:
        odp_queryset = odp_queryset.filter(odp_date__gte=start_date)
    if end_date:
        odp_queryset = odp_queryset.filter(odp_date__lte=end_date)
    else:
        # Default: current date (same as main dashboard)
        today = datetime.now().date()
        start_date = today
        end_date = today
        odp_queryset = odp_queryset.filter(odp_date__gte=start_date, odp_date__lte=end_date)

    # Aggregate targets by line
    targets_by_line = target_queryset.values('source_connection').annotate(
        target_qty=Sum('total_target_qty')
    ).order_by('source_connection')

    # Aggregate actual offloading by line
    offloading_by_line = odp_queryset.values('source_connection').annotate(
        actual_qty=Sum('unloading_qty')
    ).order_by('source_connection')

    # Calculate total target quantity
    total_target_qty = sum(item['target_qty'] for item in targets_by_line)

    # Create a map for quick lookup
    offloading_map = {item['source_connection']: item['actual_qty'] for item in offloading_by_line}

    # Combine data
    result_data = []
    for target_item in targets_by_line:
        line = target_item['source_connection']
        target_qty = target_item['target_qty'] or 0
        actual_qty = offloading_map.get(line, 0)

        # Calculate percentages
        target_percentage = (target_qty / total_target_qty * 100) if total_target_qty > 0 else 0
        achievement_rate = (actual_qty / target_qty * 100) if target_qty > 0 else 0

        result_data.append({
            'line': line,
            'target_qty': target_qty,
            'actual_qty': actual_qty,
            'target_percentage': round(target_percentage, 1),
            'achievement_rate': round(achievement_rate, 1)
        })

    return JsonResponse({
        'data': result_data,
        'total_target_qty': total_target_qty
    })


def breakdown_dashboard(request):
    """Breakdown dashboard view with summary cards and charts"""
    from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, fields
    from django.db.models.functions import Extract
    from datetime import datetime, date
    import json

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

    context = {
        'title': 'Breakdown Dashboard',
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
        'has_permission': True,  # Default to True for dashboard access
    }

    return render(request, 'admin/hangerline/breakdown/dashboard.html', context)
