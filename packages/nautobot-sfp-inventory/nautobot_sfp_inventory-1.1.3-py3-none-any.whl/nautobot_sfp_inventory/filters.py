import django_filters
from django.db.models import Q

from nautobot.dcim.models import Device, Manufacturer
from nautobot.extras.filters import CreatedUpdatedFilterSet, CustomFieldModelFilterSet
from .models import SFPType, SFP
from nautobot.core.filters import BaseFilterSet, TagFilter
from nautobot.tenancy.models import Tenant


class SFPTypeFilterSet(BaseFilterSet, CreatedUpdatedFilterSet, CustomFieldModelFilterSet):
    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    tag = TagFilter()

    class Meta:
        model = SFPType
        fields = ["id", "name"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(comments__icontains=value)
        return queryset.filter(qs_filter)


class SFPFilterSet(BaseFilterSet, CreatedUpdatedFilterSet, CustomFieldModelFilterSet):
    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name="tenant",
        queryset=Tenant.objects.all(),
        label="Tenant",
    )
    type = django_filters.ModelMultipleChoiceFilter(
        field_name="type",
        queryset=SFPType.objects.all(),
        label="Type",
    )
    assigned_device = django_filters.ModelMultipleChoiceFilter(
        field_name="assigned_device",
        queryset=Device.objects.all(),
        label="Assigned Device",
    )
    supplier = django_filters.ModelMultipleChoiceFilter(
        field_name="supplier",
        queryset=Manufacturer.objects.all(),
        label="Manufacturer",
    )

    assigned = django_filters.BooleanFilter(
        method="_assigned",
        label="Assigned",
    )

    tag = TagFilter()

    class Meta:
        model = SFP
        fields = ["id", "serial_number", "dc_tag", "asset_tag"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(serial_number__icontains=value) | Q(dc_tag__icontains=value) \
            | Q(asset_tag__icontains=value) | Q(comments__icontains=value)
        return queryset.filter(qs_filter)

    def _assigned(self, queryset, name, value):
        return queryset.filter(assigned=value)
