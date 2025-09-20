#Write a Python program that asks the user for their age. If the age is 18 or 
# older, print “You are an adult.” If the age is between 13 and 17, print 
# “You are a teenager.” Otherwise, print “You are a child...” 

def life_stage():
  age = float(input("Enter your age here: "))
  if age > 18:
    print("You are an adult.")
  elif 18 > age > 13:
    print("You are a teenager")
  else: print("You are a child")

life_stage()