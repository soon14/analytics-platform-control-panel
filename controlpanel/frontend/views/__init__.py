from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from mozilla_django_oidc.views import OIDCLogoutView

from controlpanel.frontend.views.app import (
    AdminAppList,
    AppList,
    AppDetail,
    CreateApp,
    DeleteApp,
    AddCustomers,
    RemoveCustomer,
    AddAdmin,
    RevokeAdmin,
    GrantAppAccess,
    UpdateAppAccess,
    RevokeAppAccess,
)
from controlpanel.frontend.views.datasource import (
    AdminBucketList,
    BucketDetail,
    BucketList,
    CreateDatasource,
    DeleteDatasource,
    GrantAccess,
    GrantPolicyAccess,
    RevokeAccess,
    UpdateAccessLevel,
    UpdateIAMManagedPolicyAccessLevel,
    RevokeIAMManagedPolicyAccess,
    WebappBucketList,
)
from controlpanel.frontend.views.policy import (
    AdminIAMManagedPolicyList,
    IAMManagedPolicyList,
    IAMManagedPolicyCreate,
    IAMManagedPolicyDelete,
    IAMManagedPolicyDetail,
    IAMManagedPolicyFormRoleList,
    IAMManagedPolicyRemoveUser,
)
from controlpanel.frontend.views.parameter import (
    AdminParameterList,
    ParameterList,
    ParameterCreate,
    ParameterDelete,
    ParameterFormRoleList,
)
from controlpanel.frontend.views.tool import (
    ToolList,
    DeployTool,
    RestartTool,
)
from controlpanel.frontend.views.user import (
    ResetMFA,
    SetSuperadmin,
    UserList,
    UserDelete,
    UserDetail,
)
from controlpanel.frontend.views.reset import ResetHome
from controlpanel.frontend.views.whats_new import WhatsNew


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get(self, request):
        """
        If the user is a superuser display the home page (containing useful
        admin related links). Otherwise, redirect the user to the list of the
        tools they currently have available on the platform.
        """
        if request.user.is_superuser:
            return super().get(request)
        else:
            # Redirect to the tools page.
            return HttpResponseRedirect(reverse("list-tools"))


class LogoutView(OIDCLogoutView):
    def get(self, request):
        return super().post(request)
