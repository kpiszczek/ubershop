from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect


class BackendPanel:
    # TU NIE MA CO DZIALAC ;)

    @classmethod
    @method_decorator(staff_member_required)
    def main(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def items_list(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def edit_item(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def add_item(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def group_list(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def edit_group(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def add_group(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def category_list(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def edit_category(cls, request):
        raise NotImplemented

    @classmethod
    @method_decorator(staff_member_required)
    def add_category(cls, request):
        raise NotImplemented
