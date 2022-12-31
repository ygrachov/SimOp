from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import ModelForm
from django.http import request,response
from django.urls import reverse, reverse_lazy
import pandas as pd
import simpy
from . import models
import random
from django.views.generic import UpdateView

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
        context = {'form': InputForm()}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form = InputForm(request.POST)
        form.save()
        return redirect(self.success_url)

# Create your views here.
class Globals:
    # TODO add prediction mode: reducing number of line upon resources availability
    # TODO add light computations for big simulations
    #assign variable from model just before simulation
    """stores variables used for simulation. It can simulate either a period of time or certain number of calls"""
    env = simpy.Environment()
    # how many times the whole process is reproduced
    number_of_simulations = models.CreateInput.objects.values('number_of_simulations').last()['number_of_simulations']
    # how many lines are available for dialer
    line_numbers = models.CreateInput.objects.values('line_numbers').last()['line_numbers']
    # total shift
    number_jf_agents = models.CreateInput.objects.values('number_jf_agents').last()['number_jf_agents']
    # time being simulated in sec: number or None
    shift_time = models.CreateInput.objects.values('shift_time').last()['shift_time']
    # number of customers to be served
    call_list = models.CreateInput.objects.values('call_list').last()['call_list']
    # time required to take and dial a batch(high, low, mode)
    take_high = models.CreateInput.objects.values('take_high').last()['take_high']
    take_low = models.CreateInput.objects.values('take_low').last()['take_low']
    take_mode = models.CreateInput.objects.values('take_mode').last()['take_mode']
    # the share of unsuccessful attempts in batch (high, low, mode)
    unreachable_h = models.CreateInput.objects.values('unreachable_h').last()['unreachable_h']
    unreachable_l = models.CreateInput.objects.values('unreachable_l').last()['unreachable_l']
    unreachable_m = models.CreateInput.objects.values('unreachable_m').last()['unreachable_m']
    # time between point of call starts ringing and call gets answered or cancelled (high, low, mode)
    ring_time_h = models.CreateInput.objects.values('ring_time_h').last()['ring_time_h']
    ring_time_l = models.CreateInput.objects.values('ring_time_l').last()['ring_time_l']
    ring_time_m = models.CreateInput.objects.values('ring_time_m').last()['ring_time_m']
    # share of reached customers from those who received a call (high, low, mode)
    reach_rate_h = models.CreateInput.objects.values('reach_rate_h').last()['reach_rate_h']
    reach_rate_l = models.CreateInput.objects.values('reach_rate_l').last()['reach_rate_l']
    reach_rate_m = models.CreateInput.objects.values('reach_rate_m').last()['reach_rate_m']
    # answering machine clearance duration parameters (high, low, mode)
    d_h = models.CreateInput.objects.values('d_h').last()['d_h']
    d_l = models.CreateInput.objects.values('d_l').last()['d_l']
    d_m = models.CreateInput.objects.values('d_m').last()['d_m']
    # customer's patience parameter (high, low)
    p_h = models.CreateInput.objects.values('p_h').last()['p_h']
    p_l = models.CreateInput.objects.values('p_l').last()['p_l']
    # talk time parameters (high, low)
    t_h = models.CreateInput.objects.values('t_h').last()['t_h']
    t_l = models.CreateInput.objects.values('t_l').last()['t_l']
    # clerical time parameters (high, low)
    c_h = models.CreateInput.objects.values('c_h').last()['c_h']
    c_l = models.CreateInput.objects.values('c_l').last()['c_l']
    # dataframe to record statistics on each call
    results = pd.DataFrame()


class CallCenter:
    """represents call center """

    def __init__(self, simulation_number):
        self.name = 0
        self.capacity = Globals.number_jf_agents
        self.agent = simpy.Resource(Globals.env, capacity=self.capacity)
        self.simulation_number = simulation_number
        self.call_list = [i for i in range(1, Globals.call_list + 1)]
        self.batch = 1

    def dial(self):
        counter = 0
        while len(self.call_list) > 0:
            batch_result = pd.DataFrame()
            start = Globals.env.now
            spin = counter / len(self.call_list)
            batch = [i for y, i in enumerate(self.call_list) if y + 1 <= Globals.line_numbers]
            self.call_list = [i for i in self.call_list if i not in batch]
            for i in batch:
                counter += 1
                batch_result.loc[i, 'run'] = self.simulation_number + 1
                batch_result.loc[i, 'attempt_no'] = counter
                batch_result.loc[i, 'call_no'] = i
                batch_result.loc[i, 'batch'] = self.batch
                batch_result.loc[i, 'spin'] = spin
                batch_result.loc[i, 'capacity'] = self.capacity
                batch_result.loc[i, 'attempt_started'] = start
            self.call_list = [i for i in self.call_list if i not in batch]
            yield Globals.env.timeout(random.triangular(high=Globals.take_high, low=Globals.take_low,
                                                        mode=Globals.take_mode))
            unreached = random.sample(population=batch, k=round(random.triangular(high=Globals.unreachable_h,
                                                                                  low=Globals.unreachable_l,
                                                                                  mode=Globals.unreachable_m) *
                                                                len(batch)))
            for i in batch:
                batch_result.loc[i, 'if_unreachable'] = 1 if i in unreached else None
            batch = [i for i in batch if i not in unreached]
            yield Globals.env.timeout(random.triangular(high=Globals.ring_time_h, low=Globals.ring_time_l,
                                                        mode=Globals.ring_time_m))
            talks = random.sample(population=batch, k=round(len(batch) * random.triangular(high=Globals.reach_rate_h,
                                                                                           low=Globals.reach_rate_l,
                                                                                           mode=Globals.reach_rate_m)))
            for i in batch:
                batch_result.loc[i, 'if_not_answering'] = 1 if i not in talks else None
            self.call_list += [i for i in batch if i not in talks]
            Globals.results = pd.concat([Globals.results, batch_result], ignore_index=True)
            for i in talks:
                answer_time = Globals.env.now
                call = IncomingCall(i)
                Globals.env.process(self.accepting_call(call, answer_time))
            self.batch += 1

    def accepting_call(self, call, answer_time):
        answer_time = answer_time
        Globals.results.loc[(Globals.results['call_no'] == call.name) & (Globals.results['if_unreachable'] != 1)
                            & (Globals.results['if_not_answering'] != 1) & (Globals.results['run'] ==
                                                                            self.simulation_number + 1),
                            'answer_time'] = answer_time
        duration = random.triangular(low=Globals.d_l, high=Globals.d_h, mode=Globals.d_m)
        Globals.results.loc[(Globals.results['call_no'] == call.name) & (Globals.results['answer_time'] >= 0)
                            & (Globals.results['run'] == self.simulation_number + 1),
                            'amd_time'] = duration
        yield Globals.env.timeout(min(duration, call.patience))
        call.patience = call.patience - duration if duration < call.patience else 0
        if call.patience == 0:
            Globals.results.loc[(Globals.results['call_no'] == call.name) & (
                    Globals.results['answer_time'] >= 0) & (Globals.results['run'] == self.simulation_number + 1),
                                'if_dropped'] = 1
            Globals.results.loc[(Globals.results['call_no'] == call.name) & (
                    Globals.results['answer_time'] >= 0) & (Globals.results['run'] == self.simulation_number + 1),
                                'wait_before_drop'] = Globals.env.now - answer_time
        else:
            with self.agent.request() as req:
                yield req | Globals.env.timeout(call.patience)
                if req.triggered:
                    wait_time = Globals.env.now - answer_time
                    Globals.results.loc[(Globals.results['call_no'] == call.name) & (
                            Globals.results['answer_time'] >= 0) & (Globals.results['run']
                                                                    == self.simulation_number + 1),
                                        'wait_time'] = wait_time
                    talk_time = random.uniform(Globals.t_l, Globals.t_h)
                    Globals.results.loc[(Globals.results['call_no'] == call.name) & (
                            Globals.results['answer_time'] >= 0) &
                                        (Globals.results['run'] == self.simulation_number + 1), 'talk_time'] = talk_time
                    yield Globals.env.timeout(talk_time)
                    clerical_time = random.uniform(Globals.c_l, Globals.c_h)
                    Globals.results.loc[(Globals.results['call_no'] == call.name) & (
                            Globals.results['answer_time'] >= 0) &
                                        (Globals.results[
                                             'run'] == self.simulation_number + 1), 'clerical_time'] = clerical_time
                    yield Globals.env.timeout(clerical_time)
                else:
                    Globals.results.loc[(Globals.results['call_no'] == call.name) & (
                            Globals.results['answer_time'] >= 0) & (Globals.results['run'] ==
                                                                    self.simulation_number + 1), 'if_dropped'] = 1
                    Globals.results.loc[(Globals.results['call_no'] == call.name) & (
                            Globals.results['answer_time'] >= 0) & (Globals.results['run'] ==
                                                                    self.simulation_number + 1), 'wait_before_drop'] = \
                        Globals.env.now - answer_time

    def run(self):
        Globals.env.process(self.dial())
        Globals.env.run()


class IncomingCall:
    def __init__(self, name):
        self.name = name
        self.patience = random.uniform(Globals.p_l, Globals.p_h)


# for simulation_number in range(Globals.number_of_simulations):
#     print(f'run # {simulation_number}')
#     Globals.env = simpy.Environment()
#     call_center = CallCenter(simulation_number)
#     call_center.run()
# print('wruting results to the file...')
# Globals.results.to_excel('simulation_log.xlsx', index=False, sheet_name='CDR log')

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
    print(Globals.__dict__)
    for simulation_number in range(Globals.number_of_simulations):
        print(f'run {simulation_number}')
        Globals.env = simpy.Environment()
        call_center = CallCenter(simulation_number)
        call_center.run()
    print('writing results to the file...')
    Globals.results.to_excel('simulation_log.xlsx', index=False, sheet_name='CDR log')
    print(Globals.__dict__)
    return redirect('simulator:main')


#TODO
# 3-1) change pd to BD
# 3-2) clean bd after each simulation
# 4) if script is being run something should be displayed while results are unavailable
# 5)update class Globals params when edited - they not updating

# Create a new record using the model's constructor.
# record = MyModelName(my_field_name="Instance #1")
# after all changes are made by changing attributes of var record
# Save the object into the database.
# record.save()

