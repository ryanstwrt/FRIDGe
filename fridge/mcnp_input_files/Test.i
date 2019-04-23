Input deck created by FRIDGe
c ******************************A271_Assembly_Test*****************************
c ************************Cell Cards for Assembly: 01A01*********************** 
100 100 0.04575 -100 u=101 imp:n=1 $Pin: Fuel
101 101 0.02428 100 -101 u=101 imp:n=1 $Pin: Bond
102 102 0.08599 101 -102 u=101 imp:n=1 $Pin: Clad
103 103 0.02929 102 u=101 imp:n=1 $Pin: Wirewrap + Coolant
104 104 0.02428 -103 u=102 imp:n=1 $Pin: Blank Pin Coolant
105 0 -104 lat=2 u=103 imp:n=1
     fill=-10:10 -10:10 0:0
      102 102 102 102 102 102 102 102 102 102
      102 102 102 102 102 102 102 102 102 102
      102 102 102 102 102 102 102 102 102 102
      102 101 101 101 101 101 101 101 101 101
      101 102 102 102 102 102 102 102 102 102
      102 101 101 101 101 101 101 101 101 101
      101 101 102 102 102 102 102 102 102 102
      102 101 101 101 101 101 101 101 101 101
      101 101 101 102 102 102 102 102 102 102
      102 101 101 101 101 101 101 101 101 101
      101 101 101 101 102 102 102 102 102 102
      102 101 101 101 101 101 101 101 101 101
      101 101 101 101 101 102 102 102 102 102
      102 101 101 101 101 101 101 101 101 101
      101 101 101 101 101 101 102 102 102 102
      102 101 101 101 101 101 101 101 101 101
      101 101 101 101 101 101 101 102 102 102
      102 101 101 101 101 101 101 101 101 101
      101 101 101 101 101 101 101 101 102 102
      102 101 101 101 101 101 101 101 101 101
      101 101 101 101 101 101 101 101 101 102
      102 101 101 101 101 101 101 101 101 101
      101 101 101 101 101 101 101 101 101 101
      102 102 101 101 101 101 101 101 101 101
      101 101 101 101 101 101 101 101 101 101
      102 102 102 101 101 101 101 101 101 101
      101 101 101 101 101 101 101 101 101 101
      102 102 102 102 101 101 101 101 101 101
      101 101 101 101 101 101 101 101 101 101
      102 102 102 102 102 101 101 101 101 101
      101 101 101 101 101 101 101 101 101 101
      102 102 102 102 102 102 101 101 101 101
      101 101 101 101 101 101 101 101 101 101
      102 102 102 102 102 102 102 101 101 101
      101 101 101 101 101 101 101 101 101 101
      102 102 102 102 102 102 102 102 101 101
      101 101 101 101 101 101 101 101 101 101
      102 102 102 102 102 102 102 102 102 101
      101 101 101 101 101 101 101 101 101 101
      102 102 102 102 102 102 102 102 102 102
      101 101 101 101 101 101 101 101 101 101
      102 102 102 102 102 102 102 102 102 102
      102 102 102 102 102 102 102 102 102 102
      102 102 102 102 102 102 102 102 102 102
      102
106 0 -106 u=100 fill=103 imp:n=1 $Assembly: Inner Portion of Assembly
107 107 0.03364 -107 u=100 imp:n=1 $Assembly: Plenum
108 108 0.07365 -108 u=100 imp:n=1 $Assembly: Upper Reflector
109 109 0.07365 -109 u=100 imp:n=1 $Assembly: Lower Reflector
110 110 0.08599  106 109 108 107 -110 u=100 imp:n=1 $Assembly: Assembly Duct
111 111 0.02428 -111 u=100 imp:n=1 $Assembly: Lower Coolant
112 112 0.02428 -112 u=100 imp:n=1 $Assembly: Upper Coolant
113 0 -113 fill=100 imp:n=1 $Assembly
114 0 113 imp:n=0 $Everything Else

c ********************Surface Cards for Fuel Assembly: 01A01*******************
100 RCC 0.0 0.0 0.0 0 0 60.0 0.19745 $Pin: Fuel
101 RCC 0.0 0.0 0.0 0 0 60.6 0.228 $Pin: Bond - 1% higher than fuel
102 RCC 0.0 0.0 0.0 0 0 60.6 0.265 $Pin: Clad - 1% higher than fuel
103 RHP 0.0 0.0 0.0 0 0 60.6 0.66144 0 0 $Pin: Coolant - 1% higher than fuel
104 RHP 0.0 0.0 0.0 0 0 60.6 0.33072 0 0 $Pin: Blank Pin - 1% higher than fuel
106 RHP 0.0 0.0 0.0 0 0 60.6 0 5.505 0 $Assembly: Duct Inner Surface
107 RHP 0.0 0.0 60.6 0 0 60.0 0 5.505 0 $Assembly: Plenum
108 RHP 0.0 0.0 120.6 0 0 60.0 0 5.505 0 $Assembly: Upper Reflector
109 RHP 0.0 0.0 -60.0 0 0 60.0 0 5.505 0 $Assembly: Lower Reflector
110 RHP 0.0 0.0 -60.0 0 0 240.6 0 5.80529 0 $Assembly: Duct Outer Surface
111 RHP 0.0 0.0 -99.8 0 0 39.8 0 5.80529 0 $Assembly: Lower Coolant
112 RHP 0.0 0.0 180.6 0 0 39.7 0 5.80529 0 $Assembly: Upper Coolant
113 RHP 0.0 0.0 -99.7 0 0 320.0 0 5.805 0 $Assembly: Full Assembly Surface

c **********************************Data Cards*********************************
c ******************************k-code Information*****************************
kcode 10000000000 1.0 300 2300
ksrc 0 0 80 
PRDMP 100 10 100 1 
kopts BLOCKSIZE=10 KINETICS=YES PRECURSOR=Yes 
c *****************************Material Information****************************
c Material: 5Pu22U10Zr; Density: 0.04575 atoms/bn*cm 
m100 92235.39c 1.9146E-1 92238.39c 5.4143E-1 94239.39c 4.0222E-2
     94240.39c 2.5566E-3 40090.39c 1.1707E-1 40091.39c 2.5250E-2
     40092.39c 3.8175E-2 40094.39c 3.7862E-2 40096.39c 5.9725E-3
c Material: Liquid Sodium; Density: 0.02428 atoms/bn*cm 
m101 11023.39c 1.0000E+0
c Material: HT9; Density: 0.08599 atoms/bn*cm 
m102 6000.39c 9.1823E-3 14028.39c 7.2709E-3 14029.39c 3.5663E-4
     14030.39c 2.2753E-4 15031.39c 5.3409E-4 16032.39c 3.2768E-4
     16033.39c 2.5087E-6 16034.39c 1.3799E-5 16036.39c 3.0663E-8
     23050.39c 8.2802E-6 23051.39c 3.2392E-3 24050.39c 5.5167E-3
     24052.39c 1.0230E-1 24053.39c 1.1381E-2 24054.39c 2.7805E-3
     25055.39c 6.0224E-3 26054.39c 5.0761E-2 26056.39c 7.6841E-1
     26057.39c 1.7434E-2 26058.39c 2.2802E-3 28058.39c 3.2398E-3
     28060.39c 1.2064E-3 28061.39c 5.1586E-5 28062.39c 1.6184E-4
     28064.39c 3.9894E-5 42092.39c 8.7178E-4 42094.39c 5.3731E-4
     42095.39c 9.2035E-4 42096.39c 9.5849E-4 42097.39c 5.4627E-4
     42098.39c 1.3737E-3 42100.39c 5.4201E-4 74180.39c 1.8386E-6
     74182.39c 4.0157E-4 74183.39c 2.1566E-4 74184.39c 4.5925E-4
     74186.39c 4.2153E-4
c Material: ['HT9', 'LiquidNa']; Density: 0.02929 atoms/bn*cm 
m103 6000.39c 2.1883E-3 14028.39c 1.7328E-3 14029.39c 8.4991E-5
     14030.39c 5.4226E-5 15031.39c 1.2728E-4 16032.39c 7.8093E-5
     16033.39c 5.9786E-7 16034.39c 3.2885E-6 16036.39c 7.3076E-9
     23050.39c 1.9733E-6 23051.39c 7.7195E-4 24050.39c 1.3147E-3
     24052.39c 2.4380E-2 24053.39c 2.7122E-3 24054.39c 6.6264E-4
     25055.39c 1.4352E-3 26054.39c 1.2097E-2 26056.39c 1.8313E-1
     26057.39c 4.1549E-3 26058.39c 5.4342E-4 28058.39c 7.7210E-4
     28060.39c 2.8751E-4 28061.39c 1.2294E-5 28062.39c 3.8569E-5
     28064.39c 9.5076E-6 42092.39c 2.0776E-4 42094.39c 1.2805E-4
     42095.39c 2.1934E-4 42096.39c 2.2843E-4 42097.39c 1.3019E-4
     42098.39c 3.2738E-4 42100.39c 1.2917E-4 74180.39c 4.3818E-7
     74182.39c 9.5701E-5 74183.39c 5.1396E-5 74184.39c 1.0945E-4
     74186.39c 1.0046E-4 11023.39c 7.6168E-1
c Material: Liquid Sodium; Density: 0.02428 atoms/bn*cm 
m104 11023.39c 1.0000E+0
c Material: ['LiquidNa', 'Void', 'HT9']; Density: 0.03364 atoms/bn*cm 
m107 11023.39c 3.6093E-1 6000.39c 5.8682E-3 14028.39c 4.6466E-3
     14029.39c 2.2791E-4 14030.39c 1.4541E-4 15031.39c 3.4132E-4
     16032.39c 2.0941E-4 16033.39c 1.6032E-6 16034.39c 8.8184E-6
     16036.39c 1.9596E-8 23050.39c 5.2916E-6 23051.39c 2.0701E-3
     24050.39c 3.5255E-3 24052.39c 6.5376E-2 24053.39c 7.2731E-3
     24054.39c 1.7769E-3 25055.39c 3.8487E-3 26054.39c 3.2440E-2
     26056.39c 4.9107E-1 26057.39c 1.1142E-2 26058.39c 1.4572E-3
     28058.39c 2.0705E-3 28060.39c 7.7098E-4 28061.39c 3.2967E-5
     28062.39c 1.0342E-4 28064.39c 2.5495E-5 42092.39c 5.5713E-4
     42094.39c 3.4338E-4 42095.39c 5.8817E-4 42096.39c 6.1254E-4
     42097.39c 3.4911E-4 42098.39c 8.7790E-4 42100.39c 3.4638E-4
     74180.39c 1.1750E-6 74182.39c 2.5663E-4 74183.39c 1.3782E-4
     74184.39c 2.9349E-4 74186.39c 2.6939E-4
c Material: ['LiquidNa', 'HT9']; Density: 0.07365 atoms/bn*cm 
m108 11023.39c 6.5941E-2 6000.39c 8.5768E-3 14028.39c 6.7915E-3
     14029.39c 3.3311E-4 14030.39c 2.1253E-4 15031.39c 4.9887E-4
     16032.39c 3.0607E-4 16033.39c 2.3432E-6 16034.39c 1.2889E-5
     16036.39c 2.8641E-8 23050.39c 7.7342E-6 23051.39c 3.0256E-3
     24050.39c 5.1529E-3 24052.39c 9.5553E-2 24053.39c 1.0630E-2
     24054.39c 2.5971E-3 25055.39c 5.6253E-3 26054.39c 4.7414E-2
     26056.39c 7.1774E-1 26057.39c 1.6285E-2 26058.39c 2.1298E-3
     28058.39c 3.0262E-3 28060.39c 1.1269E-3 28061.39c 4.8184E-5
     28062.39c 1.5116E-4 28064.39c 3.7264E-5 42092.39c 8.1430E-4
     42094.39c 5.0188E-4 42095.39c 8.5966E-4 42096.39c 8.9528E-4
     42097.39c 5.1025E-4 42098.39c 1.2831E-3 42100.39c 5.0626E-4
     74180.39c 1.7174E-6 74182.39c 3.7509E-4 74183.39c 2.0144E-4
     74184.39c 4.2896E-4 74186.39c 3.9374E-4
c Material: ['LiquidNa', 'HT9']; Density: 0.07365 atoms/bn*cm 
m109 11023.39c 6.5941E-2 6000.39c 8.5768E-3 14028.39c 6.7915E-3
     14029.39c 3.3311E-4 14030.39c 2.1253E-4 15031.39c 4.9887E-4
     16032.39c 3.0607E-4 16033.39c 2.3432E-6 16034.39c 1.2889E-5
     16036.39c 2.8641E-8 23050.39c 7.7342E-6 23051.39c 3.0256E-3
     24050.39c 5.1529E-3 24052.39c 9.5553E-2 24053.39c 1.0630E-2
     24054.39c 2.5971E-3 25055.39c 5.6253E-3 26054.39c 4.7414E-2
     26056.39c 7.1774E-1 26057.39c 1.6285E-2 26058.39c 2.1298E-3
     28058.39c 3.0262E-3 28060.39c 1.1269E-3 28061.39c 4.8184E-5
     28062.39c 1.5116E-4 28064.39c 3.7264E-5 42092.39c 8.1430E-4
     42094.39c 5.0188E-4 42095.39c 8.5966E-4 42096.39c 8.9528E-4
     42097.39c 5.1025E-4 42098.39c 1.2831E-3 42100.39c 5.0626E-4
     74180.39c 1.7174E-6 74182.39c 3.7509E-4 74183.39c 2.0144E-4
     74184.39c 4.2896E-4 74186.39c 3.9374E-4
c Material: HT9; Density: 0.08599 atoms/bn*cm 
m110 6000.39c 9.1823E-3 14028.39c 7.2709E-3 14029.39c 3.5663E-4
     14030.39c 2.2753E-4 15031.39c 5.3409E-4 16032.39c 3.2768E-4
     16033.39c 2.5087E-6 16034.39c 1.3799E-5 16036.39c 3.0663E-8
     23050.39c 8.2802E-6 23051.39c 3.2392E-3 24050.39c 5.5167E-3
     24052.39c 1.0230E-1 24053.39c 1.1381E-2 24054.39c 2.7805E-3
     25055.39c 6.0224E-3 26054.39c 5.0761E-2 26056.39c 7.6841E-1
     26057.39c 1.7434E-2 26058.39c 2.2802E-3 28058.39c 3.2398E-3
     28060.39c 1.2064E-3 28061.39c 5.1586E-5 28062.39c 1.6184E-4
     28064.39c 3.9894E-5 42092.39c 8.7178E-4 42094.39c 5.3731E-4
     42095.39c 9.2035E-4 42096.39c 9.5849E-4 42097.39c 5.4627E-4
     42098.39c 1.3737E-3 42100.39c 5.4201E-4 74180.39c 1.8386E-6
     74182.39c 4.0157E-4 74183.39c 2.1566E-4 74184.39c 4.5925E-4
     74186.39c 4.2153E-4
c Material: Liquid Sodium; Density: 0.02428 atoms/bn*cm 
m111 11023.39c 1.0000E+0
c Material: Liquid Sodium; Density: 0.02428 atoms/bn*cm 
m112 11023.39c 1.0000E+0