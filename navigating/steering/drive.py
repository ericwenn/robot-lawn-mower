import steer

steer.setup()

while True:
	user_input = raw_input("Direction: ")
	
	if(user_input =="r"):
		steer.right()
	elif(user_input=="l"):
		steer.left()
	elif(user_input =="f"):
		steer.forward()
	elif(user_input=="b"):
		steer.back()
	elif(user_input=="s"):
		steer.stop()
	elif(user_input =="exit"):
		steer.stop()
		break
