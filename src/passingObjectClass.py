class passingObjectClass:
   number_of_system=7
   lowestWavelength=0
   highestWavelength=0
   iones=''
   data=[]
   filename=''
   ions_interest=[]

   def __init__(self, number_of_system, lowestWavelength, highestWavelength, iones, data, filename, ions_interest):
       self.number_of_system=number_of_system
       self.highestWavelength=highestWavelength
       self.data=data
       self.lowestWavelength=lowestWavelength
       self.iones=iones
       self.filename=filename
       self.ions_interest=ions_interest
