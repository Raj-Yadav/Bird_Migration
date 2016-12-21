
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

birddata = pd.read_csv("bird_tracking.csv")

birddata.head(2)
bird_names = birddata.bird_name.unique()

### ploting path of all three bird 
plt.figure(figsize=(8,8))
for bird_name in bird_names:
    ix = birddata.bird_name == bird_name
    y, x = birddata.latitude[ix], birddata.longitude[ix]
    plt.plot(x, y,".", label=bird_name)
plt.ylabel = "latitude"
plt.xlabel = "longitude"
plt.legend(loc = "lower right")
plt.show()
plt.savefig("bird_trag.pdf")

### plotting speed data of bird
plt.figure(figsize=(10,10))
speed = birddata.speed_2d
ind = np.isnan(speed)
plt.hist(speed[~ind], bins = np.linspace(0, 30, 20), normed = True)
plt.xlabel("2D speed m/s")
plt.ylabel("Frequency")
plt.show()
plt.savefig("hist.pdf")

################
## Dealing with timestemp data
type(birddata.date_time[0])  ## given datatype is string, need datetime type
import datetime
timestemp = []
for k in range(len(birddata)):
    timestemp.append(datetime.datetime.strptime(birddata.date_time.iloc[k][:-3],\
                                                "%Y-%m-%d %H:%M:%S"))

birddata["timestemp"] = pd.Series(timestemp, index = birddata.index)

#birddata.timestemp[3] - birddata.timestemp[2]
times = birddata.timestemp[birddata.bird_name == "Eric"]
elasped_time = [time - times[0] for time in times]
plt.plot(np.array(elasped_time) / datetime.timedelta(days = 1))
plt.xlabel("observation")
plt.ylabel("Elasped time (days)")
plt.savefig("timeplot.pdf")

### calculating daily_mean_speed of one bird and plotting it.
data = birddata[birddata.bird_name == "Eric"]
times = data.timestemp
elasped_time = [time - times[0] for time in times]
elasped_day = np.array(elasped_time) / datetime.timedelta(days = 1) 

next_day = 1
ind = []
daily_mean_speed = []
for i, t in enumerate(elasped_day):
    if t < next_day:
        ind.append(i)
    else:
        daily_mean_speed.append(np.mean(data.speed_2d[ind]))
        next_day += 1
        ind = []

plt.figure(figsize=(8,7))
plt.plot(daily_mean_speed)
plt.xlabel("Days")
plt.ylabel("Daily mean (m/s)")
plt.savefig("dms.pdf")

### Plotting 3D plot
import cartopy.crs as ccrs
import cartopy.feature as cfeature
proj = ccrs.Mercator()
plt.figure(figsize=(10,10))
ax = plt.axes(projection=proj)
ax.set_extent((-25.0, 20.0, 52.0, 10))
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
for bird_name in bird_names:
    ix = birddata.bird_name == bird_name
    y, x = birddata.latitude[ix], birddata.longitude[ix]
    ax.plot(x, y,".", transform=ccrs.Geodetic(), label=bird_name)
plt.legend(loc="upper left")
plt.savefig("map1.pdf")











