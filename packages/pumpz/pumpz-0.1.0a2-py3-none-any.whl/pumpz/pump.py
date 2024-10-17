import math
import sympy
from .utilities import decompose_dict, factor_check

class pump:

    def __init__(
        self,
        file,
        dia,
        time=0,
    ):
        self.file = file
        self.dia = dia
        if self.dia < 0.1 or self.dia > 50.0:
            raise Exception('Diameter is invalid. Must be between 0.1 - 50.0 mm')
        self.time = time
        self.loop = []
        self.rate = 0
        if self.dia > 14.0:
            self.vol_units = 'mcL'
        else:
            self.vol_units = 'mL'
        # self.vol_inf=0
        # self.vol_wdr=0
        self.dir = ''
        self.rat = 0
        self.phase_name = ''
        self.phase_num = 1
        self.phase_ref = {}
        self.sync_is_useable = True
        self.sub_program= {}


    def init(*args):
        for self in args:
            self.file.write(f"dia {self.dia}\nal 1\nbp 1\nPF 0\n")
    
    def phase_to_string(self, phase) -> str:
        if type(phase) == type(1):
            if phase > 0 and phase < 99:
                return str(phase).zfill(2)
            else:
                raise Exception(f'phase argument is invalid')
        elif type(phase) == type('string'):
            return str(self.phase_ref[self.phase_name]).zfill(2)
    
    def phase(self):
        self.file.write(f'\nphase {self.phase_name}\n')
        self.phase_ref[self.phase_name] = self.phase_number
        self.phase_name = ''
        self.phase_num += 1

    def label(self, label):
        self.phase_name = label
        return label

    def rate(self, rate: int, vol: int, dir: str):
        self.phase()
        self.dir = dir
        self.rat = rate
        self.time += vol / rate * 60 * self.getloop()
        self.file.write(f"fun rat\nrat {self.rat} mm\nvol {vol}\ndir {self.dir}\n")
    
    # fil, incr, decr, not included

    def beep(self):
        self.phase()
        self.file.write(f'fun bep\n')

    def pause(self, length: int):
        if length <= 99:
            self.phase()
            self.file.write(f"fun pas {length}\n")
            self.time += length * self.getloop()

        elif length <= 99 * 3:
            self.pas(99)
            self.pas(length - 99)
        else:
            multiples = factor_check(decompose_dict(sympy.factorint(length)))
            if multiples != (0, 0) and len(multiples) <= 3:
                for i in range(len(multiples) - 1):
                    self.loopstart(multiples[1 + i])
                self.pas(multiples[0])
                for i in range(len(multiples) - 1):
                    self.loopend()
            else:
                self.pas(length % 50, self.getloop())
                length -= length % 50
                self.pas(length, self.getloop())

    def subprogram_label(self, label: int):
        self.phase()
        self.file.write(f'fun prl {label}\n')

    def subprogram_select(self):
        self.phase()
        self.file.write(f'fun pri')

    def loopstart(self, count):
        self.loop.append(count)
        if len(self.loop) > 3:
            raise Exception("Up to three nested loops, you have too many")
        self.phase()
        self.file.write(f"fun lps\n")

    def loopend(self):
        self.file.write(f"\nphase\nfun lop {self.loop.pop()}\n")

    def getloop(self):
        if len(self.loop) >= 1:
            return self.loop[-1]
        else:
            return sympy.prod(self.loop)
    
    def jump(self, phase_name: str):
        self.phase()
        self.sync_is_useable = False
        for key in self.phase_name.keys():
            if key == phase_name:
                self.file.write(f'fun jmp {self.phase_name(key)}')
                return
        raise Exception('No such phase found')
    
    def if_low(self, phase):
        self.phase()
        self.file.write(f'fun if {self.phase_to_string(phase)}')
    
    def event_trap(self, phase):
        self.phase()
        self.file.write(f'fun evn {self.phase_to_string(phase)}')
    
    def event_trap_sq(self,phase):
        self.phase()
        self.file.write(f'fun evs {self.phase_to_string(phase)}')
    
    def event_reset(self):
        self.phase()
        self.file.write(f'fun evr')

    # cld: clear total dispense volume, not implemented

    def trg(self, num: int):
        self.phase()
        self.file.write(f'fun trg {num}')

    def out(self, n):
        self.phase()
        self.file.write(f'fun out {int(n)}')

    def stop(*args):
        for self in args:
            self.phase()
            self.file.write(f"fun stp\n")

    def sync(*args):
        max_time = 0
        for arg in args:
            if arg.time > max_time:
                max_time = arg.time
            if arg.sync_is_useable == False:
                raise Exception(f'sync isn\'t useable with {arg}')
        for arg in args:
            time_diff = max_time - arg.time
            if time_diff > 0:
                arg.pas(math.ceil(time_diff))

