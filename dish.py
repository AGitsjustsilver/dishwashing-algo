import random
import copy
import matplotlib.pyplot as plt

random.seed(8675309)
SINK_SIZE = 100
CLEAR_TIME = 5
STAGE_TIME = 15
dish_type = { 
    'utensil':  0.10 ,
    'cup':      0.20 ,
    'flat':     0.25 , 
    'bowl':     0.35 , 
    'pan':      1.00 , 
    'pot':      1.20
}
mess_type = {
    'light':    0.50 ,
    'moderate': 1.00 ,
    'heavy':    1.50 
}

class Dish:

    def __init__(self) -> None:
        # Assume all dishes are dirty
        self.isCleared = self.isScrubed = self.isRinsed = False
        self.isClean = (self.isCleared and self.isScrubed and self.isRinsed)

        # Assigning the kind of dish it is
        self.dish_class = random.choice(list(dish_type.keys()))
        self.dish_mess = random.choice(list(mess_type.keys()))
        self.clearTime = (CLEAR_TIME * mess_type[self.dish_mess])
        self.scrubTime = (STAGE_TIME * dish_type[self.dish_class])
        self.rinseTime = (STAGE_TIME * dish_type[self.dish_class])
        self.ttc = self.clearTime+self.scrubTime + self.rinseTime
        

    def clearDish(self) -> float:
        t = 0.0 if self.isCleared else self.clearTime
        self.isCleared = True
        return t

    def scrubDish(self) -> float:
        t = 0.0 if self.isScrubed else self.scrubTime
        self.isScrubed = True
        return t

    def rinseDish(self) -> float:
        t = 0.0 if self.isRinsed else self.rinseTime
        self.isRinsed = True
        return t

    def clean(self) -> float:
        t = (self.clearDish() + self.scrubDish() + self.rinseDish())
        self.is_clean()
        return t

    def is_clean(self) -> bool:
        self.isClean = (self.isCleared and self.isScrubed and self.isRinsed)
        return self.isClean

    def __str__(self) -> str:
        return f"a {self.dish_mess} mess {self.dish_class} has been made."

    def __iter__(self):
        return self

class Sink:

    def __init__(self, numDishes) -> None:
        self.n_dishes = numDishes
        self.dishes = []
        self.gen_dishes()

    def gen_dishes(self) -> None:
        for x in range(self.n_dishes):
            self.dishes.append(Dish())

    def dishArray(self) -> list():
        return copy.deepcopy(self.dishes)

    def __str__(self) -> str:
        for d in self.dishes:
            print(d)
        return ""

class Algorithms:

    def cleanInPlace(a: list('Dish')) -> float:
        time = 0.0
        for d in a:
            time += d.clean()
        return time

    def scrubAndRinse(a: list('Dish')) -> float:
        time = 0.0
        for d in a:
            time += d.scrubDish() + d.rinseDish()
        return time

    def bucketSort(a: list('Dish')) -> float:
        time = 0.0
        # create buckets
        bucket = dict()
        for category in dish_type:
            bucket[category] = list()
        # place dish in bucket
        for dish in a:
            time += dish.clearDish()
            bucket[dish.dish_class].append(dish)
            time +=  0.75

        time +=  Algorithms.scrubAndRinse(a)

        return time

    def insertionSort(a: list('Dish')) -> float:
        time = 0.0

        for i in range(1,len(a)):
            key = a[i].ttc
            j = i - 1
            time += a[i].clearDish()
            while j >= 0 and key < a[j].ttc:
                time += 0.5
                a[j+1] = a[j]
                j -= 1
            a[j+1] = a[i]
            time += 0.75

        time += Algorithms.scrubAndRinse(a)

        return time

    def __merge(a: list('Dish'), l, m, r) -> float:
        time = 0.0
        n1 = m - l + 1
        n2 = r - m
        L = [0] * n1
        R = [0] * n2
        for i in range(0, n1):
            L[i] = a[l + i]
        for i in range(0, n2):
            R[i] = a[m + i + 1]

        i, j, k = 0, 0, l
        while i < n1 and j < n2:
            time += a[k].clearDish()
            if L[i].ttc <= R[j].ttc:
                a[k] = L[i]
                i += 1
            else:
                a[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            time += a[k].clearDish()
            a[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            time += a[k].clearDish()
            a[k] = R[j]
            j += 1
            k += 1
        
        return time

    def mergeSort(a: list('Dish')) -> float:
        time = 0.0
        width = 1
        n = len(a)
        while width < n:
            l= 0
            while l < n:
                r = min(l+(width*2-1), n-1)
                m = min(l+width-1, n-1)
                time += Algorithms.__merge(a, l, m, r)
                l += width*2
            width *= 2

        time += Algorithms.scrubAndRinse(a)

        return time

    def __partition(a: list('Dish'), l, h):
        time = 0.0
        i = (l - 1)
        x = a[h].ttc

        for j in range(l, h):
            if a[j].ttc <= x:
                time += a[j].clearDish()
                i = i + 1
                a[i], a[j] = a[j], a[i]
                time += 0.25

        a[i + 1], a[h] = a[h], a[i + 1]
        time += 0.25
        return (i + 1), time

    def quickSort(a: list('Dish'), l, h) -> float: 
        time = 0.0
        if l < h:
            pi, t = Algorithms.__partition(a, l, h)
            time += t
            time += Algorithms.quickSort(a, l, pi-1)
            time += Algorithms.quickSort(a, pi+1, h)

        if len(a) is SINK_SIZE:
            time += Algorithms.scrubAndRinse(a)
        return time

    def selectionSort(a: list('Dish')) -> float:
        time = 0.0
        length = len(a)
        for i in range(length):
            time += a[i].clearDish()
            minimum = i
            for j in range(i+1, length):
                if a[minimum].ttc > a[j].ttc:
                    time += j/10
                    minimum = j
            a[i], a[minimum] = a[minimum], a[i]
            time += 0.25

        time += Algorithms.scrubAndRinse(a)

        return time


def algosGraphs(x, wip, bs, ins, ms, qs, sels):
    plt.scatter(x, ms    , label="Merge Sort"     , marker='D' )
    plt.scatter(x, wip   , label="Wash in Place"  , marker='*' )
    plt.scatter(x, bs    , label="Bucket Sort"    , marker='^' )
    plt.scatter(x, ins   , label="Insertion Sort" , marker='+' )
    plt.scatter(x, qs    , label="Quick Sort"     , marker='s' )
    plt.scatter(x, sels  , label="Selection Sort" , marker='o' )
    plt.plot(x, ms    , linestyle='--' )
    plt.plot(x, wip   , linestyle='--' )
    plt.plot(x, bs    , linestyle='--' )
    plt.plot(x, ins   , linestyle='--' )
    plt.plot(x, qs    , linestyle='--' )
    plt.plot(x, sels  , linestyle='--' )

    plt.xlabel('trial')        
    plt.ylabel('seconds')        
    plt.legend()
    plt.show()

def times(x, avg):
    plt.scatter(x, avg[3], label="Merge Sort"     , marker='D' )
    plt.scatter(x, avg[0], label="Wash in Place"  , marker='*' )
    plt.scatter(x, avg[1], label="Bucket Sort"    , marker='^' )
    plt.scatter(x, avg[2], label="Insertion Sort" , marker='+' )
    plt.scatter(x, avg[4], label="Quick Sort"     , marker='s' )
    plt.scatter(x, avg[5], label="Selection Sort" , marker='o' )
    plt.plot(x   , avg[3], linestyle='--' )
    plt.plot(x   , avg[0], linestyle='--' )
    plt.plot(x   , avg[1], linestyle='--' )
    plt.plot(x   , avg[2], linestyle='--' )
    plt.plot(x   , avg[4], linestyle='--' )
    plt.plot(x   , avg[5], linestyle='--' )

    plt.xlabel('trial')
    plt.ylabel('seconds')
    plt.legend()
    plt.show()
    
def main():
    NUM_TRIALS = 100
    algTimes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    algAvgs = [[0.0]*NUM_TRIALS, [0.0]*NUM_TRIALS, [0.0]*NUM_TRIALS,[0.0]*NUM_TRIALS, [0.0]*NUM_TRIALS, [0.0]*NUM_TRIALS] 
    x = [0] * NUM_TRIALS
    wip = [0] * NUM_TRIALS
    bs = [0] * NUM_TRIALS
    ins = [0] * NUM_TRIALS
    ms = [0] * NUM_TRIALS
    qs = [0] * NUM_TRIALS
    sels = [0] * NUM_TRIALS
    for trial in range(NUM_TRIALS):
        sink = Sink(SINK_SIZE) 
        x[trial] = trial
        wip[trial] = Algorithms.cleanInPlace(sink.dishArray())
        bs[trial] = Algorithms.bucketSort(sink.dishArray())
        ins[trial] = Algorithms.insertionSort(sink.dishArray())
        ms[trial] = Algorithms.mergeSort(sink.dishArray())
        qs[trial] = Algorithms.quickSort(sink.dishArray(), 0, SINK_SIZE-1)
        sels[trial] = Algorithms.selectionSort(sink.dishArray())
        algTimes[0] += wip[trial]
        algTimes[1] += bs[trial]
        algTimes[2] += ins[trial]
        algTimes[3] += ms[trial]
        algTimes[4] += qs[trial]
        algTimes[5] += sels[trial]
        algAvgs[0][trial] = algTimes[0]/(trial+1)
        algAvgs[1][trial] = algTimes[1]/(trial+1)
        algAvgs[2][trial] = algTimes[2]/(trial+1)
        algAvgs[3][trial] = algTimes[3]/(trial+1)
        algAvgs[4][trial] = algTimes[4]/(trial+1)
        algAvgs[5][trial] = algTimes[5]/(trial+1)

    print(f"Time (in seconds) averages based on {NUM_TRIALS} trials:")
    print(f"Clean in place result time: {algTimes[0]/NUM_TRIALS:.2f}. Minutes: {algTimes[0]/60/NUM_TRIALS:.2f}")
    print(f"Bucket sort result time: {algTimes[1]/NUM_TRIALS:.2f}. Minutes: {algTimes[1]/60/NUM_TRIALS:.2f}")
    print(f"Insertion sort result time: {algTimes[2]/NUM_TRIALS:.2f}. Minutes: {algTimes[2]/60/NUM_TRIALS:.2f}")
    print(f"Merge sort result time: {algTimes[3]/NUM_TRIALS:.2f}. Minutes: {algTimes[3]/60/NUM_TRIALS:.2f}")
    print(f"Quick sort result time: {algTimes[4]/NUM_TRIALS:.2f}. Minutes: {algTimes[4]/60/NUM_TRIALS:.2f}")
    print(f"Selection sort result time: {algTimes[5]/NUM_TRIALS:.2f}. Minutes: {algTimes[5]/60/NUM_TRIALS:.2f}")

    algosGraphs(x, wip, bs, ins, ms, qs, sels)
    times(x, algAvgs)
    

if __name__ == "__main__":
    print()
    main()
    print()
