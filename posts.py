from psaw import PushshiftAPI
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta


api = PushshiftAPI()
start_epoch = int(datetime(2020, 10, 1).timestamp())
end_epoch = int(datetime(2020, 11, 1).timestamp())
date = []
time = ['07:00', '07:30', '08:00', '08:30', '09:00', '09:30',
        '10:00', '10:30',
        '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30',
        '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
        '20:00', '20:30', '21:00', '21:30', '22:00', '22:30',
        '23:00', '23:30',
        '00:00', '00:30', '01:00', '01:30', '02:00', '02:30',
        '03:00', '03:30', '04:00', '04:30', '05:00', '05:30',
        '06:00', '06:30']
while True:
    results = list(api.search_submissions(before=end_epoch,
                                after=start_epoch,
                                subreddit='desabafos',
                                filter=['url', 'author', 'title', 'subreddit'],
                                limit=100))
    if not results:
        break

    for post in results:
        day = datetime.fromtimestamp(post[1]).strftime("%d-%m-%Y")
        date.append(day)
        hour = datetime.fromtimestamp(post[1])
        hour_round = ceil_dt(hour, timedelta(minutes=30))
        hour_round = hour_round.strftime('%H:%M')
        time.append(hour_round)

    end_epoch = results[-1][1]

data = {'Time': time}
df = pd.DataFrame(data, columns=['Time'])
print(len(time))
sns.set()
sns.set_style("ticks")
plt.hist(df['Time'], bins=48)
plt.xticks(rotation=45, ha='center')
ax = plt.gca()
xticks = ax.xaxis.get_major_ticks()
for i in range(48):
    if (i % 2) == 0:
        xticks[(i+1)].label1.set_visible(False)
plt.title('Posts por horário no r/desabafos em outubro')
plt.xlabel('Horário')
plt.ylabel('Qtde de posts')
plt.show()