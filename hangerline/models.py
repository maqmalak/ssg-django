# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TransferToPacking(models.Model):
    id = models.AutoField(primary_key=True)
    dated = models.DateTimeField(blank=True, null=True, verbose_name='Date')
    proddate = models.DateField(blank=True, null=True, verbose_name='Production Date')
    scrvoucher_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='SCR Voucher No')
    transferfromdepartment_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Transfer From Department ID')
    from_dept_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='From Department Name')
    transfertodepartment_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Transfer To Department ID')
    to_dept_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='To Department Name')
    pono = models.CharField(max_length=50, blank=True, null=True, verbose_name='PO No')
    articleno = models.CharField(max_length=50, blank=True, null=True, verbose_name='Article No')
    mcolour = models.CharField(max_length=50, blank=True, null=True, verbose_name='Color')
    size = models.CharField(max_length=50, blank=True, null=True, verbose_name='Size')
    item_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Item ID')
    item_title = models.TextField(max_length=200, blank=True, null=True, verbose_name='Item Title')
    qtytransferred = models.IntegerField(blank=True, null=True, verbose_name='Quantity Transferred')
    refqty = models.IntegerField(blank=True, null=True, verbose_name='Reference Quantity')
    line_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='Line ID')
    line_desc = models.CharField(max_length=100, blank=True, null=True, verbose_name='Line Description')
    bundleno = models.BigIntegerField(blank=True, null=True, verbose_name='Bundle No')

    class Meta:
        managed = False
        db_table = 'transfertopacking'
        verbose_name = 'Transfer to Packing'
        verbose_name_plural = 'Transfer to Packing'
        ordering = ['-dated']

    def __str__(self):
        return f"Transfer {self.id} - {self.pono} - {self.item_title}"


class Article(models.Model):
    id = models.CharField(blank=False, null=False,primary_key=True)
    fg_articleno = models.CharField(blank=True, null=True)
    basearticleno = models.CharField(blank=True, null=True)
    tis_styledescription = models.CharField(blank=True, null=True)
    tis_stylecollection = models.CharField(blank=True, null=True)
    category_id = models.CharField(blank=True, null=True)
    tis_stylesize = models.CharField(blank=True, null=True)
    tis_stylecolour = models.CharField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'article'


class EtlExtractLog(models.Model):
    extractlogid = models.AutoField(primary_key=True)
    processlogid = models.CharField(max_length=100, blank=True, null=True)
    source_connection = models.CharField(max_length=255, blank=True, null=True)
    saved_count = models.IntegerField(blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    lastextractdatetime = models.DateTimeField(blank=True, null=True)
    success = models.BooleanField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    errormessage = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'etl_extract_log'


class EtlQcrExtractLog(models.Model):
    extractlogid = models.AutoField(primary_key=True)
    processlogid = models.CharField(max_length=100, blank=True, null=True)
    source_connection = models.CharField(max_length=255, blank=True, null=True)
    saved_count = models.IntegerField(blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    lastextractdatetime = models.DateTimeField(blank=True, null=True)
    success = models.BooleanField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    errormessage = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'etl_qcr_extract_log'


class HangerlineEmp(models.Model):
    id = models.IntegerField(blank=False, null=False,primary_key=True)
    emp_id = models.CharField(blank=True, null=False)
    title = models.CharField(max_length=100, null=True)
    fathername = models.CharField(max_length=100, null=True)
    desig_id = models.CharField(max_length=100, null=True)
    # deptt_id = models.DateTimeField(blank=True, null=True)
    current_line_id = models.CharField(max_length=100, null=True)
    latest_line_id = models.CharField(max_length=100, null=True)
    line_desc = models.CharField(max_length=100, null=True)
    assignment_date = models.DateTimeField(blank=True, null=True)
    shift = models.CharField(max_length=100, null=True)
    location_id = models.BigIntegerField(blank=True, null=True)
    joindate = models.DateTimeField(blank=True, null=True)
    resigndate = models.FloatField(blank=True, null=True)
    nic = models.CharField(max_length=100, null=True)
    add1 = models.TextField(blank=True, null=True)
    mobile = models.CharField(blank=True, null=True)
    activestatus = models.BooleanField(blank=True, null=True)
    gender_choice = [
        ('M', 'Male'),
        ('F','Female')
    ]
    gender = models.CharField(blank=True, null=True,choices=gender_choice)

    class Meta:
        managed = False
        db_table = 'hangerline_emp'

    def __str__(self):
        return f"{self.id} - {self.title}"
    
class Loadinginformation(models.Model):
    # id = models.TextField(blank=True, null=True)
    dated = models.DateTimeField(blank=True, null=True, verbose_name='Date',default=None)
    # scrvoucher_no = models.CharField(max_length=20, blank=True, null=True, verbose_name='SCR Voucher No')

    id = models.CharField(max_length=20, blank=True, null=True, verbose_name='SCR Voucher No',db_column='scrvoucher_no')
    barcode = models.BigIntegerField(primary_key=True, verbose_name='Barcode')
    maindeptt_id = models.CharField(blank=True, null=True, verbose_name='Main Dept ID')
    pono = models.CharField(blank=True, null=True, verbose_name='PO No',default=None)
    item_id = models.CharField(blank=True, null=True, verbose_name='Item ID')
    line_desc = models.CharField(max_length=10, blank=True, null=True, verbose_name='Line ID')
    title = models.TextField(blank=True, null=True, verbose_name='Title')
    model = models.CharField(blank=True, null=True, verbose_name='Model')
    fg_articleno = models.CharField(blank=True, null=True, verbose_name='FG Article No')
    # fg_colour = models.CharField(blank=True, null=True, verbose_name='FG Colour')
    # fg_size = models.CharField(blank=True, null=True, verbose_name='FG Size')
    bundleno = models.BigIntegerField(blank=True, null=True, verbose_name='Bundle No')
    qty = models.FloatField(blank=True, null=True, verbose_name='Quantity')

    class Meta:
        managed = False
        db_table = 'loadinginformation'
        verbose_name = 'Loading Information'
        verbose_name_plural = 'Loading Information'
        ordering = ['-dated']

    def __str__(self):
        return f"{self.id} "

class Operationinformation(models.Model):
    maindeptt_id = models.BigIntegerField(blank=True, null=True)
    applicabledate = models.DateTimeField(blank=True, null=True)
    basearticleno = models.TextField(blank=True, null=True)
    articleno = models.TextField(blank=True, null=True)
    conversionfactor = models.FloatField(blank=True, null=True)
    mnth = models.BigIntegerField(blank=True, null=True)
    vno = models.BigIntegerField(blank=True, null=True)
    dated = models.DateTimeField(blank=True, null=True)
    suboperation_id = models.TextField(blank=True, null=True)
    totalsmv = models.FloatField(blank=True, null=True)
    smv = models.FloatField(blank=True, null=True)
    machine = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operationinformation'


class OperatorDailyPerformance(models.Model):
    odp_key = models.CharField(max_length=50, blank=True, null=True)
    odp_date = models.DateField(blank=True, null=True)
    shift = models.CharField(max_length=10, blank=True, null=True)
    odp_em_key = models.IntegerField(blank=True, null=True)
    em_rfid = models.CharField(max_length=50, blank=True, null=True)
    em_department = models.CharField(max_length=100, blank=True, null=True)
    em_firstname = models.CharField(max_length=100, blank=True, null=True)
    em_lastname = models.CharField(max_length=100, blank=True, null=True)
    odp_actual_clock_in = models.DateTimeField(blank=True, null=True)
    odp_actual_clock_out = models.DateTimeField(blank=True, null=True)
    odp_shift_clock_in = models.DateTimeField(blank=True, null=True)
    odp_shift_clock_out = models.DateTimeField(blank=True, null=True)
    odp_first_hanger_time = models.DateTimeField(blank=True, null=True)
    odp_last_hanger_time = models.DateTimeField(blank=True, null=True)
    odp_current_station = models.CharField(max_length=100, blank=True, null=True)
    odp_lump_sum_payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    odp_make_up_pay_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    odp_last_hanger_start_time = models.DateTimeField(blank=True, null=True)
    odpd_key = models.CharField(max_length=50)
    odpd_workstation = models.CharField(max_length=50, blank=True, null=True)
    odpd_wc_key = models.IntegerField(blank=True, null=True)
    odpd_quantity = models.IntegerField(blank=True, null=True)
    odpd_st_key = models.CharField(max_length=50, blank=True, null=True)
    st_id = models.CharField(max_length=50, blank=True, null=True)
    st_description = models.CharField(max_length=100, blank=True, null=True)
    odpd_lot_number = models.CharField(max_length=50, blank=True, null=True)
    odpd_oc_key = models.CharField(max_length=10, blank=True, null=True)
    oc_description = models.CharField(max_length=100, blank=True, null=True)
    loading_qty = models.IntegerField(blank=True, null=True)
    unloading_qty = models.IntegerField(blank=True, null=True)
    oc_piece_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    oc_standard_time = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    odpd_standard = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    odpd_actual_time = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    odpd_pa_key = models.IntegerField(blank=True, null=True)
    odpd_pay_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    odpd_piece_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    odpd_start_time = models.DateTimeField(blank=True, null=True)
    odpd_cm_key = models.CharField(max_length=10, blank=True, null=True)
    cm_description = models.CharField(max_length=100, blank=True, null=True)
    odpd_sm_key = models.CharField(max_length=10, blank=True, null=True)
    sm_description = models.CharField(max_length=100, blank=True, null=True)
    odpd_normal_pay_factor = models.FloatField(blank=True, null=True)
    odpd_is_overtime = models.BooleanField(blank=True, null=True)
    odpd_overtime_factor = models.FloatField(blank=True, null=True)
    odpd_edited_by = models.CharField(max_length=50, blank=True, null=True)
    odpd_edited_date = models.DateTimeField(blank=True, null=True)
    odpd_actual_time_from_reader = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    odpd_stpo_key = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    source_connection = models.CharField(max_length=50, blank=True, null=True)
    # fg_item_key = models.CharField(max_length=50, blank=True, null=True)
    efficiency = models.FloatField(blank=True, null=True)
    ppd_tvwh = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operator_daily_performance'
        unique_together = (('source_connection', 'odp_key', 'odpd_key'),)



class QualityControlRepair(models.Model):
    qcr_key = models.CharField(max_length=36)
    qcr_stpo_key = models.IntegerField(blank=True, null=True)
    qcr_defect_datetime = models.DateTimeField(blank=True, null=True)
    qcr_date = models.DateField(blank=True, null=True)
    shift = models.CharField(max_length=10, blank=True, null=True)
    qcr_defect_em_key = models.IntegerField(blank=True, null=True)
    defect_em_firstname = models.CharField(max_length=100, blank=True, null=True)
    defect_em_lastname = models.CharField(max_length=100, blank=True, null=True)
    defect_em_rfid = models.CharField(max_length=50, blank=True, null=True)
    qcr_defect_st_key = models.IntegerField(blank=True, null=True)
    qcr_defect_oc_key = models.IntegerField(blank=True, null=True)
    oc_description = models.CharField(max_length=255, blank=True, null=True)
    qcr_sent_to_rework_by_em_key = models.IntegerField(blank=True, null=True)
    qcr_defect_quantity = models.IntegerField(blank=True, null=True)
    qcr_from_qc_station = models.CharField(max_length=50, blank=True, null=True)
    qcr_hm_id = models.CharField(max_length=50, blank=True, null=True)
    qcr_qc_datetime = models.DateTimeField(blank=True, null=True)
    qcr_repair_em_key = models.IntegerField(blank=True, null=True)
    em_repair_lastname = models.CharField(max_length=100, blank=True, null=True)
    qcr_repair_datetime = models.DateTimeField(blank=True, null=True)
    qcr_repair_quantity = models.IntegerField(blank=True, null=True)
    qcr_defect_cm_key = models.IntegerField(blank=True, null=True)
    cm_description = models.CharField(max_length=100, blank=True, null=True)
    qcr_defect_sm_key = models.IntegerField(blank=True, null=True)
    sm_description = models.CharField(max_length=100, blank=True, null=True)
    qcr_qcsc_key = models.CharField(max_length=36, blank=True, null=True)
    qcr_hm_key = models.IntegerField(blank=True, null=True)
    qcsc_description = models.CharField(max_length=100, blank=True, null=True)
    em_repair_firstname = models.CharField(max_length=100, blank=True, null=True)
    em_repair_key = models.IntegerField(blank=True, null=True)
    em_repair_rfid = models.CharField(max_length=50, blank=True, null=True)
    st_id = models.CharField(max_length=50, blank=True, null=True)
    st_description = models.CharField(max_length=100, blank=True, null=True)
    stpo_st_key = models.IntegerField(blank=True, null=True)
    stpo_id = models.CharField(max_length=50, blank=True, null=True)
    stpo_ci_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    source_connection = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quality_control_repair'
        unique_together = (('qcr_key', 'source_connection'),)


class Stylebasicinformation(models.Model):
    fg_articleno = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    hscode_id = models.FloatField(blank=True, null=True)
    rmvendor_id = models.BigIntegerField(blank=True, null=True)
    creationdate = models.DateTimeField(blank=True, null=True)
    fg_season = models.BigIntegerField(blank=True, null=True)
    picentryno = models.FloatField(blank=True, null=True)
    category_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stylebasicinformation'


class Size(models.Model):
    sm_key = models.CharField(max_length=4, primary_key=True, verbose_name='Size Key')
    sm_description = models.CharField(max_length=50, verbose_name='Size Description')

    class Meta:
        managed = True
        db_table = 'size'
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'
        ordering = ['sm_key']

    def __str__(self):
        return f"{self.sm_key} "


class Color(models.Model):
    cm_key = models.CharField(max_length=4, primary_key=True, verbose_name='Color Key')
    cm_short_description = models.CharField(max_length=50, verbose_name='Color Short Description')
    cm_description = models.CharField(max_length=100, verbose_name='Color Description')

    class Meta:
        managed = True
        db_table = 'color'
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
        ordering = ['cm_key']

    def __str__(self):
        return f"{self.cm_key}"


class Style(models.Model):
    style_key = models.CharField(max_length=50, primary_key=True, verbose_name='Style Key')
    style_description = models.CharField(max_length=100, verbose_name='Style Description')

    class Meta:
        managed = True
        db_table = 'style'
        verbose_name = 'Style'
        verbose_name_plural = 'Styles'
        ordering = ['style_key']

    def __str__(self):
        return f"{self.style_key}"



class LineTarget(models.Model):
    LINE_CHOICES = [
        ('line-21', 'Line-21'),
        ('line-22', 'Line-22'),
        ('line-23', 'Line-23'),
        ('line-24', 'Line-24'),
        ('line-25', 'Line-25'),
        ('line-26', 'Line-26'),
        ('line-27', 'Line-27'),
        ('line-28', 'Line-28'),
        ('line-29', 'Line-29'),
        ('line-30', 'Line-30'),
        ('line-31', 'Line-31'),
        ('line-32', 'Line-32'),
    ]

    SHIFT_CHOICES = [
        ('Day', 'Day'),
        ('Night', 'Night'),
    ]

    source_connection = models.CharField(max_length=10, choices=LINE_CHOICES, verbose_name='Line')
    target_date = models.DateField(verbose_name='Target Date')
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, verbose_name='Shift')
    total_target_qty = models.IntegerField(default=0, verbose_name='Total Target Quantity')
    loading_qty = models.IntegerField(default=0, verbose_name='DTS Quantity')
    remarks = models.CharField(max_length=500, blank=True, null=True, verbose_name='Remarks')

    class Meta:
        managed = True
        db_table = 'line_target'
        verbose_name = 'Line Target'
        verbose_name_plural = 'Line Targets'
        unique_together = ['source_connection', 'target_date', 'shift']
        ordering = ['-target_date', 'source_connection', 'shift']

    def __str__(self):
        return f"{self.source_connection} - {self.target_date} - Target: {self.total_target_qty} - Loading: {self.loading_qty}"



class LineTargetDetail(models.Model):
    SHIFT_CHOICES = [
        ('Day', 'Day'),
        ('Night', 'Night'),
    ]

    linetarget = models.ForeignKey(LineTarget, on_delete=models.CASCADE, verbose_name='Line Target', db_column='linetarget_id')
    cpo_id = models.ForeignKey('ClientPurchaseOrder', on_delete=models.SET_NULL, null=True, blank=True, db_column='cpo_id', db_constraint=False, verbose_name='Client Purchase Order')
    pono = models.CharField(max_length=10, verbose_name='PO No',null=True)
    articleno = models.CharField(max_length=50, verbose_name='Style ID',null=True,db_column='st_id')
    item_id = models.CharField(max_length=20, verbose_name='Item ID',null=True)
    item_title = models.CharField(max_length=200, verbose_name='Item Title',null=True)
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name='Model')
    barcode = models.BigIntegerField(verbose_name='Barcode',null=True)
    scrvoucher_no = models.CharField(max_length=20,blank=True, null=True, verbose_name='SCR Voucher No')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, db_column='cm_key', verbose_name='Color')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, db_column='sm_key', verbose_name='Size')
    bundleno = models.BigIntegerField(verbose_name='Bundle No',null=True)
    target_qty = models.IntegerField(verbose_name='Target Qty',null=True)
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, verbose_name='Shift',null=True)

    class Meta:
        managed = True
        db_table = 'line_target_detail'
        verbose_name = 'Line Target Detail'
        verbose_name_plural = 'Line Target Details'
        ordering = ['linetarget', 'pono', 'articleno', 'color__cm_key', 'size__sm_key']

    def save(self, *args, **kwargs):
        if self.cpo_id:
            self.articleno = self.cpo_id.articleno
            self.item_id = self.cpo_id.item_id
            self.item_title = self.cpo_id.item_title
            self.pono = self.cpo_id.pono
            # Set color and size from ClientPurchaseOrder
            if self.cpo_id.mcolour:
                color_obj, created = Color.objects.get_or_create(
                    cm_key=self.cpo_id.mcolour,
                    defaults={'cm_description': self.cpo_id.mcolour, 'cm_short_description': self.cpo_id.mcolour}
                )
                self.color = color_obj
            if self.cpo_id.itemsize:
                size_obj, created = Size.objects.get_or_create(
                    sm_key=self.cpo_id.itemsize,
                    defaults={'sm_description': self.cpo_id.itemsize}
                )
                self.size = size_obj
        if self.articleno and self.color and self.size:
            self.item_id = f"{self.articleno} - {self.color.cm_key} - {self.size.sm_key}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.linetarget} - {self.item_title} - {self.target_qty}"


class BreakdownCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'breakdown_category'
        verbose_name = 'Breakdown Category'
        verbose_name_plural = 'Breakdown Categories'

    def __str__(self):
        return self.name


class ClientPurchaseOrder(models.Model):
    id = models.BigIntegerField(primary_key=True)
    pono = models.CharField(blank=True, null=True)
    client_id = models.BigIntegerField(blank=True, null=True)
    client_title = models.CharField(blank=True, null=True)
    buyyear = models.IntegerField(blank=True, null=True)
    buymonth = models.IntegerField(blank=True, null=True)
    clientpodate = models.DateTimeField(blank=True, null=True)
    vtp = models.CharField(blank=True, null=True)
    vyear = models.IntegerField(blank=True, null=True)
    mnth = models.IntegerField(blank=True, null=True)
    vno = models.IntegerField(blank=True, null=True)
    scrvoucher_no = models.CharField(blank=True, null=True)
    srno = models.BigIntegerField(blank=True, null=True)
    divisionbygroup = models.CharField(blank=True, null=True)
    item_id = models.CharField(blank=True, null=True)
    articleno = models.CharField(blank=True, null=True)
    mcombo = models.CharField(blank=True, null=True)
    mcolour = models.CharField(blank=True, null=True)
    itemsize = models.CharField(blank=True, null=True)
    item_title = models.CharField(blank=True, null=True)
    po_qty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientpurchaseorder'
        verbose_name = 'Client Purchase Order'
        verbose_name_plural = 'ClientPurchaseOrders'
        ordering = ['-clientpodate']

    def __str__(self):
        return f"{self.articleno}-{self.pono}-{self.itemsize}-{self.mcolour}"

class Breakdown(models.Model):
    LINE_CHOICES = [
        ('line-21', 'Line-21'),
        ('line-22', 'Line-22'),
        ('line-23', 'Line-23'),
        ('line-24', 'Line-24'),
        ('line-25', 'Line-25'),
        ('line-26', 'Line-26'),
        ('line-27', 'Line-27'),
        ('line-28', 'Line-28'),
        ('line-29', 'Line-29'),
        ('line-30', 'Line-30'),
        ('line-31', 'Line-31'),
        ('line-32', 'Line-32'),
        ('line-all', 'Line-all'),
        ('line-6r', 'Line-6r'),
        ('line-7a', 'Line-7a'),
    ]

    SHIFT_CHOICES = [
        ('Day', 'Day'),
        ('Night', 'Night'),
    ]

    id = models.AutoField(primary_key=True)
    p_date = models.DateField(verbose_name='Production Date')
    line_no = models.CharField(max_length=10, choices=LINE_CHOICES, verbose_name='Line Number')
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    breakdown_category = models.ForeignKey(
        BreakdownCategory,
        on_delete=models.CASCADE,
        verbose_name='Breakdown Category'
    )
    remarks = models.TextField(blank=True, null=True)
    time_start = models.DateTimeField(verbose_name='Start Time')
    time_end = models.DateTimeField(verbose_name='End Time')
    operator_effected = models.IntegerField(default=0, verbose_name='Operators Affected')
    loss_minutes = models.IntegerField(default=0, verbose_name='Loss Minutes')

    class Meta:
        managed = True
        db_table = 'breakdown'
        verbose_name = 'Breakdown'
        verbose_name_plural = 'Breakdowns'
        ordering = ['-p_date', '-time_start']

    def __str__(self):
        return f"{self.line_no} - {self.p_date} - {self.breakdown_category}"

    @property
    def breakdown_time_minutes(self):
        """Calculate the difference between time_start and time_end in minutes"""
        if self.time_start and self.time_end:
            diff = self.time_end - self.time_start
            return diff.total_seconds() / 60
        return 0
