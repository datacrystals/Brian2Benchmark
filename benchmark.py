import cpuinfo
import time


## GET MODE SELECT FROM USER ##

mode = int(input('Please Select the Benchmark Mode: [0: Fast, 1: Medium, 2: Extensive]: '))
memory_mode = int(input('Do you want to run the benchmark in low-memory mode [0: no, 1: yes]: '))

## OPEN BENCHMARK FILE FOR WRITING, AND ADD HEADER ##

Benchmark_Data = open('results.txt', 'w') # open the benchmark file for writing, so we can output our results

Benchmark_Data.write('----------------------------\n')
Benchmark_Data.write('----- Brian2 Benchmark -----\n')
Benchmark_Data.write('----------------------------\n\n')


## GET CPU INFO ##

Cpu_Info_Dictionary = cpuinfo.get_cpu_info()

Cpu_Name = Cpu_Info_Dictionary.get('brand_raw')
Cpu_Arch = Cpu_Info_Dictionary.get('arch')
Cpu_Bits = Cpu_Info_Dictionary.get('bits')
Cpu_Cores = Cpu_Info_Dictionary.get('count')
Cpu_Advertised_GHZ = Cpu_Info_Dictionary.get('hz_advertised_friendly')

Benchmark_Data.write(f'CPU Name: {Cpu_Name}\n')
Benchmark_Data.write(f'CPU Arhitecture: {Cpu_Arch}\n')
Benchmark_Data.write(f'CPU Bits: {Cpu_Bits}\n')
Benchmark_Data.write(f'CPU Cores: {Cpu_Cores}\n')
Benchmark_Data.write(f'CPU GHZ: {Cpu_Advertised_GHZ}\n\n')


## DEFINE BENCHMARK FUNCTIONS ##

def Dense_Bench(neurons=10, duration=100, runs = 10):

    t = time.time()

    eqs = '''
    dv/dt = (I-v)/tau : 1
    I : 1
    tau : second
    '''

    start_scope()

    N = neurons
    G = NeuronGroup(N, eqs)


    S = Synapses(G, G)
    S.connect(condition='i!=j', p=1)


    initalization = time.time() - t

    
    runtimes = []
    for r in range(runs):
        t = time.time()
        run(duration*ms)
        runtimes.append(time.time()-t)


    avg = (sum(runtimes) / len(runtimes))

    return initalization, runtimes, avg



## LIF DENSE CONNECTIVITY BENCHMARK ##

from brian2 import *


if mode == 0:
    durations = [10, 50, 100, 250, 1000, 5000]
elif mode == 1:
    durations = [10, 50, 100, 250, 1000, 5000, 10000, 50000]
elif mode == 2:
    durations = [10, 50, 100, 250, 1000, 5000, 10000, 50000, 100000, 500000]
else:
    print('Invalid Selection.')
    exit()


## EXECUTE BENCHMARK ##

for duration in durations:

    print(f'Benchmarking Duration {duration}ms')

    Benchmark_Data.write('--------------------------------------\n')
    Benchmark_Data.write(f'--10 Neuron Dense LIF, {duration}ms Runtime--\n')
    Benchmark_Data.write('--------------------------------------\n')
    for z in range(10): # benchmark with 10 neurons, for 100ms
        print(f'Benchmarking 10 Neurons, Round {z+1}')
        Result = Dense_Bench(neurons=10, duration=duration)
        Benchmark_Data.write(f'Init Took {Result[0]} Seconds | Run took an average of {Result[2]} Seconds | Full List: {Result[1]}\n')

    Benchmark_Data.write('---------------------------------------\n')
    Benchmark_Data.write(f'--100 Neuron Dense LIF, {duration}ms Runtime--\n')
    Benchmark_Data.write('---------------------------------------\n')
    for z in range(10): # benchmark with 100 neurons, for 100ms
        print(f'Benchmarking 100 Neurons, Round {z+1}')
        Result = Dense_Bench(neurons=100, duration=duration)
        Benchmark_Data.write(f'Init Took {Result[0]} Seconds | Run took an average of {Result[2]} Seconds | Full List: {Result[1]}\n')


    Benchmark_Data.write('----------------------------------------\n')
    Benchmark_Data.write(f'--1000 Neuron Dense LIF, {duration}ms Runtime--\n')
    Benchmark_Data.write('----------------------------------------\n')
    for z in range(10): # benchmark with 1000 neurons, for 100ms
        print(f'Benchmarking 1000 Neurons, Round {z+1}')
        Result = Dense_Bench(neurons=1000, duration=duration)
        Benchmark_Data.write(f'Init Took {Result[0]} Seconds | Run took an average of {Result[2]} Seconds | Full List: {Result[1]}\n')


    if not memory_mode:

        Benchmark_Data.write('-----------------------------------------\n')
        Benchmark_Data.write(f'--10000 Neuron Dense LIF, {duration}ms Runtime--\n')
        Benchmark_Data.write('-----------------------------------------\n')
        for z in range(10): # benchmark with 10000 neurons, for 100ms
            print(f'Benchmarking 10000 Neurons, Round {z+1}')
            Result = Dense_Bench(neurons=10000, duration=duration)
            Benchmark_Data.write(f'Init Took {Result[0]} Seconds | Run took an average of {Result[2]} Seconds | Full List: {Result[1]}\n')



## CLOSE FILE STREAM ##

Benchmark_Data.close()