from rich.prompt import Prompt
import inspect
from enum import Enum

def _get_f_name():
    return  f"[DEBUG] In function: {inspect.currentframe().f_back.f_code.co_name}"

class StepResult(Enum):
    Cancel = 0
    Next = 1
    Previous = 2

class DIRECTION_CHOICES(Enum):
    n = "(N)ext"
    p = "(P)revious"

DIRECTION_CHOICES_NAMES = [member.name for member in DIRECTION_CHOICES]    
DIRECTION_CHOICES_VALUES = [member.value for member in DIRECTION_CHOICES]

class RipWizard:
    _steps = []
    _current_step: int = 0

    def __init__(self):
        self._steps = [
            self._select_disk,
            self._select_title,
            self._search_movies,
            self._select_movie,
        ]
        self._current_step = -1

    def _choose_direction(self, answer: str):
        answer_e = DIRECTION_CHOICES[answer]
        if answer_e == DIRECTION_CHOICES.p:
            self.prev_step()

        if answer_e == DIRECTION_CHOICES.n:
            self.next_step()

    def next_step(self):
        current_step = self._current_step
        print(current_step)
        current_step += 1
        if current_step < len(self._steps):
            self._current_step = current_step
            self._steps[current_step]()
            

    def prev_step(self):

        current_step = self._current_step
        print(current_step)
        current_step -= 1
        if current_step > 0:
            self._current_step = current_step
            self._steps[current_step]()

    def _select_disk(self):
        name = f"[DEBUG] In function: {_get_f_name()}"
        msg = f"{name}. Choose {DIRECTION_CHOICES_VALUES}"
        answer = Prompt.ask(msg, choices=DIRECTION_CHOICES_NAMES, show_choices=True)
        self._choose_direction(answer)


    def _select_title(self):
        name = f"[DEBUG] In function: {_get_f_name()}"
        msg = f"{name}. Choose {DIRECTION_CHOICES_VALUES}"
        answer = Prompt.ask(msg, choices=DIRECTION_CHOICES_NAMES, show_choices=True)
        self._choose_direction(answer)

    def _search_movies(self):
        
        name = f"[DEBUG] In function: {_get_f_name()}"
        msg = f"{name}. Choose {DIRECTION_CHOICES_VALUES}"
        answer = Prompt.ask(msg, choices=DIRECTION_CHOICES_NAMES, show_choices=True)
        self._choose_direction(answer)

    def _select_movie(self):
        name = f"[DEBUG] In function: {_get_f_name()}"
        msg = f"{name}. Choose {DIRECTION_CHOICES_VALUES}"
        answer = Prompt.ask(msg, choices=DIRECTION_CHOICES_NAMES, show_choices=True)
        self._choose_direction(answer)

    def _finish(self):
        name = f"[DEBUG] In function: {_get_f_name()}"
        answer = Prompt.ask(name, choices=['previous', 'next', 'skip'])
        self._choose_direction(answer)



w = RipWizard()
w.next_step()
    
