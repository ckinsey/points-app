from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator

from django.db.models import Sum
from django.views.generic import TemplateView, CreateView

from pointset.models import PointSet

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        point_list = PointSet.objects.filter(user=self.request.user)
        kwargs.update({
            'point_list': point_list.order_by('-assigned_datetime'),
            'total_points': point_list.aggregate(total_points=Sum('point_count'))['total_points']
        })

        return super(IndexView, self).get_context_data(**kwargs)

class CreatePointSetView(CreateView):
    model = PointSet
    template_name = "give_points.html"

    fields = ['user', 'description', 'point_count']

    success_url = "/"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreatePointSetView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(CreatePointSetView, self).get_form(form_class)
        form.fields['user'].queryset = User.objects.exclude(id=self.request.user.id)

        return form

    def form_valid(self, form):
        # Set the given by value to the currently logged in user
        form.instance.given_by = self.request.user

        messages.success(self.request, "You gave {0} points to {1}".format(
            form.cleaned_data['point_count'],
            form.cleaned_data['user'].first_name,
        ))
        return super(CreatePointSetView, self).form_valid(form)