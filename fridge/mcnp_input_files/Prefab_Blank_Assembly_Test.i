Input deck created by FRIDGe
c *****************************Blank_Assembly_Test*****************************
c ************************Cell Cards for Assembly: 01A01*********************** 
100 100 0.06748 -100 u=100 imp:n=1 $Assembly: Blank Region
101 101 0.02428 -101 u=100 imp:n=1 $Assembly: Lower Coolant
102 102 0.02428 -102 u=100 imp:n=1 $Assembly: Upper Coolant
103 0 -103 fill=100 imp:n=1 $Assembly
104 0 103 imp:n=0 $Everything Else

c ********************Surface Cards for Fuel Assembly: 01A01*******************
100 RHP 0.0 0.0 -60.0 0 0 240 0 5.80529 0 $Assembly: Blank Region
101 RHP 0.0 0.0 -100.1 0 0 40.1 0 5.80529 0 $Assembly: Lower Coolant
102 RHP 0.0 0.0 180.0 0 0 40.0 0 5.80529 0 $Assembly: Upper Coolant
103 RHP 0.0 0.0 -100.0 0 0 320.0 0 5.805 0 $Assembly: Full Assembly Surface

c **********************************Data Cards*********************************
c ******************************k-code Information*****************************
kcode 10000000000 1.0 300 2300
ksrc 0 -12 40 
PRDMP 100 10 100 1 
kopts BLOCKSIZE=10 KINETICS=YES PRECURSOR=Yes 
DBCN 68J 50000 
c *****************************Material Information****************************
c Material: ['LiquidNa', 'HT9']; Density: 0.06748 atoms/bn*cm 
m100 11023.39c 1.0796E-1 6000.39c 8.1910E-3 14028.39c 6.4860E-3
     14029.39c 3.1813E-4 14030.39c 2.0297E-4 15031.39c 4.7643E-4
     16032.39c 2.9231E-4 16033.39c 2.2378E-6 16034.39c 1.2309E-5
     16036.39c 2.7353E-8 23050.39c 7.3863E-6 23051.39c 2.8895E-3
     24050.39c 4.9211E-3 24052.39c 9.1255E-2 24053.39c 1.0152E-2
     24054.39c 2.4803E-3 25055.39c 5.3722E-3 26054.39c 4.5281E-2
     26056.39c 6.8546E-1 26057.39c 1.5552E-2 26058.39c 2.0340E-3
     28058.39c 2.8900E-3 28060.39c 1.0762E-3 28061.39c 4.6017E-5
     28062.39c 1.4436E-4 28064.39c 3.5587E-5 42092.39c 7.7767E-4
     42094.39c 4.7930E-4 42095.39c 8.2099E-4 42096.39c 8.5501E-4
     42097.39c 4.8730E-4 42098.39c 1.2254E-3 42100.39c 4.8349E-4
     74180.39c 1.6401E-6 74182.39c 3.5822E-4 74183.39c 1.9238E-4
     74184.39c 4.0967E-4 74186.39c 3.7602E-4
c Material: Liquid Sodium; Density: 0.02428 atoms/bn*cm 
m101 11023.39c 1.0000E+0
c Material: Liquid Sodium; Density: 0.02428 atoms/bn*cm 
m102 11023.39c 1.0000E+0
c Material: Liquid Sodium; Density: 0.02428 atoms/bn*cm 
m103 11023.39c 1.0000E+0