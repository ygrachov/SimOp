import simpy
import random
import pandas as pd



# class Globals:
#     # TODO add prediction mode: reducing number of line upon resources availability
#     # TODO add light computations for big simulations
#     """stores variables used for simulation. It can simulate either a period of time or certain number of calls"""
#     env = simpy.Environment()
#     # how many times the whole process is reproduced
#     number_of_simulations = 1
#     # how many lines are available for dialer
#     line_number = 300
#     # total shift
#     number_of_agents = 45
#     # time being simulated in sec: number or None
#     shift_time = None
#     # number of customers to be served
#     call_list = 600
#     # time required to take and dial a batch(high, low, mode)
#     take_h = 5
#     take_low = 1
#     take_mode = 3.5
#     # the share of unsuccessful attempts in batch (high, low, mode)
#     unreachable_h = 0.6
#     unreachable_l = 0.2
#     unreachable_m = 0.4
#     # time between point of call starts ringing and call gets answered or cancelled (high, low, mode)
#     ring_time_h = 45
#     ring_time_l = 3
#     ring_time_m = 18
#     # share of reached customers from those who received a call (high, low, mode)
#     reach_rate_h = 0.3
#     reach_rate_l = 0.5
#     reach_rate_m = 0.15
#     # answering machine clearance duration parameters (high, low, mode)
#     d_h = 10
#     d_l = 0
#     d_m = 3
#     # customer's patience parameter (high, low)
#     p_h = 11
#     p_l = 4
#     # talk time parameters (high, low)
#     t_h = 90
#     t_l = 20
#     # clerical time parameters (high, low)
#     c_h = 10
#     c_l = 5
#     # dataframe to record statistics on each call
#     results = pd.DataFrame()

#
# class CallCenter:
#     """represents call center """
#
#     def __init__(self, simulation_number):
#         self.name = 0
#         self.capacity = views.Globals.number_of_agents
#         self.agent = simpy.Resource(views.Globals.env, capacity=self.capacity)
#         self.simulation_number = simulation_number
#         self.call_list = [i for i in range(1, views.Globals.call_list + 1)]
#         self.batch = 1
#
#     def dial(self):
#         counter = 0
#         while len(self.call_list) > 0:
#             batch_result = pd.DataFrame()
#             start = views.Globals.env.now
#             spin = counter / len(self.call_list)
#             batch = [i for y, i in enumerate(self.call_list) if y + 1 <= Globals.line_number]
#             self.call_list = [i for i in self.call_list if i not in batch]
#             for i in batch:
#                 counter += 1
#                 batch_result.loc[i, 'run'] = self.simulation_number + 1
#                 batch_result.loc[i, 'attempt_no'] = counter
#                 batch_result.loc[i, 'call_no'] = i
#                 batch_result.loc[i, 'batch'] = self.batch
#                 batch_result.loc[i, 'spin'] = spin
#                 batch_result.loc[i, 'capacity'] = self.capacity
#                 batch_result.loc[i, 'attempt_started'] = start
#             self.call_list = [i for i in self.call_list if i not in batch]
#             yield Globals.env.timeout(random.triangular(high=Globals.take_h, low=Globals.take_low,
#                                                         mode=Globals.take_mode))
#             unreached = random.sample(population=batch, k=round(random.triangular(high=Globals.unreachable_h,
#                                                                                   low=Globals.unreachable_l,
#                                                                                   mode=Globals.unreachable_m) *
#                                                                 len(batch)))
#             for i in batch:
#                 batch_result.loc[i, 'if_unreachable'] = 1 if i in unreached else None
#             batch = [i for i in batch if i not in unreached]
#             yield Globals.env.timeout(random.triangular(high=Globals.ring_time_h, low=Globals.ring_time_l,
#                                                         mode=Globals.ring_time_m))
#             talks = random.sample(population=batch, k=round(len(batch) * random.triangular(high=Globals.reach_rate_h,
#                                                                                            low=Globals.reach_rate_l,
#                                                                                            mode=Globals.reach_rate_m)))
#             for i in batch:
#                 batch_result.loc[i, 'if_not_answering'] = 1 if i not in talks else None
#             self.call_list += [i for i in batch if i not in talks]
#             Globals.results = pd.concat([Globals.results, batch_result], ignore_index=True)
#             for i in talks:
#                 answer_time = Globals.env.now
#                 call = IncomingCall(i)
#                 Globals.env.process(self.accepting_call(call, answer_time))
#             self.batch += 1
#
#     def accepting_call(self, call, answer_time):
#         answer_time = answer_time
#         Globals.results.loc[(Globals.results['call_no'] == call.name) & (Globals.results['if_unreachable'] != 1)
#                             & (Globals.results['if_not_answering'] != 1) & (Globals.results['run'] ==
#                                                                             self.simulation_number + 1),
#                             'answer_time'] = answer_time
#         duration = random.triangular(low=Globals.d_l, high=Globals.d_h, mode=Globals.d_m)
#         Globals.results.loc[(Globals.results['call_no'] == call.name) & (Globals.results['answer_time'] >= 0)
#                             & (Globals.results['run'] == self.simulation_number + 1),
#                             'amd_time'] = duration
#         yield Globals.env.timeout(min(duration, call.patience))
#         call.patience = call.patience - duration if duration < call.patience else 0
#         if call.patience == 0:
#             Globals.results.loc[(Globals.results['call_no'] == call.name) & (
#                     Globals.results['answer_time'] >= 0) & (Globals.results['run'] == self.simulation_number + 1),
#                                 'if_dropped'] = 1
#             Globals.results.loc[(Globals.results['call_no'] == call.name) & (
#                     Globals.results['answer_time'] >= 0) & (Globals.results['run'] == self.simulation_number + 1),
#                                 'wait_before_drop'] = Globals.env.now - answer_time
#         else:
#             with self.agent.request() as req:
#                 yield req | Globals.env.timeout(call.patience)
#                 if req.triggered:
#                     wait_time = Globals.env.now - answer_time
#                     Globals.results.loc[(Globals.results['call_no'] == call.name) & (
#                             Globals.results['answer_time'] >= 0) & (Globals.results['run']
#                                                                     == self.simulation_number + 1),
#                                         'wait_time'] = wait_time
#                     talk_time = random.uniform(Globals.t_l, Globals.t_h)
#                     Globals.results.loc[(Globals.results['call_no'] == call.name) & (
#                             Globals.results['answer_time'] >= 0) &
#                                         (Globals.results['run'] == self.simulation_number + 1), 'talk_time'] = talk_time
#                     yield Globals.env.timeout(talk_time)
#                     clerical_time = random.uniform(Globals.c_l, Globals.c_h)
#                     Globals.results.loc[(Globals.results['call_no'] == call.name) & (
#                             Globals.results['answer_time'] >= 0) &
#                                         (Globals.results[
#                                              'run'] == self.simulation_number + 1), 'clerical_time'] = clerical_time
#                     yield Globals.env.timeout(clerical_time)
#                 else:
#                     Globals.results.loc[(Globals.results['call_no'] == call.name) & (
#                             Globals.results['answer_time'] >= 0) & (Globals.results['run'] ==
#                                                                     self.simulation_number + 1), 'if_dropped'] = 1
#                     Globals.results.loc[(Globals.results['call_no'] == call.name) & (
#                             Globals.results['answer_time'] >= 0) & (Globals.results['run'] ==
#                                                                     self.simulation_number + 1), 'wait_before_drop'] = \
#                         Globals.env.now - answer_time
#
#     def run(self):
#         Globals.env.process(self.dial())
#         Globals.env.run()
#
#
# class IncomingCall:
#     def __init__(self, name):
#         self.name = name
#         self.patience = random.uniform(Globals.p_l, Globals.p_h)
#
#
# for simulation_number in range(Globals.number_of_simulations):
#     print(f'run # {simulation_number}')
#     Globals.env = simpy.Environment()
#     call_center = CallCenter(simulation_number)
#     call_center.run()
# print('wruting results to the file...')
# Globals.results.to_excel('simulation_log.xlsx', index=False, sheet_name='CDR log')
