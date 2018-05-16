import PicoBorgRev
PBR = PicoBorgRev.PicoBorgRev()     # Create a new PicoBorg Reverse object
PBR.Init()                          # Set the board up (checks the board is connected)
PBR.ResetEpo()
PBR.MotorsOff()