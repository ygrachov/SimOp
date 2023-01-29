from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CreateInput(models.Model):
    number_of_simulations = models.IntegerField(default=1, validators=[MaxValueValidator(10),
                                                MinValueValidator(1)],
                                                help_text="how many times the entire process is repeated")
    line_numbers = models.IntegerField(default=100, validators=[MinValueValidator(1)],
                                       help_text="number of lines assigned to your call center")
    number_of_agents = models.IntegerField(default=20, validators=[MinValueValidator(1)],
                                           help_text="number of people handling calls")
    shift_time = models.FloatField(default=8, validators=[MaxValueValidator(12)],
                                   help_text="duration of the shift, measured in hours")
    call_list = models.IntegerField(default=10000, validators=[MinValueValidator(1), MaxValueValidator(40000)],
                                    help_text="number of clients that need to be contacted")
    take_high = models.FloatField(default=4, validators=[MinValueValidator(0.0)],
                                  help_text="maximum time it takes to load the dialer, measured in seconds")
    take_low = models.FloatField(default=2, validators=[MinValueValidator(0.0)],
                                 help_text="minimum time it takes to load the dialer, measured in seconds")
    take_mode = models.FloatField(default=3, validators=[MinValueValidator(0.0)],
                                  help_text="average time it takes to load the dialer, measured in seconds")
    unreachable_h = models.FloatField(default=0.3, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                      help_text="maximum percentage of unsuccessful attempts in a batch")
    unreachable_l = models.FloatField(default=0.1, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                      help_text="minimum percentage of unsuccessful attempts in a batch")
    unreachable_m = models.FloatField(default=0.2, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                      help_text="average percentage of unsuccessful attempts in a batch")
    ring_time_h = models.FloatField(default=45, validators=[MinValueValidator(1.0)],
                                    help_text="maximum longest duration, in seconds, that a call will ring before"
                                              " being considered as unanswered")
    ring_time_l = models.FloatField(default=5, validators=[MinValueValidator(1.0)],
                                    help_text="shortest duration, in seconds, that a call will ring before being "
                                              "considered as unanswered")
    ring_time_m = models.FloatField(default=15, validators=[MinValueValidator(1.0)],
                                    help_text="average duration, in seconds, that a call will ring before being "
                                              "considered as unanswered")
    reach_rate_h = models.FloatField(default=0.5, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                     help_text="highest percentage of customers who answered the call out of those who "
                                               "received it")
    reach_rate_l = models.FloatField(default=0.01, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                     help_text="lowest percentage of customers who answered the call out of those who "
                                               "received it")
    reach_rate_m = models.FloatField(default=0.3, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                     help_text="average percentage of customers who answered the call out of those who "
                                               "received it")
    d_h = models.FloatField(default=10, validators=[MinValueValidator(0.0)],
                            help_text="longest duration, in seconds, that the system takes to detect answering machine")
    d_l = models.FloatField(default=1, validators=[MinValueValidator(0.0)],
                            help_text="shortest duration, in seconds, that the system takes to detect answering machine")
    d_m = models.FloatField(default=4, validators=[MinValueValidator(0.0)],
                            help_text="average duration, in seconds, that the system takes to detect answering machine")
    p_h = models.FloatField(default=15, validators=[MinValueValidator(0.0)], help_text="longest duration, in seconds,"
                            " that a customer is willing to wait for an agent after answering the call")
    p_l = models.FloatField(default=6, validators=[MinValueValidator(0.0)], help_text="shortest duration, in seconds,"
                            " that a customer is willing to wait for an agent after answering the call")
    t_h = models.FloatField(default=90, validators=[MinValueValidator(0.0)], help_text="longest duration, in seconds, "
                            "of a conversation between a client and an agent")
    t_l = models.FloatField(default=2, validators=[MinValueValidator(0.0)], help_text="shortest duration, in seconds, "
                            "of a conversation between a client and an agent")
    c_h = models.FloatField(default=10, validators=[MinValueValidator(0.0)], help_text=" maximum amount of time, "
                            "in seconds, required to enter the results of a conversation into the system")
    c_l = models.FloatField(default=4, validators=[MinValueValidator(0.0)], help_text="minimum amount of time, "
                            "in seconds, required to enter the results of a conversation into the system")
    uuid = models.CharField(null=True, max_length=100)



class GlobalResults(models.Model):
    shift_started = models.CharField(null=True, max_length=10)
    uuid = models.CharField(null=True, max_length=100)
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
    agent = models.CharField(null=True, max_length=100)
    talk_time = models.FloatField(null=True)
    clerical_time = models.FloatField(null=True)
    shift_finished = models.CharField(null=True, max_length=100)

    class Meta:
        indexes = [models.Index(fields=['run', 'call_no', 'batch']),]
