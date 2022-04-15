from typing import List, Dict, Callable, Union, Tuple
import random
import time

def lst_to_dict_slow(lst: List[int], start: int, end: int) -> Dict[int, Union[int, None]]:
    """
    Given an unsorted list of integers, and two integers denoting a range - 'start' and 'end', 
    create a dictionary whose keys are all the integers in the given range (inclusive) and whose values
    are the indices of those numbers if the numbers are in the list, or None otherwise.
    The proposed time complexity is O(n*n) = O(n^2).

    :param lst: list of unsorted integers
    :param start: integer denoting start of range
    :param end: integer denoting end of range
    :return: dict with numbers in range as keys and indices or None as values.
    """
    dict = {}
    # loop over numbers in range 
    for i in range(start,end + 1):
        index = None
        # loop over entire list to check if number in list
        for j, value in enumerate(lst):
            if value == i:
                index = j
                break
        dict[i] = index
    return dict

def lst_to_dict_fast(lst: List[int], start: int, end: int) -> Dict[int, Union[int, None]]:
    """
    Given an unsorted list of integers, and two integers denoting a range - 'start' and 'end', 
    create a dictionary whose keys are all the integers in the given range (inclusive) and whose values
    are the indices of those numbers if the numbers are in the list, or None otherwise.
    The proposed time complexity is O(n + nlog(n) + n + n), simplifying to O(nlog(n)).

    :param lst: list of unsorted integers
    :param start: integer denoting start of range
    :param end: integer denoting end of range
    :return: dict with numbers in range as keys and indices or None as values.
    """
    original_index_dict = {}
    result_dict = {}
    # Save original indices into dict - O(n)
    for index,value in enumerate(lst):
        original_index_dict[value] = index
    # Sort list - O(nlog(n))
    lst.sort()
    index = 0
    # iterate over whole list - O(n)
    while index < len(lst) - 1:
        current_element = lst[index]
        next_element = lst[index + 1]
        if current_element > end:
            break
        if current_element < start:
            if next_element > start:
                for k in range(start, next_element):
                    result_dict[k] = None
            index += 1
            continue
        result_dict[current_element] = index
        # iterate over 'gap' between current element and next element of the list.
        # for example if current element is 8 and next element is 12, iterate over 8 to 11.
        # this does not really depend on the size of the input list - O(1)
        for j in range(current_element + 1, next_element + 1):
            # if index == len(lst) - 2 and next_element == end:
            #     result_dict[j+1] = end
            if j > end:
                break
            result_dict[j] = None
        # If we are on last iteration, and last element of list is less than end, we need to add None for
        # numbers between last element of list and end
        if index == len(lst) - 2:
            for j in range(next_element, end + 1):
                if j > end:
                    break
                result_dict[j] = None
            # if the last element in the list is less than end, add its index (previous for loop set it to None).
            if next_element <= end:
                result_dict[next_element] = index
        index += 1
    # 'translate' back to orignal indices, because indices were changed by sorting - O(n)
    for key in original_index_dict:
        if result_dict.get(key) is not None:
            result_dict[key] = original_index_dict[key]
    return result_dict

def lst_to_dict_simple(lst: List[int], start: int, end: int) -> Dict[int, Union[int, None]]:
    """
    Given an unsorted list of integers, and two integers denoting a range - 'start' and 'end', 
    create a dictionary whose keys are all the integers in the given range (inclusive) and whose values
    are the indices of those numbers if the numbers are in the list, or None otherwise.
    The proposed time complexity is O(n).

    :param lst: list of unsorted integers
    :param start: integer denoting start of range
    :param end: integer denoting end of range
    :return: dict with numbers in range as keys and indices or None as values.
    """
    result_dict = {}
    # loop over entire list and add numbers that are within range
    # as dict keys and their index as corresponding values. O(n).
    for index, value in enumerate(lst):
        if value >= start and value <= end:
            result_dict[value] = index
    # loop over range and corresponding value of numbers to either the index
    # or None if number is not to be found. O(len(range))
    for i in range(start, end + 1):
        result_dict[i] = result_dict.get(i)
    return result_dict

def single_io_test(func: Callable[[List[int], int, int], Dict], test_lst: List[int], 
                    start: int, end: int, expected_result: Dict[int, Union[int, None]]) -> bool:
    """
    Function to test the correctness of lst_to_dict_slow and lst_to_dict_fast (or function with same signature and different implementation). Tests a few
    trial inputs against expected output. Takes a function as argument and return True if results is correct, False otherwise.

    :param func: lst_to_dict_slow or lst_to_dict_fast (or function with same signature and different implementation)
    :return: True if correct, False otherwise
    """
    result_dict = func(test_lst, start, end)
    if result_dict == expected_result:
        return True
    else:
        print(f"Function {func.__name__} is incorrect.")
        print(f"Tested input: {test_lst}")
        print(f"Expected output: {expected_result}")
        print(f"Actual output: {result_dict}")
        return False

def multiple_io_tests(func: Callable[[List[int], int, int], Dict]) -> Tuple[int]:
    """
    Helper functions to run multiple io tests. Takes as argument the lst_to_dict function to be tested and returns a tuple
    whose first element is the number of passed tests and second element the number of failed tests.

    :param func: lst_to_dict_slow or lst_to_dict_fast (or function with same signature and different implementation)
    :return: Tuple with count of succesful and failed tests.
    """
    success_count = 0
    fail_count = 0

    test_lst_1 = [2, 1, 10, 0, 4, 3, 11]
    start_1 = 3
    end_1 = 10
    expected_result_1 = {
        3: 5,
        4: 4,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        10: 2
    }
    result = single_io_test(func, test_lst_1, start_1, end_1, expected_result_1)
    if result is True:
        success_count += 1
    else:
        fail_count += 1
    
    test_lst_2 = [0, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 32, 35, 36, 38, 39]
    start_2 = 5
    end_2 = 40
    expected_result_2 = {
        5: None, 6: None, 7: None, 8: None, 9: None, 10: None, 11: None, 12: None, 13: None, 14: None, 15: 1, 16: 2, 17: None, 
        18: 3, 19: 4, 20: 5, 21: 6, 22: 7, 23: 8, 24: 9, 25: 10, 26: None, 27: 11, 28: 12, 29: 13, 30: 14, 31: None, 32: 15, 
        33: None, 34: None, 35: 16, 36: 17, 37: None, 38: 18, 39: 19, 40: None
    }
    result = single_io_test(func, test_lst_2, start_2, end_2, expected_result_2)
    if result is True:
        success_count += 1
    else:
        fail_count += 1

    test_lst_3 = [2, 4, 5, 6, 7, 8, 16, 19, 20, 21, 22, 24, 25, 29, 30, 31, 32, 33, 35, 37]
    start_3 = 5
    end_3 = 40
    expected_result_3 = {
        5: 2, 6: 3, 7: 4, 8: 5, 9: None, 10: None, 11: None, 12: None, 13: None, 14: None, 15: None, 16: 6, 17: None, 18: None, 19: 7,
        20: 8, 21: 9, 22: 10, 23: None, 24: 11, 25: 12, 26: None, 27: None, 28: None, 29: 13, 30: 14, 31: 15, 32: 16, 33: 17, 34: None, 
        35: 18, 36: None, 37: 19, 38: None, 39: None, 40: None}
    result = single_io_test(func, test_lst_3, start_3, end_3, expected_result_3)
    if result is True:
        success_count += 1
    else:
        fail_count += 1

    print(f"IO test results for {func.__name__}: {success_count} successful and {fail_count} failed.")
    return success_count, fail_count



def comparative_tests(func_1: Callable[[List[int], int, int], Dict], func_2: Callable[[List[int], int, int], Dict], reps: int = 10) -> Tuple[int]:
    """
    Test two lst_to_dict functions by calling them with the same (random) input and comparing whether the outputs are equal.
    Returns a tuple where the first int is the number of equal results and the second int is the number of different results.

    :param func_1: first list_to_dict function for testing
    :param func_2: second list_to_dict function for testing
    :param reps: number of tests to be performed, defaults to 10
    :return: Tuple with counts of equal results and different results
    """
    # variables for easy modification 
    list_len = 20
    max_num = 20
    start = 5
    end = 40

    equal_count = 0
    diff_count = 0
    for _ in range(reps):
        unique_nums = set()
        while len(unique_nums) < list_len:
            rand_number = random.randrange(max_num)
            unique_nums.add(rand_number)
        test_lst = list(unique_nums)
        result_1 = func_1(test_lst, start, end)
        result_2 = func_2(test_lst, start, end)
        if result_1 == result_2:
            equal_count += 1
        else:
            print(f"Functions obtained different results.")
            print(f"Input data: list = {test_lst}, start = {start}, end = {end}")
            print(f"Output of {func_1.__name__}: ")
            print(result_1)
            print(f"Output of {func_2.__name__}:")
            print(result_2)
            diff_count += 1
    print(f"Random comparative test results: out of {reps} trials, {equal_count} equal results and {diff_count} different results were obtained.")
    return equal_count, diff_count

def single_speed_trial(input_len: int, func: Callable[[List[int], int, int], Dict], range_top: int = None) -> int:
    """
    Function to test speed of lst_to_dict functions. Generates a list of random distinct integers of the desired input length in the 
    desired range and measures time taken in milliseconds. If trial_count is changed to an int greater than 1, multiple trials are 
    performed and the average time is returned.

    :param input_len: desired length of input list for testing.
    :param func: lst_to_dict function to be tested.
    :param range_top: the greatest number that could be randomly generated 
    :return: time in milliseconds
    """
    if range_top is None:
        range_top = input_len * 10
    unique_nums = set()
    while len(unique_nums) <= input_len:
        rand_number = random.randrange(range_top)
        unique_nums.add(rand_number)
    test_lst = list(unique_nums)
    start = 5
    end = input_len // 2
    start_time = time.time_ns() // 1_000_000
    _ = func(test_lst, start, end)
    end_time = time.time_ns() // 1_000_000
    elapsed_time = end_time - start_time
    print(f"For function {func.__name__}, time taken for input length {input_len} was {elapsed_time}ms")
    return elapsed_time

def multiple_speed_trials(input_len: int, func: Callable[[List[int], int, int], Dict], trial_count: int, range_top: int = None) -> int:
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
        result = single_speed_trial(input_len, func, range_top)
        time_results.append(result)
    average_time = round(sum(time_results) / len(time_results))
    print(f"For function {func.__name__}, average time taken for input length {input_len} over {trial_count} trials was {average_time}ms")
    return average_time

def run_tests(io_correctness: bool = True, comparative_correctness: bool = True, speed: bool = True, input_length: int = 1_000_000) -> None:
    if io_correctness:
        _ = multiple_io_tests(lst_to_dict_slow)
        _ = multiple_io_tests(lst_to_dict_fast)
        _ = multiple_io_tests(lst_to_dict_simple)
    if comparative_correctness:
        _ = comparative_tests(lst_to_dict_slow, lst_to_dict_fast)
        _ = comparative_tests(lst_to_dict_simple, lst_to_dict_slow)
    if speed:
        # _ = single_speed_trial(input_length, lst_to_dict_slow)
        _ = single_speed_trial(input_length, lst_to_dict_fast)
        _ = single_speed_trial(input_length, lst_to_dict_simple)


if __name__ == '__main__':
    run_tests()
