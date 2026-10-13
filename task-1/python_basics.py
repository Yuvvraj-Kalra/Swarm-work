#qn1
altitude_readings = [120.5, 135.2, 140.0, 155.8, 160.2, 185.0]
battery_voltage_readings = [12.6, 12.4, 12.1, 11.8, 11.5, 11.0]
temperature_readings = [45.2, 48.0, 52.5, 55.0, 60.1, 65.4]


def analyze_sensor(readings):
    mini=readings[0]
    maxi = readings[0]
    sumi=0
    count=0
    for i in readings:   #done without using inbuilt functions as specified in question
        sumi+=i
        if maxi<i:
            maxi=i
        elif mini>i:
            mini=i
        count+=1
            
    average = sumi / count
    return mini, maxi, average, count


# UI for sensor choice
print("""--- Question 1: Drone Sensor Analysis ---
Choose a sensor to analyze:
1. Altitude
2. Battery Voltage
3. Temperature""")

choice = input("Enter your choice (1, 2, or 3): ").strip()

if choice == "1":
  selected_sensor = "Altitude"
  readings = altitude_readings
  unsafe_limit = 180.0  # e.g., max safe altitude limit
  condition = "above"  # check if readings are above unsafe limit
elif choice == "2":
  selected_sensor = "Battery Voltage"
  readings = battery_voltage_readings
  unsafe_limit = 11.2  #low battery
  condition = "below"  
elif choice == "3":
  selected_sensor = "Temperature"
  readings = temperature_readings
  unsafe_limit = 60.0  # e.g., overheat warning limit
  condition = "above"  # check if readings exceed safe temp
else:
  print("Invalid choice.  assumes altitude.")
  selected_sensor = "Altitude"
  readings = altitude_readings
  unsafe_limit = 180.0
  condition = "above"

# Display readings andstatistics
print(f"\nAnalyzing {selected_sensor}:")
print(f"All Readings: {readings}")

mini, maxi, avg, cnt = analyze_sensor(readings)
print(f"Minimum Value: {mini}")
print(f"Maximum Value: {maxi}")
print(f"Average Value: {round(avg, 2)}")
print(f"Total Readings: {cnt}")

# Checks threshold, uses try except
try:
  user_threshold = float(
      input(f"\nEnter a threshold value for {selected_sensor}: ")
  )

  if condition == "above":
    threshold_count = sum(1 for r in readings if r > user_threshold)
    print(
        f"Number of readings above threshold ({user_threshold}):"
        f" {threshold_count}"
    )
  else:
    threshold_count = sum(1 for r in readings if r < user_threshold)
    print(
        f"Number of readings below threshold ({user_threshold}):"
        f" {threshold_count}"
    )

  if condition == "above":
    crossed_limit = any(r > unsafe_limit for r in readings)
  else:
    crossed_limit = any(r < unsafe_limit for r in readings)

  if crossed_limit:
    print(
        f"\nWARNING: {selected_sensor} readings have crossed the unsafe"
        f" limit of {unsafe_limit}!"
    )
  else:
    print(f"\n All {selected_sensor} readings are within safe limits.")

except ValueError:
  print("Invalid number entered for the threshold.")

#question 2

print("\n--- Question 2: Drone Information ---")

#drone dict
drone_info = {
    "Drone ID": "DRONE-9042X",
    "Model Name": "SkyHawk Pro 4K",
    "Current Altitude": 145.2, 
    "Battery Percentage": 84,  # in %
    "Flight Mode": "Autonomous Waypoint",
}

#drone info: 
for key, value in drone_info.items():
  print(f"{key}: {value}")



#qn 3 creates file first

file_name = "flight_log.txt"

with open(file_name, "w") as file:
    file.write("Flight_ID, Date, Duration_Min, Status\n")
    file.write("FL-001, 2026-06-01, 25, Success\n")
    file.write("FL-002, 2026-06-03, 18, Success\n")
try:
    print("\nReading existing flight log contents:")
    with open(file_name, "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found.")
except IOError:
    print("Error: An issue occurred while reading the file.")

# Step 3: Add a new flight record to the file
new_record = "FL-003, 2026-06-05, 30, Success\n"

try:
    with open(file_name, "a") as file:
        file.write(new_record)
        print(f"Successfully added new record: {new_record.strip()}")

  # Verify by reading updated contents
    print("\nUpdated flight log contents:")
    with open(file_name, "r") as file:
        print(file.read())

except IOError:
    print("Error: Could not write to the flight log file.")