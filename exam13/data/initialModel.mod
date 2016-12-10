/*********************************************
 * OPL 12.4 Model
 * Author: oliveras
 * Creation Date: Jan 7, 2014 at 10:52:48 AM
 *********************************************/
 
 int bigM = ...;

 int userLocs = ...;
 int accessPoints = ...;
 
 range A = 1..accessPoints;
 range U = 1..userLocs;
 
 int f = ...; // fixed cost
 int c = ...; // additional cost
 int k = ...; // capacity
 int d = ...; // distance
 int cr[u in U] = ...; // capacity required by each user
 
 int posUsers[u in U][i in 1..2] = ...;
 int posAccessPoints[a in A][i in 1..2] = ...;

 // Decision variables (should be changed)
 dvar boolean x[a in A][u in U]; 
 

 // Objective function (should be changed)
 minimize sum(a in A, u in U) x[a][u];
 
 subject to {
 	
	// Example of constraint (should be changed)
 	forall (a in A)
 	  	sum(u in U) x[a][u] == 1;
 	  	
}
   
 execute {
   // Example of postprocessing (should be rewritten to output solution)
  	for (var u in U)
  		for (var a in A)
  			if (x[a][u] == 1) writeln("Access point " + a + " and user " + u + " are related"); 
 }    	  	  	  
 