import matplotlib.pyplot as plt
class Energy_graph:
    def __init__(self, LEACH_object):
        self.LEACH_object=LEACH_object
    def plot_energy_graph(self):
        plt.clf()
        plt.xlim(left=0, right=self.LEACH_object.my_model.rmax)
        plt.ylim(bottom=0, top=self.LEACH_object.n * self.LEACH_object.my_model.Eo)
        plt.plot(self.LEACH_object.sum_energy_left_all_nodes)
        plt.title("Total residual energy ")
        plt.xlabel('Rounds')
        plt.ylabel('Energy (J)')
        plt.savefig("Graphs\Total residual energy.png")
        plt.clf()
        
class LifeTime_graph:
    def __init__(self, LEACH_object):
        self.LEACH_object=LEACH_object
    def plot_lifetime_graph(self):
        plt.clf()
        plt.xlim(left=0, right=self.LEACH_object.my_model.rmax)
        plt.ylim(bottom=0, top=self.LEACH_object.n)
        plt.plot(self.LEACH_object.alive_sensors)
        plt.title("Life time of sensor nodes")
        plt.xlabel('Rounds')
        plt.ylabel('No. of live nodes')
        plt.savefig("Graphs\Life time of sensor nodes.png")
        plt.clf()