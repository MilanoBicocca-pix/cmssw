from RecoVertex.BeamSpotProducer.workflow.objects.PayloadObj import Payload


# https://github.com/MilanoBicocca-pix/cmssw/blob/CMSSW_7_4_X_master_dev/RecoVertex/BeamSpotProducer/python/workflow/objects/PayloadObj.py


# myp = Payload('result_BeamFit_Run272775.txt')
myp = Payload('result_BeamFit_Run272775_good.txt')

# write flat tree Ls by LS
myp.fillNtuple()

# plot
for i in ['X',
	  'Y',
          'Z',		  	
          'sigmaZ',	  	
          'dxdz',	  	
          'dydz',	  	
          'beamWidthX',   	
          'beamWidthY']:
    myp.plot(i, 0, 99999999999, savePdf = True) 	
               
               
               
               
               
					
