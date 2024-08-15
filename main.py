version = 0
# DO NOT CHANGE THAT
config = "alpha"

if version == 0:
    print("SATAIS version ALPHA 0.1 EN")
else:
    print("Please update your fork!")

Username = str(input("Please enter your Username "))
if Username == "":
    print("Your Username cannot be empty !")
    str(input("Please enter your Username "))

print ("Welcome", Username, "!")
