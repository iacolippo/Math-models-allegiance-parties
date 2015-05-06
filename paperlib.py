import random as rnd

#randomic takes population, density of population per squared kilometer and area of influence in squared kilometers
#and returns a coefficient of conversion per unit time

def randomic(pop, avg, area):

    deviation = float(rnd.randint(1,10))/100 #average deviation in elections
    
    rand_a = (avg*area/float(pop))*deviation
    return rand_a

# sum_vector takes a vector and return the sum of his elements

def sum_vector(vector, length):

	sum = 0
	
	for n in range(0, length):
		sum = sum + vector[n]
	
	return sum