from microqiskit import QuantumCircuit, simulate
import random
import numpy as np
import math

class bb84:
    #Based (heavily) off https://quantum-computing.ibm.com/jupyter/user/qiskit-textbook/content/ch-algorithms/quantum-key-distribution.ipynb
    #TODO - maybe seperate classes into bob and alice

    def __init__(self, n, e_t=0, e_m=0, p=0.1):
        #initialise class with number of qubits, error and loss rates and arrays to store future information
        self.n = n

        self.e_t = e_t #error in transmission - the probability that a qubit will flip will being carried
        self.e_m = e_m #error in measurement - the probability that a qubit will be measured incorrectly

        self.p = p #loss - the probability that a qubit won't make it to the other end 

        self.alice_bits = []
        self.alice_bases = []

        self.bob_bases = []
        self.bob_bits = []

        self.key = None


    def run_protocol(self, distance, user_input=False):
        """
        Different bases work as follows:

        In the z basis:

        0 => |0>
        1 => |1>

        In the x basis:

        0 => |+>  (= 1/root(2) |0> + |1>)
        1 => |->  (= 1/root(2) |0> - |1>)

        Measuring |+> or |-> in the z basis will give 0 with 0.5 probability and 1 with 0.5 probability

        Measuring |0> or |1> in the x basis will give 0 with 0.5 probability and ...
        """

        n_sent = 0
        n_received = 0

        while n_received < self.n:          #alice prepares random bits in random bases and sends them to bob
            qc = QuantumCircuit(1,1)
            alice_bit = random.choice("01") #she chooses a random value
            self.alice_bits.append(alice_bit) 
            alice_base = random.choice("zx") #and chooses a random base
            self.alice_bases.append(alice_base)
            if alice_base == "z": # Prepare qubit in Z-basis
                if alice_bit == "0":
                    pass #creates the |0> state
                else:
                    qc.x(0) #creates the |1> state
            else: # Prepare qubit in X-basis
                if alice_bit == "0":
                    qc.h(0) #creates the |+> state
                else:
                    qc.x(0)
                    qc.h(0) #creates the |-> state
            n_sent += 1
            print("sent:", n_sent)
            n_received += self.send(qc, loss=calc_loss(self.p, distance)) #attempts to send qubit to bob. The greater the distance 
            print("received:", n_received)                                          #between the two, the (exponentially) more likely the qubit will be lost
        self.n_received, self.n_sent = n_received, n_sent
        print("Alice: 'my bases were\t", self.alice_bases, "'") #alice publishes her bases
        print("Bob: 'my bases were\t", self.bob_bases, "'") #bob publishes his bases
        if not user_input:
          key_indexes = [x for x in range(len(self.alice_bases)) if self.alice_bases[x]==self.bob_bases[x]]
        else:
          key_indexes = input("What are the indexes of the ones that were the same?").split() #the user finds which were the same
        while any(self.alice_bases[int(i)] != self.bob_bases[int(i)] for i in key_indexes): #if they're wrong, make them do it again until they get it
            print("nope you're wrong")
            key_indexes = input("What are the indexes of the ones that were the same?").split() #the user finds which were the same

        #key = [self.alice_bases[i] for i in range(self.n) if str(i) in key_indexes]
        new_a_bits = [self.alice_bits[i] for i in range(self.n) if str(i) in key_indexes or i in key_indexes] #alice retains only the bits which are in the same basis as bob
        new_b_bits = [self.bob_bits[i] for i in range(self.n) if str(i) in key_indexes or i in key_indexes] #same^




        if user_input:
          k = int(input("how much of your key do you want to publish to check with Bob?")) #the user decides how much of the key to verify
        else:
          k = max(1, len(new_b_bits)//4)
        print("Alice: 'here are my first", k, " bits:\t", new_a_bits[:k], "'")
        print("Bob: 'ok, here are mine:\t", new_b_bits[:k]) #they each publish the first k of their bits

        if user_input and "y" not in input("do they match"):
            print("then we have failed")
        else:
            print("success! We shall use the rest of our bits as our secret key!!")
            key = "".join(new_a_bits[k:]) #a key has been formed    
            print("(key=", key, ")") 
        self.key = key


    def send(self, qc, loss=0.1):
        if random.random() < self.e_t: #flips the qubit with probability e_t
            qc.x(0)
            qc.z(0)
            print("qubit was contaminated")

        if random.random() > loss: #measures the qubit with probability 1 - loss
            self.b_measure(qc)
            return 1
        else:
            self.bob_bases.append(-1) #adds -1 to show qubit was not successful
            self.bob_bits.append(-1)
            return 0 # qubit didnt make the journey

    def b_measure(self, qc):
        bob_base = random.choice("zx") #bob picks a random basis to measure his qubit
        self.bob_bases.append(bob_base)
        if bob_base == 'x': qc.h(0) #coverts to x basis: H|+> = |0>, H|+> = |1> (and vice versa)
        qc.measure(0,0)
        counts = simulate(qc, shots=1)
        result = '1' in counts
        if random.random() < self.e_m: result = not(result) #does the wrong measurement with probability e_m
        self.bob_bits.append(int(result)) #stores the result

    def get_key(self):
        if len(self.key) == 0: return "error"
        return self.key

def calc_loss(p, distance):
    return min(p * math.exp((distance-1) * 0.5), 1)


