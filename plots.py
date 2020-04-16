############################## IPFS Statistics ################################
# 1. Total number of Peers in the two days of monitoring                      #
# 2. Number of Peers per country/city (Pie plot)                              #
# 3. Average global latency                                                   #
# 4. Average country latency                                                  #
# 5. Day behavior of connected peers for the two days (bar plot)              #
# 6. Average hour behavior of connected peers between the two days (bar plot) #
###############################################################################

# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json
import dateutil.parser
import operator
import collections

# Some variables
data = None
total_peers = 0
not_assigned_latency = 0
global_latency = []
country_latency = {}
num_peers_country = {}
num_peers_city = {}
num_peers_hour = {}
latency_per_country = {}
all_peers = {}
unique_peers = {}
double_peers = {}

# Some functions
def checkCountryLatency(country, latency):
    if country in latency_per_country:
        latency_per_country[country].append(latency)
    else:
        latency_per_country[country] = []
        latency_per_country[country].append(latency)

# Open JSON file obtained by the NodeJS app
with open('ipfs_monitoring.json') as json_file:
    data = json.load(json_file)
    total_peers = len(data['Peers'])

# Update data adding two hours
for peer in data['Peers']:
    isoDate = dateutil.parser.isoparse(peer['Timestamp'])
    correctDate = datetime.datetime(isoDate.year, isoDate.month, isoDate.day, isoDate.hour)

    # 5. Number of Peers every hour (line plot)
    key = correctDate.strftime("%H:00 - %d %B")

    if key in num_peers_hour:
        num_peers_hour[key] += 1
    else:
        num_peers_hour[key] = 1

    # 2. Number of Peers per country/city
    key = peer['Country']

    if key in num_peers_country:
        num_peers_country[key] += 1
    else:
        num_peers_country[key] = 1

    key = peer['City']

    if key in num_peers_city:
        num_peers_city[key] += 1
    else:
        num_peers_city[key] = 1

    # 3. Average global latency
    if peer['Latency'] != 'n/a':
        if 'ms' in peer['Latency']:
            # Global latency value
            latency = float(peer['Latency'].split('ms')[0])
            global_latency.append(latency)
            all_peers[peer['Peer']] = (latency, peer['Country'], peer['City'], peer['IPv4'])
            
            # Average latency per country
            checkCountryLatency(peer['Country'], latency)
            
        # For some peers could be seconds of latency (converted to ms)
        elif 's' in peer['Latency']:
            # Global latency value
            latency = float(peer['Latency'].split('s')[0])
            latency *= 1000
            global_latency.append(latency)
            all_peers[peer['Peer']] = (latency, peer['Country'], peer['City'], peer['IPv4'])

            # Average latency per country
            checkCountryLatency(peer['Country'], latency)
    else:
        not_assigned_latency += 1
    
    if peer['Peer'] in unique_peers:
        if peer['Peer'] not in double_peers:
            double_peers[peer['Peer']] = 1
        else:
            double_peers[peer['Peer']] += 1
    else:
        unique_peers[peer['Peer']] = 1

print('Number of unique peers:')
print(sum(unique_peers.values()))
print('Number of peers monitored multiple times:')
print(sum(double_peers.values()))

# Latency distribution
# latencies_distribution = {'50': 0, '100': 0, '150': 0, '200': 0, '250': 0, '300': 0, '350': 0,
#                           '400': 0, '450': 0, '500+': 0}

# for peer in all_peers.items():
#     real_latency = peer[1][0]
#     approx_latency = int(peer[1][0])

#     if len(str(approx_latency)) is 2:
#         latencies_distribution['50'] += 1
#     elif len(str(approx_latency)) is 4:
#         latencies_distribution['500+'] += 1
#     else:
#         if 50 <= approx_latency < 100:
#             latencies_distribution['50'] += 1
#         elif 100 <= approx_latency < 150:
#             latencies_distribution['100'] += 1
#         elif 150 <= approx_latency < 200:
#             latencies_distribution['150'] += 1
#         elif 200 <= approx_latency < 250:
#             latencies_distribution['200'] += 1
#         elif 250 <= approx_latency < 300:
#             latencies_distribution['250'] += 1
#         elif 300 <= approx_latency < 350:
#             latencies_distribution['300'] += 1
#         elif 350 <= approx_latency < 400:
#             latencies_distribution['350'] += 1
#         elif 400 <= approx_latency < 450:
#             latencies_distribution['400'] += 1
#         elif 450 <= approx_latency < 500:
#             latencies_distribution['450'] += 1

# num_peers_latencies = sum(latencies_distribution.values())
# names = []
# values = []
# perc = []

# for latency in latencies_distribution.items():
#     names.append(latency[0])
#     values.append(latency[1])
#     perc.append(str(int((latency[1] / num_peers_latencies) * 100)))

# print(perc)

# plt.bar(names, values)
# plt.xticks(names, names, rotation='vertical')
# # plt.yticks(names, perc)
# plt.xlabel('Latency values in milliseconds')
# plt.ylabel('Number of peers')
# plt.show()

# print('Total number of peers: ' + str(total_peers))
# print('Peers per hour')
# print(num_peers_hour)
# # Remove n/a peer's city
# del num_peers_city['']
# print('Peers per city')
# ordered_city = sorted(num_peers_city.items(), key = operator.itemgetter(1))
# print(list(reversed(ordered_city)))
# print('Peers per country')
# ordered_country = sorted(num_peers_country.items(), key = operator.itemgetter(1))
# print(list(reversed(ordered_country)))
# avg_global_latency = "{:.3f}ms".format(np.sum(global_latency) / float(len(global_latency)))
# print('Global average latency: ' + avg_global_latency)
# print('Number of peers without latency: ' + str(not_assigned_latency))
# print('Average country latency')
# avg_country_latency = {}
# del latency_per_country['']
# for country, latencies in latency_per_country.items():
#     avg_country_latency[country] = float("{:.3f}".format(np.sum(latencies) / float(len(latencies))))

# ordered_avg_country_latency = sorted(avg_country_latency.items(), key = operator.itemgetter(1))
# print(list(ordered_avg_country_latency))
# print('Peer with best latency:')
# ordered_peers = sorted(all_peers.items(), key = operator.itemgetter(1))
# print(list(ordered_peers)[1])
# print('Peer with worst latency:')
# print(list(ordered_peers)[-1])
# 7. Average hour behavior of connected peers between the two days (bar plot)
# print('Ordered peer per day')
# ordered_peer_hour = collections.OrderedDict(sorted(num_peers_hour.items()))

# hours = [i.split(' - ')[0] for i in ordered_peer_hour]
# names = list(dict.fromkeys(hours))
# values = []
# sum = 0
# sum_length = 0
# day_hour = '00:00'

# for hour in ordered_peer_hour.items():
#     if day_hour != hour[0].split(' - ')[0]:
#         day_hour = hour[0].split(' - ')[0]
#         values.append(sum / sum_length)
#         sum = 0
#         sum_length = 0
#         sum += hour[1]
#         sum_length += 1
#     else:
#         if hour[0] == list(ordered_peer_hour.keys())[-1]:
#             sum += hour[1]
#             sum_length += 1
#             values.append(sum / sum_length)
#         else:
#             sum += hour[1]
#             sum_length += 1

# fig, axs = plt.subplots()
# axs.bar(names, values)
# plt.xticks(names, names, rotation='vertical')
# fig.suptitle('Average hour-behaviour in the considered period')

# plt.show()

# 5. Number of Peers every hour (bar plot)
# dictionary = {'10:00 - 14 April': 43, '11:00 - 14 April': 909, '12:00 - 14 April': 881, '13:00 - 14 April': 962, 
# '14:00 - 14 April': 938, '15:00 - 14 April': 891, '16:00 - 14 April': 993, '17:00 - 14 April': 1019, 
# '18:00 - 14 April': 1008, '19:00 - 14 April': 1074, '20:00 - 14 April': 1060, '21:00 - 14 April': 1070,
#  '22:00 - 14 April': 1065, '23:00 - 14 April': 1051, '00:00 - 15 April': 1006, '01:00 - 15 April': 1044, 
# '02:00 - 15 April': 1065, '03:00 - 15 April': 1003, '04:00 - 15 April': 1037, '05:00 - 15 April': 991,
#  '06:00 - 15 April': 1112, '07:00 - 15 April': 743, '08:00 - 15 April': 771, '09:00 - 15 April': 775, '10:00 - 15 April': 754, '11:00 - 15 April': 767, '12:00 - 15 April': 716, '13:00 - 15 April': 748, '14:00 - 15 April': 757, '15:00 - 15 April': 749, '16:00 - 15 April': 718, '17:00 - 15 April': 729, '18:00 - 15 April': 751, 
# '19:00 - 15 April': 761, '20:00 - 15 April': 787, '21:00 - 15 April': 777, '22:00 - 15 April': 780, 
# '23:00 - 15 April': 777, '00:00 - 16 April': 786, '01:00 - 16 April': 774, '02:00 - 16 April': 740, 
# '03:00 - 16 April': 758, '04:00 - 16 April': 743, '05:00 - 16 April': 745, '06:00 - 16 April': 755, 
# '07:00 - 16 April': 865, '08:00 - 16 April': 845, '09:00 - 16 April': 841,
#  '10:00 - 16 April': 942}
# names = []
# values = []

# for day in dictionary.items():
#     names.append(day[0])
#     values.append(day[1])

# plt.bar(names, values)
# plt.xticks(names, names, rotation='vertical')
# plt.xlabel('Days of monitoring')
# plt.ylabel('Number of peers')
# plt.show()

# 2. Number of Peers per country and average latency (Pie plot)
# first_n_elems = list(reversed(ordered_country))[:6]
# labels = [i[0] for i in first_n_elems]
# sizes = [i[1] for i in first_n_elems]

# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, shadow=False, startangle=90)
# ax1.axis('equal')
# plt.title('Top 6 countries per number of peers')
# plt.legend(labels)

# plt.show()

# 2. Number of Peers per city (Pie plot)
# first_n_elems = list(reversed(ordered_city))[:6]
# labels = [i[0] for i in first_n_elems]
# sizes = [i[1] for i in first_n_elems]

# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, labels=sizes, shadow=False, startangle=90)
# ax1.axis('equal')
# plt.legend(labels)
# plt.title('Top 6 cities per number of peers')

# plt.show()
