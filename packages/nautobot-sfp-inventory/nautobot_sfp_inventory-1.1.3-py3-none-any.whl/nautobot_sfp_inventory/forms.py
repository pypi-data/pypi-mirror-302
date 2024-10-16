from django.forms import DateField, BooleanField

from nautobot.extras.forms import CustomFieldModelFilterFormMixin, CustomFieldModelFormMixin, \
    RelationshipModelFormMixin, \
    TagsBulkEditFormMixin, CustomFieldModelBulkEditFormMixin
from nautobot.dcim.models import Manufacturer, Device
from nautobot.core.forms import CommentField
from nautobot.core.forms import StaticSelect2, BOOLEAN_WITH_BLANK_CHOICES
from nautobot.core.forms import ExpandableNameField
from .models import SFPType, SFP
from nautobot.core.forms import BootstrapMixin, DynamicModelMultipleChoiceField, TagFilterField
from nautobot.core.forms import widgets
from nautobot.tenancy.models import Tenant
from nautobot.core.forms import DynamicModelChoiceField
from django import forms


class SFPTypeFilterForm(BootstrapMixin, CustomFieldModelFilterFormMixin):
    model = SFPType
    q = forms.CharField(required=False, label="Search")

    tag = TagFilterField(model)


class SFPTypeForm(BootstrapMixin, CustomFieldModelFormMixin, RelationshipModelFormMixin):
    comments = CommentField()

    class Meta:
        model = SFPType
        fields = [
            "name",
            "comments"
        ]


class SFPFilterForm(BootstrapMixin, CustomFieldModelFilterFormMixin):
    model = SFP
    q = forms.CharField(required=False, label="Search")

    type = DynamicModelMultipleChoiceField(
        queryset=SFPType.objects.all(),
        to_field_name="pk",
        required=False,
        null_option="None",
    )

    supplier = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="pk",
        required=False,
        null_option="None",
    )

    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name="pk",
        required=False,
        null_option="None",
    )

    assigned = forms.NullBooleanField(
        required=False,
        label="Assigned",
        widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    assigned_device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        null_option="None",
        label="Assigned Device"
    )

    tag = TagFilterField(model)


class SFPBulkCreateForm(BootstrapMixin, forms.Form):
    pattern = ExpandableNameField(label="Serial Number")


class SFPForm(BootstrapMixin, CustomFieldModelFormMixin, RelationshipModelFormMixin):
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    type = DynamicModelChoiceField(queryset=SFPType.objects.all(), required=False)
    assigned_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Assigned Device"
    )
    supplier = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    end_of_manufacturer_support = DateField(
        widget=widgets.DatePicker,
        required=False,
        label="End of Manufacturer Support"
    )

    comments = CommentField()

    class Meta:
        model = SFP
        fields = [
            "serial_number",
            "type",
            "dc_tag",
            "asset_tag",
            "tenant",
            "assigned",
            "assigned_device",
            "supplier",
            "procurement_ident",
            "end_of_manufacturer_support",
            "comments",
        ]


class SFPBulkEditForm(BootstrapMixin, TagsBulkEditFormMixin, CustomFieldModelBulkEditFormMixin):
    pk = forms.ModelMultipleChoiceField(queryset=SFP.objects.all(), widget=forms.MultipleHiddenInput)
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    type = DynamicModelChoiceField(queryset=SFPType.objects.all(), required=False)
    assigned = BooleanField(required=False)
    assigned_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Assigned Device"
    )
    supplier = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    end_of_manufacturer_support = DateField(
        widget=widgets.DatePicker,
        required=False,
        label="End of Manufacturer Support"
    )

    comments = CommentField()

    class Meta:
        nullable_fields = [
            "assigned",
            "end_of_manufacturer_support",
            "comments",
        ]


class SFPBulkAttachForm(BootstrapMixin, CustomFieldModelFormMixin):
    sfps = DynamicModelMultipleChoiceField(
        queryset=SFP.objects.all(),
        required=False,
        label="Assigned SFPs",
    )

    class Meta:
        model = Device
        fields = ["sfps"]

    # we need to populate initial values 1st
    # so that when object gets edited, we don't "forget"
    # currently assigned SFPs
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.initial["sfps"] = self.instance.sfps.values_list("id", flat=True)
