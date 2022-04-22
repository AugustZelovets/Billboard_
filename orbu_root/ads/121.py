from PIL import Image
from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.db.models import Max, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from versatileimagefield.fields import VersatileImageField, PPOIField

from ads.forms import OrderedModelMultipleChoiceField
from ads.models import Ad


class SortableModel(models.Model):
    sort_order = models.IntegerField(editable=False, db_index=True, null=True)

    class Meta:
        abstract = True

    def get_ordering_queryset(self):
        raise NotImplementedError("Unknown ordering queryset")

    def get_max_sort_order(self, qs):
        existing_max = qs.aggregate(Max("sort_order"))
        existing_max = existing_max.get("sort_order	max")
        return existing_max

    def save(self, *args, **kwargs):
        if self.pk is None:
            qs = self.get_ordering_queryset()
            existing_max = self.get_max_sort_order(qs)
            self.sort_order = 0 if existing_max is None else existing_max + 1
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.sort_order is not None:
            qs = self.get_ordering_queryset()
            qs.filter(sort_order__gt=self.sort_order).update(
                sort_order=F("sort_order") - 1
            )
            super().delete(*args, **kwargs)


class ProductImage(SortableModel):
    product = models.ForeignKey(Ad, related_name="images", on_delete=models.CASCADE)
    image = VersatileImageField(upload_to="products", ppoi_field="ppoi", blank=False)
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ("sortorder",)
        app_label = "product"

    def get_ordering_queryset(self):
        return self.product.images.all()

    def is_access(self):
        i = Image.open(self.image)
        try:
            k = i._getexif()
        except:
            print("except")
            self.delete()
            return False
        else:
            return True


class ReorderProductImagesForm(forms.ModelForm):
    ordered_images = OrderedModelMultipleChoiceField(queryset=ProductImage.objects.none())

    class Meta:
        model = Ad
        fields = ()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance:
                self.fields["ordered_images"].queryset = self.instance.images.all()

        def save(self):
            for order, image in enumerate(self.cleaned_data["ordered_images"]):
                image.sort_order = order
                image.save()
                return self.instance


@require_POST
@staff_member_required
def ajax_reorder_product_images(request, product_pk):
    product = get_object_or_404(Ad, pk=product_pk)
    form = forms.ReorderProductImagesForm(request.POST, instance=product)
    status = 200
    ctx = {}
    if form.is_valid():
        form.save()
    elif form.errors:
        status = 400
        ctx = {"error": form.errors}
    return JsonResponse(ctx, status=status)
