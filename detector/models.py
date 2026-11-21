
from django.db import models
from django.conf import settings


class Image(models.Model):

    image_id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='images'
    )

    file = models.ImageField(upload_to='images/')

    original_name = models.CharField(max_length=255)

    format = models.CharField(max_length=10)

    size = models.PositiveBigIntegerField()

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name


class ImageAnalysis(models.Model):

    RESULT_CHOICES = [
        ('real', 'Real'),
        ('ai_generated', 'AI Generated'),
        ('manipulated', 'Manipulated'),
        ('both', 'Both'),
        ('uncertain', 'Uncertain'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    analysis_id = models.BigAutoField(primary_key=True)

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='analyses'
    )

    final_result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis {self.analysis_id}"


class ModelVersion(models.Model):

    model_version_id = models.BigAutoField(primary_key=True)

    model_type = models.CharField(max_length=50)

    version = models.CharField(max_length=50)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_type} - {self.version}"


class AIAnalysisResult(models.Model):

    aianalysisresult_id = models.BigAutoField(primary_key=True)

    analysis = models.ForeignKey(
        ImageAnalysis,
        on_delete=models.CASCADE,
        related_name='ai_results'
    )

    model_version = models.ForeignKey(
        ModelVersion,
        on_delete=models.PROTECT,
        related_name='ai_results'
    )

    prediction = models.CharField(max_length=50)

    confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    details = models.JSONField(
        blank=True,
        default=dict
    )

    def __str__(self):
        return f"AI Result - Analysis {self.analysis_id}"


class ManipulationResult(models.Model):

    manipulationresult_id = models.BigAutoField(primary_key=True)

    analysis = models.ForeignKey(
        ImageAnalysis,
        on_delete=models.CASCADE,
        related_name='manipulation_results'
    )

    model_version = models.ForeignKey(
        ModelVersion,
        on_delete=models.PROTECT,
        related_name='manipulation_results'
    )

    prediction = models.CharField(max_length=50)

    confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    details = models.JSONField(
        blank=True,
        default=dict
    )

    def __str__(self):
        return f"Manipulation Result - Analysis {self.analysis_id}"



























# from django.db import models
# from django.conf import settings


# class Image(models.Model):

#     image_id = models.BigAutoField(primary_key=True)

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='images'
#     )

#     file = models.ImageField(upload_to='images/')

#     original_name = models.CharField(max_length=255)

#     format = models.CharField(max_length=10)

#     size = models.PositiveBigIntegerField()

#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.original_name


# class ImageAnalysis(models.Model):

#     RESULT_CHOICES = [
#         ('real', 'Real'),
#         ('ai_generated', 'AI Generated'),
#         ('manipulated', 'Manipulated'),
#         ('both', 'Both'),
#         ('uncertain', 'Uncertain'),
#     ]

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('failed', 'Failed'),
#     ]

#     analysis_id = models.BigAutoField(primary_key=True)

#     image = models.ForeignKey(
#         Image,
#         on_delete=models.CASCADE,
#         related_name='analyses'
#     )

#     final_result = models.CharField(
#         max_length=20,
#         choices=RESULT_CHOICES,
#         null=True,
#         blank=True
#     )

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='pending'
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Analysis {self.analysis_id}"

#     class AIAnalysisResult(models.Model):

#     aianalysisresult_id = models.BigAutoField(primary_key=True)

#     analysis = models.ForeignKey(
#         ImageAnalysis,
#         on_delete=models.CASCADE,
#         related_name='ai_results'
#     )

#     model_version = models.ForeignKey(
#         ModelVersion,
#         on_delete=models.PROTECT,
#         related_name='ai_results'
#     )

#     prediction = models.CharField(max_length=50)

#     confidence = models.DecimalField(
#         max_digits=5,
#         decimal_places=2
#     )

#     details = models.JSONField(
#         blank=True,
#         default=dict
#     )

#     def __str__(self):
#         return f"AI Result - Analysis {self.analysis_id}"

#     class ManipulationResult(models.Model):

#     manipulationresult_id = models.BigAutoField(primary_key=True)

#     analysis = models.ForeignKey(
#         ImageAnalysis,
#         on_delete=models.CASCADE,
#         related_name='manipulation_results'
#     )

#     model_version = models.ForeignKey(
#         ModelVersion,
#         on_delete=models.PROTECT,
#         related_name='manipulation_results'
#     )

#     prediction = models.CharField(max_length=50)

#     confidence = models.DecimalField(
#         max_digits=5,
#         decimal_places=2
#     )

#     details = models.JSONField(
#         blank=True,
#         default=dict
#     )

#     def __str__(self):
#         return f"Manipulation Result - Analysis {self.analysis_id}"