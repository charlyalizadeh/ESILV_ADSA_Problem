from .GameSimulation import Game
import timeit

def benchmark(repeat = 1000):
    test_Array = "game.start()"
    setup_Array = "from GameSimulation import Game; game = Game('Array')"
    test_AVLTree = "game.start()"
    setup_AVLTree = "from GameSimulation import Game; game = Game('AVLTree')"
    time_Array = timeit.timeit(test_Array, setup = setup_Array, number = repeat) / repeat
    time_AVLTree = timeit.timeit(test_AVLTree, setup = setup_AVLTree, number = repeat) / repeat
    print("====RESULT====")
    print("Array mean time: {}".format(time_Array))
    print("AVLTree mean time: {}".format(time_AVLTree))

benchmark(10000)

