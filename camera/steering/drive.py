import steer


steer.setup()

while True:
    user_input = raw_input("Direction")

    if(user_input =="r"):
        steer.right()
    else if(user_input == "l"):
        steer.left()
    else if(user_input == "f"):
        steer.forward()
    else if(user_input == "b"):
        steer.back()
    else if(user_input == "s"):
        steer.stop()
