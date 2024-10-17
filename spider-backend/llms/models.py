from django.db import models

from common.models import CommonModel


# Create your models here.
class LlmModelTypes(CommonModel):
    """LlmModelType Model Definition"""

    model_type_id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=50)
    provider = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    port = models.CharField(max_length=10)
    price_per_token = models.IntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.model_name

    class Meta:
        db_table = "TB_LLM_MODEL_TYPE"
        verbose_name = "Llm Model Type"
        verbose_name_plural = "Llm Model Types"
