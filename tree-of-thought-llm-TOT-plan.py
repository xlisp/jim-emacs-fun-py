坚持去λ化(中-易) jim-emacs-fun-py  master @ import argparse
........................................... from tot.methods.bfs import solve
........................................... from tot.tasks.game24 import Game24Task
...........................................
坚持去λ化(中-易) jim-emacs-fun-py  master @
坚持去λ化(中-易) jim-emacs-fun-py  master @ Game24Task
tot.tasks.game24.Game24Task
坚持去λ化(中-易) jim-emacs-fun-py  master @ Game24Task??
Type:             type
String form:      <class 'tot.tasks.game24.Game24Task'>
File:             /opt/anaconda3/lib/python3.11/site-packages/tot/tasks/game24.py
Init definition:  Game24Task(self, file='24.csv')
Source:
class Game24Task(Task):
    """
    Input (x)   : a string of 4 numbers
    Output (y)  : a trajectory of 3 steps to reach 24
    Reward (r)  : 0 or 1, depending on whether the trajectory is correct
    Input Example:
        1 2 3 4
    Output Example:
        1 + 2 = 3 (left: 3 3 4)
        3 + 3 = 6 (left: 4 6)
        6 * 4 = 24 (left: 24)
        (1 + 2 + 3) * 4 = 24
    """
    def __init__(self, file='24.csv'):
        """
        file: a csv file (fixed)
        """
        super().__init__()
        path = os.path.join(DATA_PATH, '24', file)
        self.data = list(pd.read_csv(path)['Puzzles'])
        self.value_cache = {}
        self.steps = 4
        self.stops = ['\n'] * 4

    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int) -> str:
        return self.data[idx]

    def test_output(self, idx: int, output: str):
        expression = output.strip().split('\n')[-1].lower().replace('answer: ', '').split('=')[0]
        numbers = re.findall(r'\d+', expression)
        problem_numbers = re.findall(r'\d+', self.data[idx])
        if sorted(numbers) != sorted(problem_numbers):
            return {'r': 0}
        try:
            # print(sympy.simplify(expression))
            return {'r': int(sympy.simplify(expression) == 24)}
        except Exception as e:
            # print(e)
            return {'r': 0}

    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        return standard_prompt.format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        return cot_prompt.format(input=x) + y

    @staticmethod
    def propose_prompt_wrap(x: str, y: str='') -> str:
        current_numbers = get_current_numbers(y if y else x)
        if current_numbers == '24':
            prompt = cot_prompt.format(input=x) + 'Steps:' + y
            # print([prompt])
        else:
            prompt = propose_prompt.format(input=current_numbers)
        return prompt

    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        if 'left: ' not in last_line:  # last step
            ans = last_line.lower().replace('answer: ', '')
            # print([value_last_step_prompt.format(input=x, answer=ans)])
            return value_last_step_prompt.format(input=x, answer=ans)
        current_numbers = get_current_numbers(y)
        return value_prompt.format(input=current_numbers)

    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        if len(y.strip().split('\n')) == 4 and 'answer' not in y.lower():
            return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value

Init docstring:   file: a csv file (fixed)


tot.tasks.game24.Game24Task
坚持去λ化(中-易) jim-emacs-fun-py  master @ args = argparse.Namespace(backend='gpt-4', temperature=0.7, task
='game24', naive_run=False, prompt_sample=None, method_generate='propose', method_evaluate='value', method_s
elect='greedy', n_generate_sample=1, n_evaluate_sample=3, n_select_sample=5)
...........................................
坚持去λ化(中-易) jim-emacs-fun-py  master @ task = Game24Task()
...........................................
坚持去λ化(中-易) jim-emacs-fun-py  master @ ys, infos = solve(args, task, 900)
...........................................
functools.partial(<function gpt at 0x1526ceac0>, model='gpt-4', temperature=0.7)


-- new_ys --: ('10 - 4 = 6 (left: 5 6 6)\n', '10 - 5 = 5 (left: 4 5 6)\n', '10 / 5 = 2 (left: 2 4 6)\n', '4 * 5 = 20 (left: 6 10 20)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n', '4 + 5 = 9 (left: 6 9 10)\n', '5 + 6 = 11 (left: 4 10 11)\n', '6 - 4 = 2 (left: 2 5 10)\n', '6 * 4 = 24 (left: 5 10 24)\n')
-- sol values --: (3.0, 3.0, 3.0, 3.0, 3.0, 2.001, 2.001, 2.001, 1.002)
-- choices --: ['10 - 4 = 6 (left: 5 6 6)\n', '10 - 5 = 5 (left: 4 5 6)\n', '10 / 5 = 2 (left: 2 4 6)\n', '4 * 5 = 20 (left: 6 10 20)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n']

-- new_ys --: ('10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n2.5 * 5 = 12.5 (left: 6 12.5)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n5 - 2.5 = 2.5 (left: 2.5 6)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n6 / 2.5 = 2.4 (left: 2.4 5)\n', '10 - 4 = 6 (left: 5 6 6)\n5 + 6 = 11 (left: 6 11)\n', '10 - 4 = 6 (left: 5 6 6)\n6 - 5 = 1 (left: 1 6)\n', '10 - 4 = 6 (left: 5 6 6)\n6 / 5 = 1.2 (left: 1.2 6)\n', '10 - 4 = 6 (left: 5 6 6)\n6 / 6 = 1 (left: 1 5)\n', '10 - 4 = 6 (left: 5 6 6)\n5 - 6 = -1 (left: -1 6)\n', '10 - 4 = 6 (left: 5 6 6)\n6 * 6 = 36 (left: 5 36)\n', '10 - 5 = 5 (left: 4 5 6)\n4 + 5 = 9 (left: 6 9)\n', '10 - 5 = 5 (left: 4 5 6)\n5 + 6 = 11 (left: 4 11)\n', '10 - 5 = 5 (left: 4 5 6)\n6 - 4 = 2 (left: 2 5)\n', '10 - 5 = 5 (left: 4 5 6)\n4 * 5 = 20 (left: 6 20)\n', '10 - 5 = 5 (left: 4 5 6)\n5 * 6 = 30 (left: 4 30)\n', '10 - 5 = 5 (left: 4 5 6)\n6 / 4 = 1.5 (left: 1.5 5)\n', '10 - 5 = 5 (left: 4 5 6)\n4 - 5 = -1 (left: -1 6)\n', '10 - 5 = 5 (left: 4 5 6)\n5 - 4 = 1 (left: 1 6)\n', '10 - 5 = 5 (left: 4 5 6)\n6 - 5 = 1 (left: 1 4)\n', '10 / 5 = 2 (left: 2 4 6)\n2 + 4 = 6 (left: 6 6)\n', '10 / 5 = 2 (left: 2 4 6)\n4 - 2 = 2 (left: 2 6)\n', '10 / 5 = 2 (left: 2 4 6)\n6 - 2 = 4 (left: 4 4)\n', '10 / 5 = 2 (left: 2 4 6)\n6 - 4 = 2 (left: 2 2)\n', '10 / 5 = 2 (left: 2 4 6)\n2 * 4 = 8 (left: 6 8)\n', '10 / 5 = 2 (left: 2 4 6)\n4 * 2 = 8 (left: 6 8)\n', '10 / 5 = 2 (left: 2 4 6)\n6 / 2 = 3 (left: 3 4)\n', '10 / 5 = 2 (left: 2 4 6)\n6 / 4 = 1.5 (left: 1.5 2)\n', '4 * 5 = 20 (left: 6 10 20)\n6 + 10 = 16 (left: 16 20)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 10 = 10 (left: 6 10)\n', '4 * 5 = 20 (left: 6 10 20)\n20 / 10 = 2 (left: 2 6)\n', '4 * 5 = 20 (left: 6 10 20)\n20 / 6 = 3.33 (left: 3.33 10)\n', '4 * 5 = 20 (left: 6 10 20)\n10 * 6 = 60 (left: 20 60)\n', '4 * 5 = 20 (left: 6 10 20)\n20 * 6 = 120 (left: 10 120)\n', '4 * 5 = 20 (left: 6 10 20)\n10 * 20 = 200 (left: 6 200)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n2.5 + 5 = 7.5 (left: 6 7.5)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n5 / 2.5 = 2 (left: 2 6)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n6 - 2.5 = 3.5 (left: 3.5 5)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n6 + 2.5 = 8.5 (left: 5 8.5)\n')
-- sol values --: (60.0, 60.0, 60.0, 1.002, 1.002, 1.002, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003)
-- choices --: ['10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n2.5 * 5 = 12.5 (left: 6 12.5)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n5 - 2.5 = 2.5 (left: 2.5 6)\n']

-- new_ys --: ('4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n', '10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n30 - 6 = 24 (left: 24)\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n4 + 20 = 24 (left: 24)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n10 + 14 = 24 (left: 24)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n5 - 2.5 = 2.5 (left: 2.5 6)\n6 / 2.5 = 2.4 (left: 2.4)\n', '10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n30 / 6 = 5 (left: 5)\n', '10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n30 + 6 = 36 (left: 36)\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n20 / 4 = 5 (left: 5)\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n20 - 4 = 16 (left: 16)\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n4 * 20 = 80 (left: 80)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 / 10 = 1.4 (left: 1.4)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 * 10 = 140 (left: 140)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n2.5 * 5 = 12.5 (left: 6 12.5)\n6 + 12.5 = 18.5 (left: 18.5)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n2.5 * 5 = 12.5 (left: 6 12.5)\n12.5 * 6 = 75 (left: 75)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n5 - 2.5 = 2.5 (left: 2.5 6)\n2.5 + 6 = 8.5 (left: 8.5)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n5 - 2.5 = 2.5 (left: 2.5 6)\n6 - 2.5 = 3.5 (left: 3.5)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n5 - 2.5 = 2.5 (left: 2.5 6)\n2.5 * 6 = 15 (left: 15)\n', '10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n6 * 30 = 180 (left: 180)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n2.5 * 5 = 12.5 (left: 6 12.5)\n12.5 - 6 = 6.5 (left: 6.5)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n2.5 * 5 = 12.5 (left: 6 12.5)\n12.5 / 6 = 2.08 (left: 2.08)\n')
-- sol values --: (40.001, 40.0, 40.0, 40.0, 20.002, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.002, 0.002, 0.001)
-- choices --: ['4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n', '10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n30 - 6 = 24 (left: 24)\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n4 + 20 = 24 (left: 24)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n10 + 14 = 24 (left: 24)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n5 - 2.5 = 2.5 (left: 2.5 6)\n6 / 2.5 = 2.4 (left: 2.4)\n']

-- new_ys --: ('10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n30 - 6 = 24 (left: 24)\nAnswer: (5 * (10 - 4)) - 6 = 24\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n4 + 20 = 24 (left: 24)\nAnswer: (4 * 5) + (10 - 6) = 24\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n10 + 14 = 24 (left: 24)\nAnswer: (4 * 5 - 6) + 10 = 24\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n4 + 2 = 6 (left: 6 8 8 14)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n4 + 8 = 12 (left: 2 8 12 14)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n4 + 14 = 18 (left: 2 8 8 18)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n2 * 4 = 8 (left: 8 8 8 14)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n8 / 4 = 2 (left: 2 2 8 14)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n14 / 4 = 3.5 (left: 2 3.5 8 8)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n14 - 4 = 10 (left: 2 8 8 10)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n8 - 4 = 4 (left: 2 4 4 14)\n', '10 / 4 = 2.5 (left: 2.5 5 6)\n5 - 2.5 = 2.5 (left: 2.5 6)\n6 / 2.5 = 2.4 (left: 2.4)\nNo possible next steps as there are not enough numbers to perform an operation.\n')
-- sol values --: (60.0, 60.0, 60.0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
-- choices --: ['10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n30 - 6 = 24 (left: 24)\nAnswer: (5 * (10 - 4)) - 6 = 24\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n4 + 20 = 24 (left: 24)\nAnswer: (4 * 5) + (10 - 6) = 24\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n10 + 14 = 24 (left: 24)\nAnswer: (4 * 5 - 6) + 10 = 24\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n4 + 2 = 6 (left: 6 8 8 14)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n4 + 8 = 12 (left: 2 8 12 14)\n']

['10 - 4 = 6 (left: 5 6 6)\n5 * 6 = 30 (left: 6 30)\n30 - 6 = 24 (left: 24)\nAnswer: (5 * (10 - 4)) - 6 = 24\n', '4 * 5 = 20 (left: 6 10 20)\n10 - 6 = 4 (left: 4 20)\n4 + 20 = 24 (left: 24)\nAnswer: (4 * 5) + (10 - 6) = 24\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n10 + 14 = 24 (left: 24)\nAnswer: (4 * 5 - 6) + 10 = 24\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n4 + 2 = 6 (left: 6 8 8 14)\n', '4 * 5 = 20 (left: 6 10 20)\n20 - 6 = 14 (left: 10 14)\n14 - 10 = 4 (left: 4)\n4 + 8 = 12 (left: 2 8 12 14)\n']
坚持去λ化(中-易) jim-emacs-fun-py  master @

