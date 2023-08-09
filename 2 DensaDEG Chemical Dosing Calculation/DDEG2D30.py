#!/usr/bin/env python
# coding: utf-8

# In[67]:


#read data
#import pandas as pd
#data=pd.read_excel("Calculationdata.xls")
#print(data)

import csv
with open('Calculationdata.csv') as csvfile:
    reader=csv.reader(csvfile)
    data=[]
    for row in reader:            
        data.append(row)           
    #打印
    print(data)

type(data[3][3])


# In[ ]:





# In[68]:


#inlet analysis
SSinlet=float(data[3][3])
SSoutlet=float(data[3][4])
SSremoved=SSinlet-SSoutlet

Cainlet=float(data[4][3])
Caoutlet=float(data[4][4])
Caremoved=Cainlet-Caoutlet

Mginlet=float(data[5][3])
Mgoutlet=float(data[5][4])
Mgremoved=Mginlet-Mgoutlet

Nainlet=float(data[6][3])
NH4inlet=float(data[7][3])
SO42inlet=float(data[8][3])
Clinlet=float(data[9][3])
HCO3inlet=float(data[10][3])
CO32inlet=float(data[10][3])

Totalcationinlet=Cainlet/40*2+Mginlet/24*2+Nainlet/23*1+NH4inlet/14*1
Totalanioninlet=SO42inlet/96*2+Clinlet/35.5*1+HCO3inlet/61*1+CO32inlet/60*2

Totalhardnessinlet=Cainlet/40+Mginlet/24
Cahardnessinlet=Cainlet/40
Mghardnessinlet=Mginlet/24

Totalalkalintyinlet=HCO3inlet/61*0.5+CO32inlet/60*1

print("总阳离子是：{:.1f} mmol/L;\n总阴离子是： {:.1f} mmol/L;".format(Totalcationinlet,Totalanioninlet))
print("总硬度是(CaCO3计)： {:.1f} mmol/L;\n钙硬度是(CaCO3计)： {:.1f} mmol/L;\n镁硬度是(CaCO3计)：{:.1f} mmol/L;".format(Totalhardnessinlet,Cahardnessinlet,Mghardnessinlet))
print("总碱度是(CaCO3计)： {:.1f} mmol/L;".format(Totalalkalintyinlet))


# In[69]:


# give a suggestion
if Cahardnessinlet >= Totalalkalintyinlet:
    print("钙硬大于等于碱度，建议采用烧碱-纯碱法除硬（NaOH+Na2CO3）!")
else:
    print("钙硬小于碱度，建议采用石灰-纯碱法除硬（Ca(OH)2+Na2CO3）!")


# In[70]:


#Coagualtion&flocculation
if (Cainlet-Caoutlet)/40*100+(Mginlet-Mgoutlet)/24*58+(SSinlet-SSoutlet) >= 300:
    TotalFeCl3dosing=50/162.5
    TotalPAMdosing=1.0
else:
    TotalFeCl3dosing=30/162.5
    TotalPAMdosing=0.5


# In[71]:


#NaOH-Na2CO3 treatment
def NaCO3NaOHmethod():

    if Mgoutlet < Mginlet: #######需要除镁硬     

        #Na2CO3 dosing
        Na2CO3dosingcal=Caremoved/40-HCO3inlet/61-CO32inlet/60
        Na2CO3dosingmargin=0 #######不考虑margin
                
        if Na2CO3dosingcal <= 0: ########碱度足够，不加Na2CO3
        
            #NaOH dosing
            NaOHforpH=3+HCO3inlet/61+NH4inlet/14
            NaOHforMg=Mgremoved/24*2
            NaOHforCoagulation=TotalFeCl3dosing*3
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))
            
            TotalNa2CO3dosing=0
            print("Na2CO3投加量是：{:.0f} mg/L".format(TotalNa2CO3dosing*106))    
            
            #H2SO4 dosing
            H2SO4dosingcal=(CO32inlet/60+HCO3inlet/61-Caremoved/40)*0.5
            H2SO4forNH4=NH4inlet/14*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4forNH4+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))

        else: ########碱度不足
            
            #NaOH dosing
            NaOHforpH=3+HCO3inlet/61+NH4inlet/14
            NaOHforMg=Mgremoved/24*2
            NaOHforCoagulation=TotalFeCl3dosing*3
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))           
            
            Na2CO3dosingmargin=0 #######不考虑margin
            TotalNa2CO3dosing=Na2CO3dosingcal+Na2CO3dosingmargin
            print("Na2CO3投加量是：{:.0f} mg/L".format(TotalNa2CO3dosing*106))

            #H2SO4 dosing
            H2SO4dosingcal=0
            H2SO4forNH4=NH4inlet/14*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4forNH4+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))
        

    else: #不考虑除镁硬
        
    
        Na2CO3dosingcal=Caremoved/40-HCO3inlet/61-CO32inlet/60
        Na2CO3dosingmargin=0 #######不考虑margin

        if Na2CO3dosingcal <= 0: ########碱度足够，不加Na2CO3
    
            #NaOH dosing
            NaOHforpH=NH4inlet/14 #######pH9就可以了
            NaOHforMg=0
            NaOHforCa=Caremoved/40
            NaOHforCoagulation=TotalFeCl3dosing*3
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCa+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))
            
            #Na2CO3 dosing
            TotalNa2CO3dosing=0 ########碱度足够
            print("Na2CO3投加量是：{:.0f} mg/L".format(TotalNa2CO3dosing*106))
        
            #H2SO4 dosing
            H2SO4dosingcal=0
            H2SO4forNH4=NH4inlet/14*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4forNH4+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))

        else: ########碱度不足

            #NaOH dosing
            NaOHforpH=NH4inlet/14 #######pH9就可以了
            NaOHforMg=0
            NaOHforCa=HCO3inlet/61
            NaOHforCoagulation=TotalFeCl3dosing*3
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCa+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))

            Na2CO3dosingmargin=0 #######不考虑margin
            TotalNa2CO3dosing=Na2CO3dosingcal+Na2CO3dosingmargin
            print("Na2CO3投加量是：{:.0f} mg/L".format(TotalNa2CO3dosing*106))

            #H2SO4 dosing
            H2SO4dosingcal=0
            H2SO4forNH4=NH4inlet/14*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4forNH4+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))

    print("FeCl3投加量是：{:.0f} mg/L".format(TotalFeCl3dosing*162.5))
    print("PAM投加量是：{:.1f} mg/L".format(TotalPAMdosing))


# In[72]:


#define Ca(OH)2+Na2CO3 treatmentmethod

def LimeNa2CO3mothod():

    ########  石灰加药量等于碳酸盐浓度/2
    LimeforCa=(HCO3inlet/61+CO32inlet/60)/2
    LimeforMg=Mgremoved/24
    LimeForpH=1.5
    Limeformargin=0 #######不考虑margin
    TotalLimedosing=LimeforCa+LimeforMg+LimeForpH+Limeformargin
    print("Ca(OH)2投加量是：{:.0f} mg/L".format(TotalLimedosing*74))     

                
    #Na2CO3 dosing
    Na2CO3forCa=(LimeforCa+Caremoved/40)-(HCO3inlet/61+CO32inlet/60)
    if Na2CO3forCa >= 0: #需要补充纯碱
        TotalNa2CO3dosing=Na2CO3forCa
        print("Na2CO3投加量是：{:.0f} mg/L".format(TotalNa2CO3dosing*106))
        #H2SO4 dosing
        H2SO4dosingcal=(NH4inlet/14)*0.5
        H2SO4dosingmargin=0 #######不考虑margin
        TotalH2SO4dosing=H2SO4dosingcal+H2SO4dosingmargin 
        print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))  
    
    else:
        TotalNa2CO3dosing=0 #不需要补充纯碱
        print("Na2CO3投加量是：{:.0f} mg/L".format(TotalNa2CO3dosing*106))    
        #H2SO4 dosing
        H2SO4dosingcal=(NH4inlet/14)*0.5+((HCO3inlet/61+CO32inlet/60)-(LimeforCa+Caremoved/40))*0.5
        H2SO4dosingmargin=0 #######不考虑margin
        TotalH2SO4dosing=H2SO4dosingcal+H2SO4dosingmargin 
        print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))  
 
    print("FeCl3投加量是：{:.0f} mg/L".format(TotalFeCl3dosing*162.5))
    print("PAM投加量是：{:.1f} mg/L".format(TotalPAMdosing))


# In[73]:


#define Ca(OH)2+NaOH+Na2CO3 treatmentmethod

def LimeNaOHNa2CO3mothod():

    ########  来水碱度大于硬度
    if Mgoutlet >= Mginlet: #######不需要除镁硬     
        if HCO3inlet/61 >= Cainlet/40*2: ###进水碱度大于硬度
            LimeforCa=Caremoved/40
            LimeForpH=NH4inlet/14+1.5+1.5
            Limeformargin=0 #######不考虑margin
            TotalLimedosing=LimeforCa+LimeForpH+Limeformargin
            print("Ca(OH)2投加量是：{:.0f} mg/L".format(TotalLimedosing*74))
            #H2SO4 dosing
            H2SO4dosingcal=(NH4inlet/14)*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))    

        elif HCO3inlet/61 >= Cainlet/40: ###进水碱度大于硬度的1/2
            LimeforCa=HCO3inlet/61-Cainlet/40
            LimeForpH=NH4inlet/14
            Limeformargin=0 #######不考虑margin
            TotalLimedosing=LimeforCa+LimeForpH+Limeformargin
            print("Ca(OH)2投加量是：{:.0f} mg/L".format(TotalLimedosing*74)) 
            
            #NaOH dosing
            NaOHforpH=0
            NaOHforMg=0
            NaOHforCa=Cainlet/40*2-HCO3inlet/61
            NaOHforCoagulation=0
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCa+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))

            #H2SO4 dosing
            H2SO4dosingcal=(NH4inlet/14)*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))              

        elif HCO3inlet/61 >= Cainlet/40*0.5:###进水碱度小于硬度的1/2，大于1/4
            LimeforCa=0
            LimeForpH=0
            Limeformargin=0 #######不考虑margin
            TotalLimedosing=LimeforCa+LimeForpH+Limeformargin
            print("Ca(OH)2投加量是：{:.0f} mg/L".format(TotalLimedosing*74)) 
            
            #NaOH dosing
            NaOHforpH=(NH4inlet/14)*0.5+3
            NaOHforMg=0
            NaOHforCa=Caremoved/40
            NaOHforCoagulation=3
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCa+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))

            #H2SO4 dosing
            H2SO4dosingcal=(NH4inlet/14)*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))              

        else:###进水碱度小于硬度的1/4
            LimeforCa=0
            LimeForpH=0
            Limeformargin=0 #######不考虑margin
            TotalLimedosing=LimeforCa+LimeForpH+Limeformargin
            print("Ca(OH)2投加量是：{:.0f} mg/L".format(TotalLimedosing*74)) 
            
            #NaOH dosing
            NaOHforpH=(NH4inlet/14)+3
            NaOHforMg=0
            NaOHforCa=HCO3inlet/61
            NaOHforCoagulation=3
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCa+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))

            #Na2CO3 dosing
            Na2CO3forCa=Caremoved-HCO3inlet/61
            TotalNa2CO3dosing=Na2CO3forCa
            print("Na2CO3投加量是：{:.0f} mg/L".format(TotalNa2CO3dosing*106))

            #H2SO4 dosing
            H2SO4dosingcal=(NH4inlet/14)*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))       

    else: #######需要除镁
        if HCO3inlet/61 >= Cainlet/40*2: ###进水碱度大于硬度
            LimeforCa=Cainlet/40
            LimeForpH=0
            Limeformargin=0 #######不考虑margin
            TotalLimedosing=LimeforCa+LimeForpH+Limeformargin
            print("Ca(OH)2投加量是：{:.0f} mg/L".format(TotalLimedosing*74))
            #NaOH dosing
            NaOHforpH=NH4inlet/14+1.5+HCO3inlet/61-Cainlet/40
            NaOHforMg=Mgremoved/24*2
            NaOHforCa=0
            NaOHforCoagulation=1.5
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCa+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))
            #H2SO4 dosing
            H2SO4dosingcal=(NH4inlet/14)*0.5+HCO3inlet/61/2-LimeforCa/74-Cainlet/40
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))    

        elif HCO3inlet/61 >= Cainlet/40: ###进水碱度大于硬度的1/2
            LimeforCa=HCO3inlet/61-Cainlet/40
            LimeForpH=0
            Limeformargin=0 #######不考虑margin
            TotalLimedosing=LimeforCa+LimeForpH+Limeformargin
            print("Ca(OH)2投加量是：{:.0f} mg/L".format(TotalLimedosing*74))             
            #NaOH dosing
            NaOHforCa=2*Cainlet/40-HCO3inlet/61
            NaOHforMg=0
            NaOHforpH=NH4inlet/14+1.5
            NaOHforCoagulation=0
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCa+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))

            #H2SO4 dosing
            H2SO4dosingcal=(NH4inlet/14)*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))  

        else:###进水碱度小于硬度的1/2
            LimeforCa=0
            LimeForpH=0
            Limeformargin=0 #######不考虑margin
            TotalLimedosing=LimeforCa+LimeForpH+Limeformargin
            print("Ca(OH)2投加量是：{:.0f} mg/L".format(TotalLimedosing*74)) 
            
            #NaOH dosing
            NaOHforpH=(NH4inlet/14)+3
            NaOHforMg=Mgremoved/24*2
            NaOHforCa=HCO3inlet/61
            NaOHforCoagulation=3
            NaOHformargin=0 #######不考虑margin
            TotalNaOHdosing=NaOHforpH+NaOHforMg+NaOHforCa+NaOHforCoagulation+NaOHformargin
            print("NaOH投加量是：{:.0f} mg/L".format(TotalNaOHdosing*40))

            #Na2CO3 dosing
            Na2CO3forCa=Caremoved-HCO3inlet/61
            if Na2CO3forCa >=0:
                TotalNa2CO3dosing=Na2CO3forCa
            else:
                TotalNa2CO3dosing=0
            print("Na2CO3投加量是：{:.0f} mg/L".format(TotalNa2CO3dosing*106))

            #H2SO4 dosing
            H2SO4dosingcal=(NH4inlet/14)*0.5
            H2SO4dosingmargin=0 #######不考虑margin
            TotalH2SO4dosing=H2SO4dosingcal+H2SO4dosingmargin 
            print("H2SO4投加量是：{:.0f} mg/L".format(TotalH2SO4dosing*98))              

 
    print("FeCl3投加量是：{:.0f} mg/L".format(TotalFeCl3dosing*162.5))
    print("PAM投加量是：{:.1f} mg/L".format(TotalPAMdosing))


# In[74]:


#decide to continue or break
print("采用烧碱纯碱法结果是：")
NaCO3NaOHmethod()

print("采用石灰纯碱法结果是：")
LimeNa2CO3mothod()

print("采用石灰烧碱纯碱法结果是：")
LimeNaOHNa2CO3mothod()

input('Press <Enter>')

