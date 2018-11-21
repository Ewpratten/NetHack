import sys
import matplotlib.pyplot as plt

exclude_vendors = ["Aruba Networks", ""]

with open(sys.argv[1], "r") as f:
	data = str(f.read())
	f.close()

data = data.replace("'", '"')

data = dict(eval(data))["data"]
i = 0
for device in data:
	device = data[i]["mac"]
	if data[i]["vendor"] in exclude_vendors:
		i += 1
		continue
	print(data[i]["mac"]+ " - "+ str(data[i]["vendor"])+ " ("+ str(len(data[i]["readings"])) + ") " )
	i += 1

print("Who to parse?")
mac = input(">")

i = 0
for dev in data:
	if data[i]["mac"] == mac:
		device = data[i]
		break
	i += 1

print(device["vendor"] +" "+ device["mac"])

legnths = []
times = []
for datapoint in device["readings"]:
	legnths.append(float(datapoint[0]) * -1)
	times.append(float(datapoint[1]))
	print(str(datapoint[1]) +" "+ str(datapoint[0]))

print("--- Visualization ---")

for datapoint in legnths:
	print("#" * round(datapoint))

print("Generating line graph")
plt.plot(times, legnths, color='g')
plt.xlabel('Time')
plt.ylabel('Power')
plt.title("Mapping for: " + mac)
plt.savefig(sys.argv[1]+"-"+mac+".png")
print(sys.argv[1]+"-"+mac+".png")