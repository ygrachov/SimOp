from django.db import models

# Create your models here.
class CreateInput(models.Model):
    number_of_simulations = models.IntegerField(help_text="How many times the whole process is reproduced")
    line_numbers = models.IntegerField(help_text="How many lines assigned to your call center")
    number_jf_agents = models.IntegerField(help_text="How many people are serving calls")
    shift_time = models.FloatField(help_text="How long the shift lasts in hours, decimal")
    call_list = models.IntegerField(help_text="How many calls have to be served")
    take_high = models.FloatField(help_text="max. time to load the dialer in sec, decimal")
    take_low = models.FloatField(help_text="min.time to load the dialer in sec, decimal")
    take_mode = models.FloatField(help_text="avg time to load the dialer in sec, decimal")
    unreachable_h = models.FloatField(help_text="max. share of unsuccessful attempts in butch, decimal")
    unreachable_l = models.FloatField(help_text="min. share of unsuccessful attempts in butch, decimal")
    unreachable_m = models.FloatField(help_text="avg. share of unsuccessful attempts in butch, decimal")
    ring_time_h = models.FloatField(help_text="max.ringing time in sec, decimal")
    ring_time_l = models.FloatField(help_text="min.ringing time in sec, decimal")
    ring_time_m = models.FloatField(help_text="avg.ringing time in sec, decimal")
    reach_rate_h = models.FloatField(help_text="max.share of answered customers from those who received "
                                                "a call, decimal")
    reach_rate_l = models.FloatField(help_text="min.share of answered customers from those who received "
                                                "a call, decimal")
    reach_rate_m = models.FloatField(help_text="avg.share of answered customers from those who received "
                                                "a call, decimal")
    d_h = models.FloatField(help_text="max.time answering machine detection takes in sec, decimal")
    d_l = models.FloatField(help_text="min.time answering machine detection takes in sec, decimal")
    d_m = models.FloatField(help_text="avg.time answering machine detection takes in sec, decimal")
    p_h = models.FloatField(help_text="max.time customer is willing to wait for agent after answering in sec, decimal")
    p_l = models.FloatField(help_text="min.time customer is willing to wait for agent after answering in sec, decimal")
    t_h = models.FloatField(help_text="max.talk time between agent and customer in sec, decimal")
    t_l = models.FloatField(help_text="min.talk time between agent and customer in sec, decimal")
    c_h = models.FloatField(help_text="max.time to put conversation results in the system in sec, decimal")
    c_l = models.FloatField(help_text="min.time to put conversation results in the system in sec, decimal")

class GlobalResults(models.Model):
    run = models.IntegerField(null=True)
    attempt_no = models.IntegerField(null=True)
    call_no = models.IntegerField(null=True)
    batch = models.IntegerField(null=True)
    queue = models.IntegerField(null=True)
    spin = models.FloatField(null=True)
    capacity = models.IntegerField(null=True)
    attempt_started = models.FloatField(null=True)
    if_unreachable = models.IntegerField(null=True)
    if_not_answering = models.IntegerField(null=True)
    answer_time = models.FloatField(null=True)
    amd_time = models.FloatField(null=True)
    if_dropped = models.IntegerField(null=True)
    wait_before_drop = models.FloatField(null=True)
    wait_time = models.FloatField(null=True)
    talk_time = models.FloatField(null=True)
    clerical_time = models.FloatField(null=True)

    class Meta:
        indexes = [models.Index(fields=['run', 'call_no', 'batch']),]
