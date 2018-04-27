def can_move_forward(ultrasound, camera, gps):

  us_verdict = ultrasound.can_move_forward()
  cam_verdict = camera.can_move_forward()
  m = min([us_verdict, cam_verdict])
  return m >= 0, (us_verdict, cam_verdict)