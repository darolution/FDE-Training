# Launchpad L2 - your first program.
# Run it from the course folder:   python labs/launchpad/l2/hello.py
# Then change things and run it again. Breaking it is part of learning.

name = input("What's your name? ")
hours_per_week = float(input("How many hours a week can you study? "))

weeks = 32
total_hours = hours_per_week * weeks

print(f"Nice to meet you, {name}.")
print(f"At {hours_per_week} hours a week, the full course is about {total_hours:.0f} hours of practice.")
print("Every one of them counts. Let's go!")
