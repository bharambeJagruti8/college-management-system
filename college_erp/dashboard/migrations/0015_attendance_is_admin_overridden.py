from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0014_remove_attendance_is_admin_overridden_and_more'),
    ]
    operations = [
        migrations.AddField(
            model_name='attendance',
            name='is_admin_overridden',
            field=models.BooleanField(default=False),
        ),
    ]