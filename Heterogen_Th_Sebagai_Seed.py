# Make directories
import os
import numpy as np
import shutil
import pandas as pd
from past.builtins import reduce, xrange; import operator

par_dir = np.arange(10, 18, 1)
paths = []
var_pm = np.arange(5,55,5)  
for i in par_dir:
    for var in var_pm:
        path1 = str(i) + '/DTC' + '/' + str(var)
        path2 = str(i) + '/MTC' + '/' + str(var)
        path3 = str(i) + '/VC'  + '/' + str(var)
        try :
            os.makedirs(path1)
            os.makedirs(path2)
            os.makedirs(path3)
        except FileExistsError :
            pass
        paths.append(path1)
        paths.append(path2)
        paths.append(path3)


def scale_write_standard(parameters):

    # Initialize default gap, cladding thickness
    gap = 0.009          # gap thickness in cm
    clad1_thick = 0.057  # cladding thickness in cm
    clad2_thick = 0.03   # cladding thickness in cm

    # Extract parameters
    # Get npin
    npin = int(parameters[0])
   
    # Get calculation type
    if parameters[1] == 1:
        calc_opt = "DTC"
        Tempf = round(parameters[2], 6)
        Tempm = 571
        rhom  = 0.72998
    elif parameters[1] == 2:
        calc_opt = "MTC"
        Tempf = 900
        Tempm = round(parameters[3], 6)
        rhom  = round(parameters[4], 6)
    elif parameters[1] == 3:
        calc_opt = "VC"
        Tempf = 900
        Tempm = 571
        rhom  = round(parameters[4], 6)
    # Calculate y value
    rho_U3Si2 = 11.468           # Density of U3Si2
    rho_Th3Si2 = 9.8             # Density of Th3Si2
    rho_UN = 13                  # Density of UN
    rho_ThN = 11.6               # Density of ThN
    var_pm = parameters[5]       # Mass percentage of ThN
    x = ((rho_U3Si2 * var_pm * 0.01)/(rho_Th3Si2 - rho_Th3Si2 * var_pm * 0.01))
    y = ((rho_UN * var_pm * 0.01)/(rho_ThN - rho_ThN * var_pm * 0.01))
    
    if npin == 10:
        pd      = 1.47    # pitch to diameter ratio
        pin_rad = 0.3962  # radius pin in cm
        fuel_type = 1 
        clad_type = 1 
        fuel_enr = 0.0634 # Uranium enrichment
        clad = clad1_thick 
        Th_rad = (np.sqrt(x/(x+1)) * pin_rad)  # radius Th in cm for each mass percentage of ThN
    elif npin == 11:
        pd      = 1.60    # pitch to diameter ratio
        pin_rad = 0.3707  # radius pin in cm
        fuel_type = 1 
        clad_type = 2 
        fuel_enr = 0.0679 # Uranium enrichment
        clad = clad2_thick
        Th_rad = (np.sqrt(x/(x+1)) * pin_rad)  # radius Th in cm for each mass percentage of ThN
    elif npin == 12:
        pd      = 1.81    # pitch to diameter ratio
        pin_rad = 0.3621  # radius pin in cm
        fuel_type = 2 
        clad_type = 2 
        fuel_enr = 0.0751 # Uranium enrichment
        clad = clad2_thick
        Th_rad = (np.sqrt(y/(y+1)) * pin_rad)  # radius Th in cm for each mass percentage of ThN
    elif npin == 13:
        pd      = 1.54    # pitch to diameter ratio
        pin_rad = 0.4948  # radius pin in cm
        fuel_type = 2 
        clad_type = 1 
        fuel_enr = 0.0668 # Uranium enrichment
        clad = clad1_thick
        Th_rad = (np.sqrt(y/(y+1)) * pin_rad)  # radius Th in cm for each mass percentage of ThN
    elif npin == 14:
        pd      = 1.41    # pitch to diameter ratio
        pin_rad = 0.5197  # radius pin in cm
        fuel_type = 1 
        clad_type = 1 
        fuel_enr = 0.0639 # Uranium enrichment
        clad = clad1_thick
        Th_rad = (np.sqrt(x/(x+1)) * pin_rad)  # radius Th in cm for each mass percentage of ThN
    elif npin == 15:
        pd      = 1.90    # pitch to diameter ratio
        pin_rad = 0.4168  # radius pin in cm
        fuel_type = 2 
        clad_type = 2 
        fuel_enr = 0.0717 # Uranium enrichment
        clad = clad2_thick
        Th_rad = (np.sqrt(y/(y+1)) * pin_rad)  # radius Th in cm for each mass percentage of ThN
    elif npin == 16:
        pd      = 1.62    # pitch to diameter ratio
        pin_rad = 0.4543  # radius pin in cm
        fuel_type = 1 
        clad_type = 2 
        fuel_enr = 0.0667 # Uranium enrichment
        clad = clad2_thick
        Th_rad = (np.sqrt(x/(x+1)) * pin_rad)  # radius Th in cm for each mass percentage of ThN
    elif npin == 17:
        pd      = 1.73    # pitch to diameter ratio
        pin_rad = 0.5073  # radius pin in cm
        fuel_type = 1 
        clad_type = 1 
        fuel_enr = 0.0654 # Uranium enrichment
        clad = clad1_thick
        Th_rad = (np.sqrt(x/(x+1)) * pin_rad)  # radius Th in cm for each mass percentage of ThN
    
    # Get fuel type
    if fuel_type == 1:
        fuel_opt = 'USi'
    elif fuel_type == 2:
        fuel_opt = 'UN'

    # Get cladding type
    if clad_type == 1:
        clad_opt = 'SiC'
    elif clad_type == 2:
        clad_opt = 'FeCrAl'

    # Open input file layout
    read_layout = open('layout-seed.inp', 'r')

    # Make new input file for every calculation
    if parameters[1] == 1:
        filename = str(npin) + '_' + str(Tempf) + '_' + str(calc_opt)  + '_' + str(var_pm) + "%" +  '.inp'
        write_inp = open(filename, 'w')
    elif parameters[1] == 2:
        filename = str(npin) + '_' + str(Tempm) + '_'+ str(rhom) + '_' + str(calc_opt)  + '_' + str(var_pm) + "%" +  '.inp'
        write_inp = open(filename, 'w')
    elif parameters[1] == 3:
        filename = str(npin) + '_' + str(rhom) + '_' + str(calc_opt)  + '_' + str(var_pm) + "%" +  '.inp'
        write_inp = open(filename, 'w')

    # Define fuel composition
    if fuel_opt == 'USi':
        comp_fuel = "comp c_usi   : WT Si=7.3 c_u=-100"
        mat_fuel = "mat  FUEL.1  : c_usi dens=11.468"
        comp_th = "comp c_th    : WT 90232=99.98 90230=-100\ncomp c_th3Si2   : FORM c_th=3 Si=2"
        mat_th = "mat  FUEL.2    : c_th3Si2 dens=9.8" #Preparation, Identification and Chemical Properties of the Thorium Silicides’” BY E. L. JACOBSON, ROBERT D. FREEMAN, A. C,. THARP AND .ALAN W. SEARCY’~ RECEIVED APRIL 2, 1956

    elif fuel_opt == 'UN': 
        comp_fuel = "comp c_un    : WT c_n=5.7 c_u=-100"
        mat_fuel = "mat  FUEL.1  : c_un dens=13"
        comp_th = "comp c_th    : WT 90232=99.98 90230=-100\ncomp c_thn   : FORM c_n=1 c_th=1"
        mat_th = "mat  FUEL.2    : c_thn dens=11.6"

    
    # Define fuel enrichment in %4
    fuel_enr = fuel_enr * 100

    # Define real gap thickness
    gap_real = gap + pin_rad

    # Define cladding composition
    if clad_opt == 'SiC':
        clad_thick = clad + gap_real
        comp_clad =  "comp sic     : WT Si=70.08 C=29.92"
        mat_clad = "mat  CLAD.1  : sic dens=2.58  temp=600"
        pin_F = ("pin F : "+str("%.4f" %Th_rad)+" "+str("%.4f" %pin_rad)+"    "+str("%.4f" %gap_real)+"  "+str("%.4f" %clad_thick))
    elif clad_opt == 'FeCrAl':
        clad_thick = clad + gap_real
        comp_clad = "comp fecral  : WT Fe=75 Cr=20 Al=5"
        mat_clad = "mat  CLAD.1  : fecral dens=7.1  temp=600"
        pin_F = ("pin F : "+str("%.4f" %Th_rad)+" "+str("%.4f" %pin_rad)+"    "+str("%.4f" %gap_real)+"  "+str("%.4f" %clad_thick))
    
    # Get pitch size from pin to diameter ratio
    pitch = clad_thick * pd * 2
    
    # change the type argument of temperature and the moderator for an overwrite newfile
    Temp_f = str(Tempf)
    Temp_m = str(Tempm)
    rho_m  = str(rhom)
    
    # Define fuel assembly layout
    nxn = (str("%.0f" % npin)+"x"+str("%.0f" % npin))

    # Define pin map and Water Rod position according to npin
    if npin == 10:
        pinmap = ' F F F F F \n F F F F F \n F F F F F \n F F F F F \n F F F F F'
    elif npin == 11:
        pinmap = ' F F F F F F \n F F F F F F \n F F F F F F \n F F F F F F \n F F F F F F \n F F F F F F'
    elif npin == 12:
        pinmap = " F F F F F F \n F F F F F F \n F F F F F F \n F F F F F F \n F F F F F F \n F F F F F F"
    elif npin == 13:
        pinmap = " F F F F F F F \n F F F F F F F \n F F F F F F F \n F F F F F F F \n F F F F F F F \n F F F F F F F \n F F F F F F F"
    elif npin == 14:
        pinmap = " F F F F F F F \n F F F F F F F \n F F F F F F F \n F F F F F F F \n F F F F F F F \n F F F F F F F \n F F F F F F F"
    elif npin == 15:
        pinmap = " F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F"
    elif npin == 16:
        pinmap = " F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F \n F F F F F F F F"
    elif npin == 17:
        pinmap = " F F F F F F F F F \n F F F F F F F F F \n F F F F F F F F F \n F F F F F F F F F \n F F F F F F F F F \n F F F F F F F F F \n F F F F F F F F F \n F F F F F F F F F \n F F F F F F F F F"

    # Define burnup power in W/g MHI with limit of 60000 MWd/kg MHI for 10 years
    power = 60000 / 3650

    # Replace lines in layout.inp with new parameters
    for line in read_layout:
        write_inp.write(line.replace('nn', nxn).replace('jp', "%.0f" %npin).replace('pp1', "%.2f" %pitch).replace('u235', "%.4f" %fuel_enr)
            .replace('c_usi1', comp_fuel).replace('matf', mat_fuel).replace('tempf', Temp_f).replace('comp_cl', comp_clad).replace('mat_cl', mat_clad)
            .replace('rhom', rho_m).replace('tempm', Temp_m).replace('pinF', pin_F).replace('pow_1', "%.4f" %power).replace('pmap', pinmap).replace('c_th', comp_th).replace('matth', mat_th))
    
    return filename

 

Npin = np.arange(10, 18, 1)
Tfuel = np.linspace(800, 1000, 5) # TF nominal = 900 K
Tmode = np.linspace(541, 601, 7) # Tmode nominal = 571 K
calculation = [1, 2, 3]

rho_l = 0.72998
rho_g = 0.044553
x = np.linspace(0, 0.01, 10)
rhoM_v = (1-x)*rho_l + x*rho_g

# To determine the density of water as the effect of temperature decrease, we use interpolate
df = pd.read_csv("Water_15_MPa-RJS.txt", sep="\t",header=None, skiprows=[0])  # read file
Temperature = list(df[0])   # set list of water Temperature from 300 to 580 with increment 10 K
Density = list(df[2])       # set list of water density at pressure = 15 MPa as the function Temperature
arr_temp = np.array(Temperature)
arr_dens = np.array(Density)
rhow = []

# define a function to find temperature and density value 
def find_Temp(array,T):
    index = np.where(array==T)[0][0] # Mencari indeks suhu yang ditentukan pada larik yang berisi kumpulan suhu
    return index 
for temp in Tmode:
    indeks = find_Temp(arr_temp, temp)
    rhow.append(arr_dens[indeks])


for calc in calculation:
    for Np in Npin:
        for var in var_pm:
            for Tf in Tfuel:
                if calc == 1:
                    calculate = "DTC"
                    target_folder = str(Np) + '/' + calculate + '/' + str(var)
                    param = [Np, calc, Tf, 0, 0, var]
                    shutil.move(scale_write_standard(param), target_folder)
            for i in range(len(Tmode)):
                if calc == 2:
                    calculate = "MTC"
                    target_folder = str(Np) + '/' + calculate + '/' + str(var)
                    param = [Np, calc, 0, Tmode[i], rhow[i], var]
                    shutil.move(scale_write_standard(param), target_folder)
            for rhom in rhoM_v:
                if calc == 3:
                    calculate = "VC"
                    target_folder = str(Np) + '/' + calculate + '/' + str(var)
                    param = [Np, calc, 0, 0, rhom, var]
                    shutil.move(scale_write_standard(param), target_folder)

# Searching .inp files in subdirectories
import glob
inp_paths = [glob.glob(path + '/*.inp') for path in paths]
inp_paths = [path for paths in inp_paths for path in paths]
inp_paths

# Running .inp files using python on bash : subprocess.run()
import subprocess

def run_scale(path):
    command = "nohup /usr/local/SCALE-6.2.4/bin/scalerte " + path +" > log.txt &"
    subprocess.run(command, shell=True)
    return 0

import psutil
import time

def cpu_is_free():
    for proc in psutil.process_iter():
        if proc.name() == 'scalerte':
            return False
    return True

# Running acording to the number of cpu
cpu_num = os.cpu_count()
loop_num = np.ceil(len(inp_paths) / cpu_num)

i = 0

while i < loop_num :
    if (i + 1) * cpu_num > len(inp_paths):
        for path in inp_paths[i * cpu_num : ]:
            print('Running ' + path)
            run_scale(path)
    else :
        for path in inp_paths[i * cpu_num : (i + 1) * cpu_num]:
            print('Running ' + path)
            run_scale(path)
    # Wait cpu is free for the next loop
    while not cpu_is_free():
        time.sleep(1)
    print('Loop '+str(i+1) +' is finished')
    i += 1