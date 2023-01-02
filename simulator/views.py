from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
import simpy
from . import models
import random
from django.views.generic import UpdateView
from datetime import datetime
from django.http import HttpResponse
import csv

class InputForm(ModelForm):
    class Meta:
        model = models.CreateInput
        fields = '__all__'

def index(request):
    context = {'greetings': 'WELCOME TO MY CALL CENTER SIMULATION PAGE'}
    return render(request, 'simulator/index.html', context)

class GetVars(View):
    model = models.CreateInput
    template_name = 'simulator/form.html'
    success_url = reverse_lazy('simulator:success')

    def get(self, request):
        models.CreateInput.objects.all().delete()
        context = {'form': InputForm()}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form = InputForm(request.POST)
        form.save()
        return redirect(self.success_url)


class CallCenter:
    """represents call center """
    def __init__(self, simulation_number):
        self.name = 0
        self.simulation_number = simulation_number
        self.call_list = models.CreateInput.objects.values('call_list').last()['call_list']
        self.call_list = [i for i in range(1, self.call_list + 1)]
        self.batch = 1
        self.env = simpy.Environment()
        # how many times the whole process is reproduced
        # how many lines are available for dialer
        self.line_numbers = models.CreateInput.objects.values('line_numbers').last()['line_numbers']
        # total shift
        self.capacity = models.CreateInput.objects.values('number_jf_agents').last()['number_jf_agents']
        self.agent = simpy.Resource(self.env, capacity=self.capacity)
        # time being simulated in sec: number or None
        self.shift_time = models.CreateInput.objects.values('shift_time').last()['shift_time']
        # time required to take and dial a batch(high, low, mode)
        self.take_high = models.CreateInput.objects.values('take_high').last()['take_high']
        self.take_low = models.CreateInput.objects.values('take_low').last()['take_low']
        self.take_mode = models.CreateInput.objects.values('take_mode').last()['take_mode']
        # the share of unsuccessful attempts in batch (high, low, mode)
        self.unreachable_h = models.CreateInput.objects.values('unreachable_h').last()['unreachable_h']
        self.unreachable_l = models.CreateInput.objects.values('unreachable_l').last()['unreachable_l']
        self.unreachable_m = models.CreateInput.objects.values('unreachable_m').last()['unreachable_m']
        # time between point of call starts ringing and call gets answered or cancelled (high, low, mode)
        self.ring_time_h = models.CreateInput.objects.values('ring_time_h').last()['ring_time_h']
        self.ring_time_l =models.CreateInput.objects.values('ring_time_l').last()['ring_time_l']
        self.ring_time_m = models.CreateInput.objects.values('ring_time_m').last()['ring_time_m']
        # share of reached customers from those who received a call (high, low, mode)
        self.reach_rate_h = models.CreateInput.objects.values('reach_rate_h').last()['reach_rate_h']
        self.reach_rate_l = models.CreateInput.objects.values('reach_rate_l').last()['reach_rate_l']
        self.reach_rate_m = models.CreateInput.objects.values('reach_rate_m').last()['reach_rate_m']
        # answering machine clearance duration parameters (high, low, mode)
        self.d_h = models.CreateInput.objects.values('d_h').last()['d_h']
        self.d_l =models.CreateInput.objects.values('d_l').last()['d_l']
        self.d_m =models.CreateInput.objects.values('d_m').last()['d_m']
        # talk time parameters (high, low)
        self.t_h = models.CreateInput.objects.values('t_h').last()['t_h']
        self.t_l = models.CreateInput.objects.values('t_l').last()['t_l']
        # clerical time parameters (high, low)
        self.c_h = models.CreateInput.objects.values('c_h').last()['c_h']
        self.c_l =models.CreateInput.objects.values('c_l').last()['c_l']


    def dial(self):
        counter = 0
        while len(self.call_list) > 0 and self.env.now < self.shift_time:
            start = self.env.now
            spin = counter / len(self.call_list)
            batch = [i for y, i in enumerate(self.call_list) if y + 1 <= self.line_numbers]
            self.call_list = [i for i in self.call_list if i not in batch]
            for i in batch:
                counter += 1
                record = models.GlobalResults(run=self.simulation_number + 1)
                record.attempt_no = counter
                record.call_no = i
                record.batch = self.batch
                record.spin = spin
                record.capacity = self.capacity
                record.attempt_started = start
                record.save()
            self.call_list = [i for i in self.call_list if i not in batch]
            yield self.env.timeout(random.triangular(high=self.take_high, low=self.take_low,
                                                        mode=self.take_mode))
            unreached = random.sample(population=batch, k=round(random.triangular(high=self.unreachable_h,
                                                                                  low=self.unreachable_l,
                                                                                  mode=self.unreachable_m) *
                                                                len(batch)))
            for i in batch:
                update_rec = models.GlobalResults.objects.filter(run=self.simulation_number+1, call_no=i).last()
                update_rec.if_unreachable = 1 if i in unreached else None
                update_rec.save()
            batch = [i for i in batch if i not in unreached]
            yield self.env.timeout(random.triangular(high=self.ring_time_h, low=self.ring_time_l,
                                                        mode=self.ring_time_m))
            talks = random.sample(population=batch, k=round(len(batch) * random.triangular(high=self.reach_rate_h,
                                                                                           low=self.reach_rate_l,
                                                                                           mode=self.reach_rate_m)))
            for i in batch:
                update_rec_na = models.GlobalResults.objects.filter(run=self.simulation_number+1, call_no=i).last()
                update_rec_na.if_not_answering = 1 if i not in talks else None
                update_rec_na.save()
            self.call_list += [i for i in batch if i not in talks]
            for i in talks:
                answer_time = self.env.now
                call = IncomingCall(i)
                self.env.process(self.accepting_call(call, answer_time))
            self.batch += 1


    def accepting_call(self, call, answer_time):
        answer_time = answer_time
        update_rec_at = models.GlobalResults.objects.filter(call_no=call.name, run=self.simulation_number+1).last()
        update_rec_at.answer_time = answer_time
        duration = random.triangular(low=self.d_l, high=self.d_h, mode=self.d_m)
        update_rec_at.amd_time = duration
        yield self.env.timeout(min(duration, call.patience))
        call.patience = call.patience - duration if duration < call.patience else 0
        if call.patience == 0:
           update_rec_at.if_dropped = 1
           update_rec_at.wait_before_drop = self.env.now - answer_time
        else:
            with self.agent.request() as req:
                yield req | self.env.timeout(call.patience)
                if req.triggered:
                    wait_time = self.env.now - answer_time
                    update_rec_at.wait_time = wait_time
                    talk_time = random.uniform(self.t_l, self.t_h)
                    update_rec_at.talk_time = talk_time
                    yield self.env.timeout(talk_time)
                    clerical_time = random.uniform(self.c_l, self.c_h)
                    update_rec_at.clerical_time = clerical_time
                    yield self.env.timeout(clerical_time)
                else:
                    update_rec_at.if_dropped = 1
                    update_rec_at.wait_before_drop = self.env.now - answer_time
        update_rec_at.save()

    def run(self):
        self.env.process(self.dial())
        self.env.run()


class IncomingCall:
    def __init__(self, name):
        self.name = name
        self.patience = random.uniform(models.CreateInput.objects.values('p_h').last()['p_h'],
                                       models.CreateInput.objects.values('p_l').last()['p_l'])


class ConfirmVars(View):
    template = 'simulator/confirm_vars.html'
    def get(self,request):
        myvars = models.CreateInput.objects.values().last()
        return render(request, template_name=self.template, context={'myvars': myvars})

class EditVars(UpdateView):
    template_name = 'simulator/createinput_update.html'
    success_url = reverse_lazy('simulator:success')
    def get(self, request, pk):
        pk = models.CreateInput.objects.values().last()['id']
        vars = get_object_or_404(models.CreateInput, id=pk)
        form = InputForm(instance=vars)
        cntx = {'form': form}
        print(vars)
        return render(request, template_name=self.template_name, context=cntx)

    def post(self, request, pk=None):
        vars = get_object_or_404(models.CreateInput, id=pk)
        form = InputForm(request.POST, instance=vars)
        vars = form.save()
        return redirect(self.success_url)


def launch(request):
    start = datetime.now()
    models.GlobalResults.objects.all().delete()
    for simulation_number in range(models.CreateInput.objects.values('number_of_simulations').last()['number_of_simulations']):
        print(f'run {simulation_number}')
        CallCenter.env = simpy.Environment()
        call_center = CallCenter(simulation_number)
        call_center.run()
    finish = datetime.now()
    print(f' simulation took {finish - start}')
    return redirect('simulator:export')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="simulation_log.csv"'

    writer = csv.writer(response)
    writer.writerow(['run', 'attempt_no', 'call_no', 'batch', 'spin', 'capacity', 'attempt_started', 'if_unreachable',
                     'if_not_answering', 'answer_time', 'amd_time', 'if_dropped', 'wait_before_drop', 'wait_time',
                     'talk_time', 'clerical_time'])

    results = models.GlobalResults.objects.all().values_list('run', 'attempt_no', 'call_no', 'batch', 'spin', 'capacity',
                                                           'attempt_started', 'if_unreachable',
                                                           'if_not_answering', 'answer_time', 'amd_time', 'if_dropped',
                                                           'wait_before_drop', 'wait_time', 'talk_time',
                                                           'clerical_time')
    for result in results:
        writer.writerow(result)

    return response


#TODO
# 4) if script is being run something should be displayed while results are unavailable



