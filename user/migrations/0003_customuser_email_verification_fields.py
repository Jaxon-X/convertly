from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_customuser_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="email_verification_sent_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="is_email_verified",
            field=models.BooleanField(default=False),
        ),
    ]
