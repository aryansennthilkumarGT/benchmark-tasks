"""One connected ordinary-tweezer collision envelope, not a calibrated product.
Handle center is the tool frame origin; axis+Z, 120mm origin-to-tip,142.5mm
end-to-end. This geometry is a rejection hypothesis, never a proven purchase.
"""
import numpy as np,fcl

def parts():
 return [('tweezer-handle',fcl.Box(.005,.0025,.045),np.array([0,0,0.])),
  ('tweezer-branch0',fcl.Box(.002,.001,.071),np.array([0,-.001,.058])),
  ('tweezer-branch1',fcl.Box(.002,.001,.071),np.array([0,.001,.058])),
  ('tweezer-tip0',fcl.Box(.001,.0005,.028),np.array([0,-.00075,.106])),
  ('tweezer-tip1',fcl.Box(.001,.0005,.028),np.array([0,.00075,.106]))]
