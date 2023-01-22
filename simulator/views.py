from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.urls import reverse_lazy
import simpy
from . import models
import random
from django.views.generic import FormView
from datetime import datetime
from django.http import HttpResponse
import uuid
import csv


class Uuid:
    """Generates a unique ID for user input, using UUID standard to ensure no collisions.
    The unique ID is stored as a string object self.id"""
    def __init__(self):
        self.id = uuid.uuid4().hex


num = Uuid()


class InputForm(ModelForm):
    """ A form class used to validate user input for a simulation. Inherits from Django's ModelForm and uses
    the CreateInput model. Includes fields for all input variables, as well as a clean method for validating input
    values."""
    class Meta:
        """ A nested class that defines metadata for the InputForm class.
        Specifies the model used for the form and the fields included in the form"""
        model = models.CreateInput
        fields = ['number_of_simulations',
                  'line_numbers',
                  'number_of_agents',
                  'shift_time',
                  'call_list',
                  'take_high',
                  'take_low',
                  'take_mode',
                  'unreachable_h',
                  'unreachable_l',
                  'unreachable_m',
                  'ring_time_h',
                  'ring_time_l',
                  'ring_time_m',
                  'reach_rate_h',
                  'reach_rate_l',
                  'reach_rate_m',
                  'd_h',
                  'd_l',
                  'd_m',
                  'p_h',
                  'p_l',
                  't_h',
                  't_l',
                  'c_h',
                  'c_l']

    def clean(self):
        """validates user's input for the logic required to make the model works """
        cleaned_data = super().clean()
        shift_time = cleaned_data.get('shift_time')
        take_high = cleaned_data.get('take_high')
        take_low = cleaned_data.get('take_low')
        take_mode = cleaned_data.get('take_mode')
        unreachable_h = cleaned_data.get('unreachable_h')
        unreachable_l = cleaned_data.get('unreachable_l')
        unreachable_m = cleaned_data.get('unreachable_m')
        ring_time_h = cleaned_data.get('ring_time_h')
        ring_time_l = cleaned_data.get('ring_time_l')
        ring_time_m = cleaned_data.get('ring_time_m')
        reach_rate_h = cleaned_data.get('reach_rate_h')
        reach_rate_l = cleaned_data.get('reach_rate_l')
        reach_rate_m = cleaned_data.get('reach_rate_m')
        d_h = cleaned_data.get('d_h')
        d_l = cleaned_data.get('d_l')
        d_m = cleaned_data.get('d_m')
        p_h = cleaned_data.get('p_h')
        p_l = cleaned_data.get('p_l')
        t_h = cleaned_data.get('t_h')
        t_l = cleaned_data.get('t_l')
        c_h = cleaned_data.get('c_h')
        c_l = cleaned_data.get('c_l')

        if shift_time <= 0:
            self.add_error('shift_time', 'number_of_simulations must be > 0')
        if take_high < take_low:
            self.add_error('take_high', 'lower bound must be <= upper bound')
        if take_mode < take_low:
            self.add_error('take_low', 'lower bound must be <= upper bound')
        if take_mode > take_high:
            self.add_error('take_mode', 'lower bound must be <= upper bound')
        if unreachable_h < unreachable_l:
            self.add_error('unreachable_h', 'lower bound must be <= upper bound')
        if unreachable_m < unreachable_l:
            self.add_error('unreachable_l', 'lower bound must be <= upper bound')
        if unreachable_m > unreachable_h:
            self.add_error('unreachable_m', 'lower bound must be <= upper bound')
        if ring_time_h < ring_time_l:
            self.add_error('ring_time_h', 'lower bound must be <= upper bound')
        if ring_time_m < ring_time_l:
            self.add_error('ring_time_l', 'lower bound must be <= upper bound')
        if ring_time_m > ring_time_h:
            self.add_error('ring_time_m', 'lower bound must be <= upper bound')
        if reach_rate_h < reach_rate_l:
            self.add_error('reach_rate_h', 'lower bound must be <= upper bound')
        if reach_rate_m < reach_rate_l:
            self.add_error('reach_rate_l', 'lower bound must be <= upper bound')
        if reach_rate_m > reach_rate_h:
            self.add_error('reach_rate_m', 'lower bound must be <= upper bound')
        if d_h < d_l:
            self.add_error('d_h', 'lower bound must be <= upper bound')
        if d_m < d_l:
            self.add_error('d_l', 'lower bound must be <= upper bound')
        if d_m > d_h:
            self.add_error('d_m', 'lower bound must be <= upper bound')
        if t_h < t_l:
            self.add_error('t_h', 'lower bound must be <= upper bound')
        if p_h < p_l:
            self.add_error('p_h', 'lower bound must be <= upper bound')
        if c_h < c_l:
            self.add_error('c_h', 'lower bound must be <= upper bound')
        return cleaned_data


def index(request):
    """Handles request for main page and returns rendered template"""
    context = {}
    return render(request, 'simulator/index.html', context)


class GetVars(FormView):
    """A FormView class that handles the rendering and processing of the input form.
    If input is valid it is being written to the database (table Createinput)"""
    form_class = InputForm
    num = Uuid()
    template_name = 'simulator/form.html'
    success_url = reverse_lazy('simulator:launch')

    def form_valid(self, form):
        """Calls the clean method of the InputForm and handles a valid form submission by saving the data to
        the database and redirecting to the 'success_url'"""
        if form.is_valid():
            instance = form.save(commit=False)
            uuid = self.num.id
            instance.uuid = uuid
            instance.save()
            response = redirect(self.get_success_url())
            response['cache-control'] = 'no-cache'
            return response
        else:
            return super().form_invalid(form)


def launch(request):
    """Handles the execution of the simulation model, triggered by a valid form submission.
    This method uses all the necessary input from the user to initialize and run the simulation environment."""
    uu_id = models.CreateInput.objects.values('uuid').last()['uuid']
    start = datetime.now()
    for simulation_number in range(models.CreateInput.objects.values('number_of_simulations').last()
                                   ['number_of_simulations']):
        CallCenter.env = simpy.Environment()
        call_center = CallCenter(simulation_number, uu_id)
        call_center.run()
    finish = datetime.now()
    return redirect('simulator:export')


def display_results(request):
    """Renders the content of the resulting page after the simulation is completed. Displays the input values used
    in the simulation and provides a link to download the simulation log file."""
    template_name = 'simulator/export.html'
    myvars = models.CreateInput.objects.filter(uuid=num.id).values().last()
    fields = InputForm()
    return render(request,  template_name=template_name, context={'myvars': myvars, 'form': fields})


def export_csv(request):
    """writes simulation log file in '.csv' format and returns it as a response to be downloaded by the user"""
    uu_id = models.CreateInput.objects.values('uuid').last()['uuid']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="simulation_log.csv"'
    writer = csv.writer(response)
    writer.writerow(['shift_started', 'shift_finished', 'run', 'attempt_no', 'call_no', 'batch', 'queue', 'spin',
                     'capacity', 'attempt_started', 'if_unreachable',
                     'if_not_answering', 'answer_time', 'amd_time', 'if_dropped', 'wait_before_drop', 'wait_time',
                     'talk_time', 'clerical_time'])

    results = models.GlobalResults.objects.filter(uuid=uu_id).values_list('shift_started', 'shift_finished', 'run',
                                                                           'attempt_no', 'call_no', 'batch', 'queue',
                                                                           'spin', 'capacity',
                                                                           'attempt_started', 'if_unreachable',
                                                                           'if_not_answering', 'answer_time',
                                                                           'amd_time', 'if_dropped',
                                                                           'wait_before_drop', 'wait_time', 'talk_time',
                                                                           'clerical_time')

    for result in results:
        writer.writerow(result)

    models.GlobalResults.objects.filter(uuid=uu_id).delete()
    models.CreateInput.objects.filter(uuid=uu_id).delete()

    return response


class CallCenter:
    """The CallCenter class represents the logic of the call center business process. A unique instance of the class
    is created for each simulation run (variable 'simulation_number'). All variables for the init method are retrieved
     from the database (table CreateInput). To avoid issues with multiple users running the app simultaneously, each
     user is identified by a unique uuid, which is generated from the Uuid class"""
    def __init__(self, simulation_number, uuid):
        self.uuid = uuid
        self.name = 0
        self.simulation_number = simulation_number
        self.call_list = models.CreateInput.objects.values('call_list').last()['call_list']
        self.call_list = [i for i in range(1, self.call_list + 1)]
        self.batch = 1
        self.env = simpy.Environment()
        self.line_numbers = models.CreateInput.objects.values('line_numbers').last()['line_numbers']
        # total shift
        self.capacity = models.CreateInput.objects.values('number_of_agents').last()['number_of_agents']
        self.agent = simpy.Resource(self.env, capacity=self.capacity)
        # time being simulated in sec: number or None
        self.shift_time = models.CreateInput.objects.values('shift_time').last()['shift_time'] * 3600
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
        self.ring_time_l = models.CreateInput.objects.values('ring_time_l').last()['ring_time_l']
        self.ring_time_m = models.CreateInput.objects.values('ring_time_m').last()['ring_time_m']
        # share of reached customers from those who received a call (high, low, mode)
        self.reach_rate_h = models.CreateInput.objects.values('reach_rate_h').last()['reach_rate_h']
        self.reach_rate_l = models.CreateInput.objects.values('reach_rate_l').last()['reach_rate_l']
        self.reach_rate_m = models.CreateInput.objects.values('reach_rate_m').last()['reach_rate_m']
        # answering machine clearance duration parameters (high, low, mode)
        self.d_h = models.CreateInput.objects.values('d_h').last()['d_h']
        self.d_l = models.CreateInput.objects.values('d_l').last()['d_l']
        self.d_m = models.CreateInput.objects.values('d_m').last()['d_m']
        # talk time parameters (high, low)
        self.t_h = models.CreateInput.objects.values('t_h').last()['t_h']
        self.t_l = models.CreateInput.objects.values('t_l').last()['t_l']
        # clerical time parameters (high, low)
        self.c_h = models.CreateInput.objects.values('c_h').last()['c_h']
        self.c_l = models.CreateInput.objects.values('c_l').last()['c_l']
        self.queue = 0
        self.start = 0
        self.finish = 0

    def dial(self):
        """The dial method simulates the behavior of an autodialer and applies the logic of a funnel. It selects a
        portion of the call list (batch) based on the number of available lines and the current queue. If a number is
        unreachable, it is removed from the call list. If it is reached, it may result either in a list of answered
        calls ('talk') or not. If the attempt is not in the 'talk' list, the phone number becomes the last element of
        the call list. If it is in the 'talk' list, the accepting_call method is applied to that. Each batch is
        written to DB"""
        record1 = models.GlobalResults(shift_started=self.env.now)
        record1.uuid = self.uuid
        record1.save()
        counter = 0
        while len(self.call_list) > 0 and self.env.now < self.shift_time:
            start = self.env.now
            spin = counter / len(self.call_list)
            if self.queue:
                grab = ((self.line_numbers * (1 - self.unreachable_m) * self.reach_rate_m) - self.queue) //\
                       ((1 - self.unreachable_m) * self.reach_rate_m)

                batch = [i for y, i in enumerate(self.call_list) if y + 1 <= grab]
            else:
                batch = [i for y, i in enumerate(self.call_list) if y + 1 <= self.line_numbers]
            self.call_list = [i for i in self.call_list if i not in batch]

            for i in batch:
                counter += 1
                record = models.GlobalResults(run=self.simulation_number + 1)
                record.uuid = self.uuid
                record.queue = self.queue
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
        final_record = models.GlobalResults(shift_finished=self.env.now)
        final_record.uuid = self.uuid
        final_record.save()

    def accepting_call(self, call, answer_time):
        """It simulates how a call is handled. When a customer answers, the system checks if it is an answering
        machine for a certain duration. If the duration exceeds the customer's patience, the call is dropped and
        the phone number becomes the last element of the call list. If the call is not dropped, an agent is requested
        and the system waits for them until the customer's patience expires. If patience ends, the call is dropped and
        the phone number becomes the last element of the call list. If the call is not dropped, it is handled during the
        talk_time. The agent is then released and available for the next customer in the queue after the clerical_time.
        Each status is written to DB"""
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
            self.call_list += [call.name]
        else:
            with self.agent.request() as req:
                yield req | self.env.timeout(call.patience)
                self.queue = len(self.agent.queue)
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
                    self.call_list += [call.name]
        update_rec_at.save()

    def run(self):
        """The method is responsible for creating a simpy process and running the simulation environment"""
        self.env.process(self.dial())
        self.env.run()


class IncomingCall:
    """This class creates an instance of a customer, which is passed to the CallCenter class to simulate the call
    center business process. It should be noted that the IncomingCall class is a part of the simulation and not an
    actual representation of a customer in a call center. The name attribute represents the phone number of the
    customer, and the patience attribute represents the amount of time the customer is willing to wait on hold before
     hanging up"""
    def __init__(self, name):
        self.name = name
        self.patience = random.uniform(models.CreateInput.objects.values('p_h').last()['p_h'],
                                       models.CreateInput.objects.values('p_l').last()['p_l'])

