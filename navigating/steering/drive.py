import steer


steer.setup()

while True:
    user_input = raw_input("Direction: ")

    if(user_input =="r"):
        steer.right()
        #print("r")
    elif(user_input == "l"):
        steer.left()
        #print("l")
    elif(user_input == "f"):
        steer.forward()
        #print("f")
    elif(user_input == "b"):
        steer.back()
        #print("b")
    elif(user_input == "s"):
        steer.stop()
        #print("s")
