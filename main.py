import os
from poc.utils import read_test_cases, get_hand_result


if __name__ == '__main__':
    test_files = os.listdir('test_cases')
    for test_file in test_files:
        print('\n' + '-'*30)
        print(test_file)
        print('-'*30)
        
        test_cases = read_test_cases(f'test_cases/{test_file}')
        for i, test_case in enumerate(test_cases):
            hand_result = get_hand_result(**test_case)
            if set(hand_result) == set(test_case['result']):
                print(f'Test {i+1} - passed!')
            else:
                print(f'Test {i+1} - failed!')