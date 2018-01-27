###############################################################################################
# Agent-based Legislative Modeling Simulation
#
# Author: Joseph Stigall
#
# Description:
#   Legislators within a majority and minority party are generated and mapped onto
#   one-dimensional euclidean space. A spatial voting model is assumed with legislators'
#   ideal points (preferred policy outcomes) following a normal distribution at party means.
#   A member will vote in favor a bill if the proposed policy point is within an "error"
#   distance of their ideal point. A randomly selected legislator puts forth proposals
#   at the point nearest to the median ideal within their acceptable range, and repeats
#   this process until a bill is passed. Each time a vote is taken but the proposal does
#   not pass, the "error" range of each member is increased as a fatigue factor. Majority
#   party size, distance betweenparty medians, and intraparty heterogeneity are altered
#   to generate data across these variables and output to a .csv file. 
#
# Notes:
#   To reduce computational time, this script use multi-core processing to run the simulation
#   across different variables. Be sure to change the commented number in the 'parallelize'
#   function to match the number of processor cores the computer has in order to correctly
#   start the multiprocessing pool.
#
###############################################################################################

####################
# Prep
####################

# load packages
import random, timeit
import pandas as pd
import numpy as np
import parallel
from multiprocessing import Pool

# set seed for randomization
initial_seed = 0
random.seed(initial_seed)

####################
# Object Classes
####################

class Legis:
    """ Legislator Class: Legis(number, ideal, error, adj)
    Legislator object to propose and vote on bills.
    
    Init Parameters: 
        number- ID number
        ideal- ideal policy point
        error- maximum acceptable distance from ideal policy point
        adj- post-vote error increase
        
    Functions:
        vote(proposed)
        propose(proposal)
        find_proposal()
    """
    def __init__(self, number, ideal, error, adj):
        self.number = number
        self.ideal = ideal
        self.error = error
        self.adj = adj
        
    def vote(self, proposed):
        """ Votes on a submitted legislative proposal. Votes in favor if the proposal is
        within the range of the legislator's ideal point +/- error

        Parameters: proposed- proposed ideal point

        Returns: TRUE if vote in favor, FALSE if vote against
        """
        
        if (proposed >= self.ideal-self.error) and (proposed <= self.ideal+self.error):
            self.error = self.error + self.adj
            return True
        else:
            self.error = self.error + self.adj
            return False
         
    def propose(self, proposal):
        """ Proposes a vote to the legislature. Vote passes via simple majority.
        Parameters: proposal- proposal ideal point

        Returns: array [boolean of vote passage, ideal point, count of yea votes]
        """
        
        print("Proposing ideal point of:", proposal)
        yeas = 0
        
        for i in legis_list:
            if i.vote(proposal) == True: yeas += 1
            elif  i == self: yeas +=1
            
        if yeas > n_legis/2:
            # vote passes
            print("Proposal passed.  Yeas-", yeas, "Nays-", n_legis-yeas)
            return [True, proposal, yeas]
        else:
            # vote fails
            print("Proposal failed. Yeas-", yeas, "Nays-", n_legis-yeas)
            return [False, proposal, yeas]
        
    def find_proposal(self):
        """ Returns proposal point based on personal ideal point and acceptable range compared
        to the median ideal point.

        Returns: median ideal if point is within the legislator's error range OR closest point
            to the median ideal within the error range if otherwise.
        """

        global median_ideal
        
        if (median_ideal >= self.ideal-self.error) and (median_ideal <= self.ideal+self.error):
            # median ideal within acceptable range
            return median_ideal
        
        else:
            # median ideal outside acceptable range
            if median_ideal < self.ideal-self.error:
                return self.ideal-self.error
            else: 
                return self.ideal+self.error
            
class Party:
    """ Party Class: Party(size, mu, sigma, error, adj)
    Upon intialization, populates party with legislator objects with a standard distribution
    of ideal points based on init parameters. Adds members to the global legis_list array,
    and stores list of internal party members to the party_list array.
    
    Init Parameters:
        size- number of party members
        mu- mean ideal point across party
        sigma- standard deviation of ideal points across party
        error- error variable for generated legislator objects
        adj- adj variable for generated legislator objects  
    """
    
    def __init__(self, size, mu, sigma, error, adj):
        # set init variables
        self.size = size        
        self.mu = mu
        self.sigma = sigma
        self.error= error
        self.adj = adj
        
        self.party_list = []
        
        global legis_list, n_legis, n_seats

        # populate party
        for i in range(self.size):
            if (n_legis < n_seats):
                ideal = random.normalvariate(self.mu, self.sigma)
                if ideal > 1.0:
                    ideal = 1.0
                elif ideal < -1.0:
                    ideal = 0.0
                    
                member = Legis(i,ideal,self.error, self.adj)
                self.party_list.append(member)
                legis_list.append(member)
                n_legis += 1
            else:
                print("All seats are filled.")
                break
            
####################
# Global Functions
####################

def parallelize(f, sequence):
    """ Parallizes a function f to compute a sequence of numbers

    Parameters:
        f- function
        sequence- sequence to run f on
        
    Returns: sequence of result
    """
    
    # start multiprocessing pool
    pool = Pool(processes = parallel::detectCores())
    
    result = pool.map(f, sequence)
    
    # End Pool
    pool.close()
    pool.join()
    return result

def run_simulation(reps, maj_party_size, mu_distance, maj_sigma, maj_error, maj_adj,
                   min_sigma,min_error, min_adj):
    """ Runs a simulation

    Parameters: 
        reps- number of repetitions
        maj_party_size- majority party size 
        mu_distance- distance between party ideal point medians
        maj_sigma- minority st. dev.
        maj_error- minority error value
        maj_adj- minority post-vote adjustment
        min_sigma- minority st. dev.
        min_error- minority error value
        min_adj-minority post-vote adjustment
        
    Returns: PANDAS dataframe with columns [Initial Value, Final Value, Number of Votes, Yeas,
        Majority Party Size, Distance between Medians, Majority St. Dev., Majority Round Adjustment,
        Minority St. Dev., Minority Round Adjustment]
    """
    
    # create PANDAS dataframe
    df_sim= pd.DataFrame(0, index = np.arange(reps)+1, columns= ["Initial Value", "Final Value",
        "Number of Votes", "Yeas", "Majority Party Size", "Distance between Medians", "Majority St. Dev.",
        "Majority Round Adjustment", "Minority St. Dev.", "Minority Round Adjustment"])
    
    for i in range(reps):
        global legis_list, n_legis, median_ideal
        
        # clear intial parameters, randomize
        rep = i
        n_votes= 0
        n_legis= 0
        legis_list= []
        random.seed(initial_seed+rep)
        
        # generate parties
        majority = Party(maj_party_size, mu_distance/2, maj_sigma, maj_error, maj_adj)
        minority = Party(n_seats-maj_party_size, -mu_distance/2, min_sigma, min_error, min_adj)

        # sort Legislators by ideal points
        legis_list.sort(key= lambda x: x.ideal)
        median_ideal = legis_list[50].ideal
        
        # find proposer at random, find intital proposal point
        proposer = random.choice(legis_list)
        prop_ideal= proposer.ideal
        int_point = proposer.find_proposal()
        
        # run proposal
        print("Running Simulation. Proposer ideal point:", prop_ideal)
        while True:
            proposal_data = proposer.propose(proposer.find_proposal())
            n_votes+=1
            if proposal_data[0]== True:
                
                # clear error terms
                for i in majority.party_list:
                    i.error=maj_error
                for i in minority.party_list:
                    i.error=min_error
                
                # replace empty data in main dataframe
                df_sim.loc[rep+1]= int_point, proposal_data[1], n_votes, proposal_data[2], maj_party_size, \
                     mu_distance, maj_sigma, maj_adj, min_sigma, min_adj
                break
            
    # output data
    return df_sim

# simulation specific pass-through functions for easier parallelization
def party_size_sim(majority_party_size):
    return run_simulation(reps, majority_party_size, 1, 0.1, 0.02, 0.01, 0.1, 0.02, 0.01)
    
def distance_sim(mu_distance):
    return run_simulation(reps, 51, mu_distance, 0.1, 0.02, 0.01, 0.1, 0.02, 0.01)

def intraparty_sim(sigma):
    return run_simulation(reps, 51, 1, sigma, 0.02, 0.01, sigma, 0.02, 0.01)

####################
# Simulation
####################

# intial parameters
n_legis = 0 # number of legislators; begins at 0
n_seats = 101 # number of seats

legis_list = [] # empty array to be populated with an overall list of legislator objects

# number of repetitions
reps = 10000

# process timer; non-essential
print("Simulation Running...")
tic = timeit.default_timer()

# uncomment type of simulation needed
# default simulation
df_sim = run_simulation(reps, 51, 1, 0.1, 0.02, 0.01, 0.1, 0.02, 0.01)

# party size
#seq = np.arange(51,101,2)
#df_sim = parallelize(party_size_sim, seq) 

# distance between parties
#seq = np.arange(0.0,2.05,0.05)
#df_sim = parallelize(distance_sim, seq) 

# intraparty heterogeneity
#seq = np.arange(0.01,1,0.02)
#df_sim = parallelize(intraparty_sim, seq) 

# concatenate data (only needed for parallelized simulations)
#df_main= pd.concat(df_sim, ignore_index=True)
#df_main.index += 1

# output to csv, depending on type of simulation
df_main.to_csv("simulation_output/output.csv")
#df_main.to_csv("simulation_output/output_party_size.csv")
#df_main.to_csv("simulation_output/output_party_distance.csv")
#df_main.to_csv("simulation_output/output_intraparty.csv")

# end process timer 
toc = timeit.default_timer()
print("Simulation complete. Process took",toc-tic,"seconds.")

####################
# END
####################

