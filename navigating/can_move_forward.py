def can_move_forward(ultrasound, camera, gps):
  if ultrasound.freshness() < 0.2:
    return True, 0 # total uncertainty
  
  can_forward = ultrasound.verdict() == 1
  certainty = ultrasound.certainty()

  return can_forward