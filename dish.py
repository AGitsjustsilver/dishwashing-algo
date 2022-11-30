import random

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
        

    def clear(self) -> float:
        if self.isCleared is False:
            self.isCleared = True
            return (CLEAR_TIME * self.dish_mess)
        
        return 0.0

    def scrub(self) -> float:
        if self.isScrubed is False:
            self.isScrubed = True
            return (STAGE_TIME * self.dish_class)
        
        return 0.0

    def rinse(self) -> float:
        if self.isRinsed is False:
            self.isRinsed = True
            return (STAGE_TIME * self.dish_class)
        
        return 0.0

    def clean(self) -> float:
        return ( self.clear() + self.scrub() + self.rinse() )

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
        return self.dishes

    def __str__(self) -> str:
        for d in self.dishes:
            print(d)
        return ""

class Algorithms:

    def scrubAndRinse(a: list) -> float:
        time = 0.0
        for d in a:
            time += d.scrub() + d.rinse()
        return time

    def bucketSort(a: list) -> float:
        time = 0.0
        # create buckets
        bucket = dict()
        for category in dish_type:
            bucket[category] = list()
        # place dish in bucket
        for dish in a:
            time += dish.clear()
            bucket[dish.dish_class].append(dish)
            time += 0.75

        time += Algorithms.scrubAndRinse(a)

        return time

def main():
    SINK_SIZE = 100
    sink = Sink(SINK_SIZE)
    print(f"Bucket sort result time: {Algorithms.bucketSort(sink.dishArray())}")

if __name__ == "__main__":
    main()
