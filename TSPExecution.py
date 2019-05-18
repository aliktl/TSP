from TravelingSalesmanProblem import *

#data_mode = 'Random'
data_mode = 'Load'
csvfile = "TSP1.csv"
height = 500
width = 700
cities = 15
mutationFactor = 0.5
time = 180

tsp = TravelingSalesmanProblem(data_mode,csvfile,cities,height, width, time)
print("start of routes, utility ...")

routes, utility, distance, elapsedTime = tsp.performEvolution(100, 70, 100, mutationFactor)

currentCity = 0
route = ''
for itr in range(len(routes.keys())):
    # print("start of for itr in range of TSP Execution", itr)
    route = route + '->' + str(currentCity)
    # print("route" + route + " = route + '->' + str(currentCity)" + str(currentCity))
    currentCity = routes[currentCity]
    # print("currentCity " + str(currentCity))
print ("===== 20130841, Ali Mazlumov =====")
print ("Routes : %s" %(route))
print ("Distance : ", distance)
print ("Elapsed time : ", elapsedTime, "secs")
