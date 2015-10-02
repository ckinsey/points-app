import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator

from django.db.models import Sum
from django.views.generic import TemplateView, CreateView

from pointset.models import PointSet


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

class HistoryView(TemplateView):
    template_name = "history.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HistoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        point_list = PointSet.objects.filter(given_by=self.request.user)
        kwargs.update({
            'point_list': point_list.order_by('-assigned_datetime'),
            'total_points': point_list.aggregate(total_points=Sum('point_count'))['total_points']
        })

        return super(HistoryView, self).get_context_data(**kwargs)

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


class LeaderBoardView(TemplateView):
    template_name = "leaderboard.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LeaderBoardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user_list = User.objects.all()

        for u in user_list:
            u.points = PointSet.objects.filter(user=u).aggregate(
                total_points=Sum('point_count'))['total_points']

        # Order users by total points
        user_list = sorted(user_list, key=lambda u: u.points, reverse=True)

        color_list = ["#F7464A", "#46BFBD", "#FDB45C", "#4D5360"]
        chart_data = {'datasets':[{'label': "User Point Breakdown",
            'fillColor': "rgba(151,187,205,0.5)",
            'strokeColor': "rgba(151,187,205,0.8)",
            'highlightFill': "rgba(151,187,205,0.75)",
            'highlightStroke': "rgba(151,187,205,1)",
            'data': []}]}
        for index, u in enumerate(user_list):
            chart_data.setdefault('labels', []).append(u.first_name)
            chart_data['datasets'][0]['data'].append(u.points)

        kwargs.update({
            'user_list': user_list,
            'chart_data': json.dumps(chart_data),
        })

        return super(LeaderBoardView, self).get_context_data(**kwargs)
