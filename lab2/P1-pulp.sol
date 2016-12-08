Problem:    
Rows:       10
Columns:    13
Non-zeros:  39
Status:     OPTIMAL
Objective:  OBJ = 0.7237731791 (MINimum)

   No.   Row name   St   Activity     Lower bound   Upper bound    Marginal
------ ------------ -- ------------- ------------- ------------- -------------
     1 _C1          NS             1             1             =      0.152689 
     2 _C10         NL             0             0                    0.410127 
     3 _C2          NS             1             1             =      0.327789 
     4 _C3          NS             1             1             =      0.181465 
     5 _C4          NS             1             1             =     0.0618305 
     6 _C5          B         365.99                      505.67 
     7 _C6          B         364.55                      503.68 
     8 _C7          B         507.93                      701.78 
     9 _C8          NL             0             0                    0.295518 
    10 _C9          NL             0             0                    0.294355 

   No. Column name  St   Activity     Lower bound   Upper bound    Marginal
------ ------------ -- ------------- ------------- ------------- -------------
     1 z            B       0.723773             0             1 
     2 x_0_0        NL             0             0             1         < eps
     3 x_0_1        NL             0             0             1         < eps
     4 x_0_2        B              1             0             1 
     5 x_1_2        B       0.347483             0             1 
     6 x_2_2        B       0.166693             0             1 
     7 x_3_2        NL             0             0             1         < eps
     8 x_1_0        B       0.652517             0             1 
     9 x_1_1        NL             0             0             1         < eps
    10 x_2_0        NL             0             0             1         < eps
    11 x_2_1        B       0.833307             0             1 
    12 x_3_0        NL             0             0             1         < eps
    13 x_3_1        B              1             0             1 

Karush-Kuhn-Tucker optimality conditions:

KKT.PE: max.abs.err = 2.22e-16 on row 3
        max.rel.err = 9.07e-17 on row 10
        High quality

KKT.PB: max.abs.err = 0.00e+00 on row 0
        max.rel.err = 0.00e+00 on row 0
        High quality

KKT.DE: max.abs.err = 1.67e-16 on column 5
        max.rel.err = 1.01e-16 on column 5
        High quality

KKT.DB: max.abs.err = 0.00e+00 on row 0
        max.rel.err = 0.00e+00 on row 0
        High quality

End of output
