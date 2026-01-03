from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from .models import OperatorDailyPerformance, LineTarget
# from .batch_api import fetch_batch_no


def dashboard(request):
    """Main dashboard view with summary cards and charts"""
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

    # Default to current month if no dates provided
    if not start_date or not end_date:
        today = datetime.now().date()
        # current_month = today.replace(day=1)
        # next_month = (current_month.replace(month=current_month.month % 12 + 1, year=current_month.year + (current_month.month // 12))).replace(day=1)
        start_date = today
        # end_date = next_month
        end_date = datetime.now().date()

    # Get summary statistics
    queryset = OperatorDailyPerformance.objects.filter(
        odp_date__gte=start_date,
        odp_date__lt=end_date
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
        target_date__lt=end_date
    )
    if line_filter:
        target_queryset = target_queryset.filter(source_connection=line_filter)
    
    # Get total target
    total_target = target_queryset.aggregate(total=Sum('total_target_qty'))['total'] or 0
    
    # Calculate variance (target - offloading)
    variance = total_offloading - total_target
    variance_percent = round((variance / total_target * 100), 1) if total_target > 0 else 0
    
    # Achievement percentage
    achievement_percent = round((total_offloading / total_target * 100), 1) if total_target > 0 else 0
    
    # Efficiency (offloading / loading * 100)
    efficiency = round((total_offloading / total_loading * 100), 1) if total_loading > 0 else 0

    # ========== LINE-WISE DATA ==========
    # Line-wise Loading
    line_loading_data = (
        queryset
        .values('source_connection')
        .exclude(source_connection__isnull=True)
        .exclude(source_connection='')
        .annotate(total=Sum('loading_qty'))
        .order_by('-total')
    )
    line_loading = []
    for item in line_loading_data:
        pct = round((item['total'] or 0) / total_loading * 100, 1) if total_loading > 0 else 0
        line_loading.append({
            'line': item['source_connection'],
            'qty': item['total'] or 0,
            'percent': pct
        })

    # Line-wise Offloading
    line_offloading_data = (
        queryset
        .values('source_connection')
        .exclude(source_connection__isnull=True)
        .exclude(source_connection='')
        .annotate(
            offload_total=Sum('unloading_qty'),
            load_total=Sum('loading_qty')
        )
        .order_by('-offload_total')
    )
    line_offloading = []
    for item in line_offloading_data:
        offload = item['offload_total'] or 0
        load = item['load_total'] or 0
        pct = round(offload / total_offloading * 100, 1) if total_offloading > 0 else 0
        eff = round(offload / load * 100, 1) if load > 0 else 0
        line_offloading.append({
            'line': item['source_connection'],
            'qty': offload,
            'percent': pct,
            'efficiency': eff
        })

    # Line-wise WIP
    line_wip_data = (
        queryset
        .values('source_connection')
        .exclude(source_connection__isnull=True)
        .exclude(source_connection='')
        .annotate(
            load_total=Sum('loading_qty'),
            offload_total=Sum('unloading_qty')
        )
        .order_by('source_connection')
    )
    line_wip = []
    total_wip_calc = max(total_wip, 1)  # Avoid division by zero
    for item in line_wip_data:
        load = item['load_total'] or 0
        offload = item['offload_total'] or 0
        wip = load - offload
        pct = round(abs(wip) / abs(total_wip_calc) * 100, 1) if total_wip != 0 else 0
        line_wip.append({
            'line': item['source_connection'],
            'qty': wip,
            'percent': min(pct, 100)  # Cap at 100%
        })

    # Line-wise Targets vs Achievement
    targets_by_line = target_queryset.values('source_connection').annotate(
        target_qty=Sum('total_target_qty')
    ).order_by('source_connection')
    
    offloading_by_line_map = {
        item['source_connection']: item['offload_total'] or 0 
        for item in line_offloading_data
    }
    
    line_targets = []
    for item in targets_by_line:
        line = item['source_connection']
        target = item['target_qty'] or 0
        achieved = offloading_by_line_map.get(line, 0)
        var = achieved - target
        pct = round(achieved / target * 100, 1) if target > 0 else 0
        line_targets.append({
            'line': line,
            'target': target,
            'achieved': achieved,
            'variance': var,
            'percent': pct
        })

    # ========== BREAKDOWN DATA (sample/placeholder) ==========
    # Since we don't have a Breakdown model, we'll provide sample data
    # In production, this should be replaced with actual breakdown data
    breakdown_categories_labels = json.dumps(["Mechanical", "Electrical", "Material", "Operator", "Other"])
    breakdown_categories_data = json.dumps([30, 25, 20, 15, 10])
    breakdown_lines_labels = json.dumps([item['source_connection'] for item in line_loading_data[:8]])
    breakdown_lines_data = json.dumps([10, 15, 12, 8, 20, 18, 14, 16][:len(line_loading_data)])
    
    # Total breakdown (sample - replace with actual data)
    total_breakdown = 120  # minutes

    # Total defects (sample - replace with actual data)
    total_defects = 0
    defect_variance = 0

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
        'total_target': total_target,
        'variance': variance,
        'variance_percent': variance_percent,
        'achievement_percent': achievement_percent,
        'total_breakdown': total_breakdown,
        'efficiency': efficiency,
        # Line-wise data
        'line_loading': line_loading,
        'line_offloading': line_offloading,
        'line_wip': line_wip,
        'line_targets': line_targets,
        # Breakdown chart data (JSON strings)
        'breakdown_categories_labels': breakdown_categories_labels,
        'breakdown_categories_data': breakdown_categories_data,
        'breakdown_lines_labels': breakdown_lines_labels,
        'breakdown_lines_data': breakdown_lines_data,
    }

    return render(request, 'admin/hangerline/dashboard.html', context)


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
        # Default: current month
        now = datetime.now()
        queryset = queryset.filter(odp_date__year=now.year, odp_date__month=now.month)
    
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
        now = datetime.now()
        queryset = queryset.filter(odp_date__year=now.year, odp_date__month=now.month)
    
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
        now = datetime.now()
        queryset = queryset.filter(odp_date__year=now.year, odp_date__month=now.month)
    
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
        now = datetime.now()
        queryset = queryset.filter(odp_date__year=now.year, odp_date__month=now.month)

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
        now = datetime.now()
        queryset = queryset.filter(odp_date__year=now.year, odp_date__month=now.month)

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
        # Default: current month
        now = datetime.now()
        queryset = queryset.filter(target_date__year=now.year, target_date__month=now.month)

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
        now = datetime.now()
        odp_queryset = odp_queryset.filter(odp_date__year=now.year, odp_date__month=now.month)

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
        now = datetime.now()
        target_queryset = target_queryset.filter(target_date__year=now.year, target_date__month=now.month)

    # Get actual offloading by line
    odp_queryset = OperatorDailyPerformance.objects.all()
    if start_date:
        odp_queryset = odp_queryset.filter(odp_date__gte=start_date)
    if end_date:
        odp_queryset = odp_queryset.filter(odp_date__lte=end_date)
    else:
        now = datetime.now()
        odp_queryset = odp_queryset.filter(odp_date__year=now.year, odp_date__month=now.month)

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
