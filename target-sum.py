from typing import List, Dict, Callable, Union, Tuple
import random
import time

def target_sum_slow(lst: List[int], target: int) -> Tuple[int]:
    """
    Given a list of integers and a target number, find whether there are two numbers in the list which
    add up to the given target number and return their indices. 
    Proposed time complexity: O(n^2).

    :param lst: list of integers
    :param target: target number to which two numbers in the list should add up to
    :return: Two integer tuple with indices of the numbers which sum to target. Smaller index first.
    """
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] + lst[j] == target:
                return i,j

def target_sum_fast(lst: List[int], target: int) -> Tuple[int]:
    """
    Given a list of integers and a target number, find whether there are two numbers in the list which
    add up to the given target number and return their indices. 
    Proposed time complexity: O(n).

    :param lst: list of integers
    :param target: target number to which two numbers in the list should add up to
    :return: Two integer tuple with indices of the numbers which sum to target. Smaller index first.
    """
    lst_dict = {}
    # Put all numbers in list and their indices into dict
    for index, value in enumerate(lst):
        lst_dict[value] = index
    mid = target // 2
    # Loop over all numbers from 0 up to target / 2. The idea is to check the dict for all
    # possible combinations of numbers which add up to target. For example if target is 7,
    # we will check whether 0 and 7 are in the list on the first iteration, then 6 and 1 on the 
    # second iteration, then 5 and 2 and so on.
    for i in range(mid + 1):
        small = i
        big = target - i
        small_index = lst_dict.get(small)
        big_index = lst_dict.get(big)
        if small_index is not None and big_index is not None:
            if small_index > big_index:
                return big_index, small_index
            else:
                return small_index, big_index

def single_io_test(func: Callable[[List[int], int], Tuple], test_lst: List[int], 
                    target: int, expected_result: Tuple[int]) -> bool:
    """
    Function to test the correctness of target_sum_slow and target_sum_fast (or functions with same signature and different implementation). 
    Tests a few trial inputs against expected output. Takes a function as argument and return True if results is correct, False otherwise.

    :param func: target_sum_slow or target_sum_fast or equivalent function with different implementation
    :return: True if correct, False otherwise
    """
    result_dict = func(test_lst, target)
    if result_dict == expected_result:
        return True
    else:
        print(f"Function {func.__name__} is incorrect.")
        print(f"Tested input: {test_lst}")
        print(f"Expected output: {expected_result}")
        print(f"Actual output: {result_dict}")
        return False

def multiple_io_tests(func: Callable[[List[int], int], Tuple]) -> Tuple[int]:
    """
    Helper functions to run multiple io tests. Takes as argument the lst_to_dict function to be tested and returns a tuple
    whose first element is the number of passed tests and second element the number of failed tests.

    :param func: lst_to_dict_slow or lst_to_dict_fast (or function with same signature and different implementation)
    :return: Tuple with count of succesful and failed tests.
    """
    success_count = 0
    fail_count = 0

    test_lst_1 = [1, 2, 3, 5, 9, 15]
    target = 7
    expected_result_1 = (1, 3)
    result = single_io_test(func, test_lst_1, target, expected_result_1)
    if result is True:
        success_count += 1
    else:
        fail_count += 1

    print(f"IO test results for {func.__name__}: {success_count} successful and {fail_count} failed.")
    return success_count, fail_count

def comparative_tests(func_1: Callable[[List[int], int], Tuple], func_2: Callable[[List[int], int], Tuple], reps: int = 20) -> Tuple[int]:
    """
    Test two lst_to_dict functions by calling them with the same (random) input and comparing whether the outputs are equal.
    Returns a tuple where the first int is the number of equal results and the second int is the number of different results.

    :param func_1: first list_to_dict function for testing
    :param func_2: second list_to_dict function for testing
    :param reps: number of tests to be performed, defaults to 10
    :return: Tuple with counts of equal results and different results
    """
    # variables for easy modification 
    list_len = 50
    max_num = 100
    target = random.randrange(list_len // 2)

    equal_count = 0
    diff_count = 0
    for _ in range(reps):
        unique_nums = set()
        while len(unique_nums) < list_len:
            rand_number = random.randrange(max_num)
            unique_nums.add(rand_number)
        test_lst = list(unique_nums)
        result_1 = func_1(test_lst, target)
        result_2 = func_2(test_lst, target)
        if result_1 == result_2:
            equal_count += 1
        else:
            print(f"Functions obtained different results.")
            print(f"Input data: list = {test_lst}, target={target}")
            print(f"Output of {func_1.__name__}: ")
            print(result_1)
            print(f"Output of {func_2.__name__}:")
            print(result_2)
            diff_count += 1
    print(f"Random comparative test results: out of {reps} trials, {equal_count} equal results and {diff_count} different results were obtained.")
    return equal_count, diff_count

def single_speed_trial(input_len: int, func: Callable[[List[int], int, int], Dict]) -> int:
    """
    Function to test speed of lst_to_dict functions. Generates a list of random distinct integers of the desired input length in the 
    desired range and measures time taken in milliseconds. If trial_count is changed to an int greater than 1, multiple trials are 
    performed and the average time is returned.

    :param input_len: desired length of input list for testing.
    :param func: lst_to_dict function to be tested.
    :param range_top: the greatest number that could be randomly generated 
    :return: time in milliseconds
    """
    unique_nums = set()
    target = random.randrange(input_len // 2)
    while len(unique_nums) <= input_len:
        rand_number = random.randrange(input_len * 2)
        unique_nums.add(rand_number)
    test_lst = list(unique_nums)
    random.shuffle(test_lst)
    random.shuffle(test_lst)
    random.shuffle(test_lst)
    start_time = time.time_ns() // 1_000_000
    result = func(test_lst, target)
    found = False
    if result:
        found = True
    end_time = time.time_ns() // 1_000_000
    elapsed_time = end_time - start_time
    print(f"For function {func.__name__}, time taken for input length {input_len} was {elapsed_time}ms")
    if found:
        first_index = result[0]
        second_index = result[1]
        first_num = test_lst[first_index]
        second_num = test_lst[second_index]
        print(f"The function found numbers adding up to target of {target}: {first_num} + {second_num} at indices {first_index} and {second_index}.")
    else:
        print("No numbers adding up to target were found")
    return elapsed_time

def multiple_speed_trials(input_len: int, func: Callable[[List[int], int, int], Dict], trial_count: int) -> int:
    """
    Helper function which runs multiple speed trials and returns the average time.

    :param input_len: desired length of input list for testing.
    :param func: lst_to_dict function to be tested.
    :param range_top: the greatest number that could be randomly generated 
    :param trial_count: number of times the experiment is repeated.
    :return: average time in milliseconds
    """
    time_results = []
    for _ in range(trial_count):
        result = single_speed_trial(input_len, func)
        time_results.append(result)
    average_time = round(sum(time_results) / len(time_results))
    print(f"For function {func.__name__}, average time taken for input length {input_len} over {trial_count} trials was {average_time}ms")
    return average_time

def run_tests(io_correctness: bool = True, comparative_correctness: bool = True, speed: bool = True, input_length: int = 10_000) -> None:
    if io_correctness:
        _ = multiple_io_tests(target_sum_slow)
        _ = multiple_io_tests(target_sum_fast)
    if comparative_correctness:
        _ = comparative_tests(target_sum_slow, target_sum_fast)
    if speed:
        _ = multiple_speed_trials(input_length, target_sum_slow, 20)
        _ = multiple_speed_trials(input_length, target_sum_fast, 20)


if __name__ == '__main__':
    run_tests()
