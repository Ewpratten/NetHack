import sys
import matplotlib.pyplot as plt

exclude_vendors = ["Aruba Networks", ""]

with open(sys.argv[1], "r") as f:
	data = str(f.read())
	f.close()

with open("./known_macs.txt", "r") as f:
	known = str(f.read())
	f.close()

known_o = known.split("\n")
known = {}
for line in known_o:
	x = line.split(" @ ")
	known[x[0]] = x[1]

data = data.replace("'", '"')

data = dict(eval(data))["data"]
i = 0
for device in data:
	device = data[i]["mac"]
	if data[i]["vendor"] in exclude_vendors:
		i += 1
		continue
	name_str = ""
	if device in known:
		name_str = " - "+ known[device]
	print(data[i]["mac"]+ " - "+ str(data[i]["vendor"])+ " ("+ str(len(data[i]["readings"])) + ") " + name_str)
	i += 1

print("Who to parse?")
mac = input(">")

if mac == "master":
	
	i = 0
	for device in data:
		times = []
		powers = []
		device = data[i]["mac"]
		if data[i]["vendor"] in exclude_vendors:
			i += 1
			continue
		for reading in data[i]["readings"]:
			times.append(reading[1])
			powers.append(reading[0])
		plt.plot(times, powers)
		i += 1
	
	plt.xlabel('Time')
	plt.ylabel('Power')
	plt.title("Mapping for all")
	plt.savefig(sys.argv[1]+"-"+mac+".png")
	print(sys.argv[1]+"-"+mac+".png")
	exit()

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