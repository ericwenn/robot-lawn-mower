def can_move_forward(ultrasound, camera, gps):

  us_verdict = ultrasound.can_move_forward()
  cam_verdict = camera.can_move_forward()
  if us_verdict > 0 and us_verdict < 0.75 and cam_verdict < -.7:
    return False, (us_verdict, cam_verdict)

  return True, (us_verdict, cam_verdict)