import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0015_attendance_is_admin_overridden'),
    ]
    operations = [
        migrations.AlterField(
            model_name='subject',
            name='assigned_staff',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='staff.staffprofile'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='staff',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='staff.staffprofile'),
        ),
    ]