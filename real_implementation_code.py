#Experiment Case B: Uniform Distribution

import random
import numpy as np
import math
import scipy.stats
import pandas as pd


def simulation(m, i, B, bit_pattern, times, mean, max):
    cb = i  # current buffer size
    current_time = 0
    next_packet_time = 0
    time_index = 0  # Keep track of which arrival times we've processed

    for bit in bit_pattern:
        # Generate delay based on bit value
        if bit == 0:
            delay = np.random.uniform(0, mean)
        else:
            delay = np.random.uniform(mean, max)
        
        next_packet_time = current_time + delay
        
        # Count arrivals between current_time and next_packet_time
        while time_index < len(times) and times[time_index] < next_packet_time:
            cb += 1
            time_index += 1
            
            # Check for overflow
            if cb > B:
                return "overflow"
        
        current_time = next_packet_time
        
        # Send packet
        cb -= 1
        
        # Check for underflow
        if cb < 0:
            return "underflow"
    

    return "success"  


def exponential_distribution(B, i, m):
    
    lamb = 1 # rate parameter; pkts/sec

    # Run simulations and collect results
    results = []
    num_trials = 500

    median = np.log(2)


    counts = {"underflow": 0, "overflow": 0, "success": 0}
    for _ in range(num_trials):
    # Step 1
        bit_pattern = [random.randint(0, 1) for i in range(m+1)]

        # Step 2
        worst_case_packets = 500
        
        times = np.random.exponential(scale=lamb, size=worst_case_packets)
        arrival_times = np.cumsum(times)
        arrival_times = arrival_times.tolist()
    
        outcome = simulation(m, i, B, bit_pattern, arrival_times, median, 5)
        counts[outcome] += 1

# Compute probabilities
    total = num_trials
    results.append([
        m, i, 
        counts["underflow"] / total, 
        counts["overflow"] / total, 
        counts["success"] / total
        ])

    # Convert results to DataFrame
    df = pd.DataFrame(results, columns=["M Size", "i", "Underflow", "Overflow", "Success"])
    df.insert(0, "Source Distribution", "Exponential")  # Add first column

    return df

def uniform_distribtuion(B, i, m):
    # Run simulations and collect results
    results = []
    num_trials = 500

    
    counts = {"underflow": 0, "overflow": 0, "success": 0}
    for _ in range(num_trials):
        # Step 1
        bit_pattern = [random.randint(0, 1) for i in range(m+1)]

        # Step 2
        worst_case_packets = 500
        
        times = np.random.uniform(0,1,size=worst_case_packets)
        mean = np.mean(times)
        arrival_times = np.cumsum(times)
        arrival_times = arrival_times.tolist()
    
        outcome = simulation(m, i, B, bit_pattern, arrival_times, mean, 1)
        counts[outcome] += 1

            # Compute probabilities
    total = num_trials
    results.append([
        m, i, 
        counts["underflow"] / total, 
        counts["overflow"] / total, 
        counts["success"] / total
    ])

    # Convert results to DataFrame
    df = pd.DataFrame(results, columns=["M Size", "i", "Underflow", "Overflow", "Success"])
    df.insert(0, "Source Distribution", "Uniform")  # Add first column

    return df



def main():

    B = 20

    distribution = input("Input the type of distribution, 'Uniform' or 'Exponential\n") 
    m_size = int(input("Input the size of the secret message (m)\n"))
    i_value = int(input("Input a starting buffer value (i)\n"))

    if(distribution == "Uniform"):
        df = uniform_distribtuion(B, i_value, m_size)
    elif(distribution == "Exponential"):
        df = exponential_distribution(B, i_value, m_size) 
    else:
        distribution = input("Input the type of distribution, 'Uniform' or 'Exponential")

    print(df)


main()
