from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import LineTarget, LineTargetDetail


@receiver([post_save, post_delete], sender=LineTargetDetail)
def update_line_target_total(sender, instance, **kwargs):
    """
    Signal handler to update total_target_qty in LineTarget whenever
    LineTargetDetail records are created, updated, or deleted.
    """
    # Get the related LineTarget
    line_target = instance.linetarget

    # Calculate the sum of all target_qty from related LineTargetDetail instances
    total_qty = LineTargetDetail.objects.filter(linetarget=line_target).aggregate(
        total=Sum('target_qty')
    )['total'] or 0

    # Update the total_target_qty field
    line_target.total_target_qty = total_qty
    line_target.save(update_fields=['total_target_qty'])
