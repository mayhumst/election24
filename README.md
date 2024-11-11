# election24
Simplified presidential election simulator based on battleground state polling 

---

This is a very simplified version of an election simulator of the 2024 presidential election. This simulator takes the predicted vote percentages in 7 battleground states, using polling data from Siena College and the New York Times. Based on the predicted values and the margin of error, my simulator generates a normal distribution, randomly picks a value for the margin of error, and adjusts the vote results accordingly to determine the winner of each battleground state. Based on electoral college votes for each of these swing states (and assuming every other non-swing state votes exactly as predicted), calculate who won the election in this simulation. 

This code then runs 2500 simulations (can be adjusted) and prints the statistics of all simulation results. 

*This simulation is NOT an accurate simulation. It does not factor in any sociopolitical considerations, and relies purely on random math for seven of the fifty states. This was just for fun. 
