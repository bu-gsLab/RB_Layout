from yaml import safe_load
import numpy as np
from functools import total_ordering

@total_ordering
class Row:
    def __init__(self, modules, row_index, keepout_radius, tolerance):
        self.modules = []
        self.num_modules = 0
        self.row_index = row_index
        self.is_row = True

        self.pb_distance = 0
        self.rb_distance = 0

        self.module_total_short = modules[0].RB_PB_short
        self.rb_short = modules[0].RB_short

        self.tol = tolerance
        self.R = keepout_radius

        self.in_tolerance = {"RB": False, "PB": False}
        self.over_tolerance = False
        self.crossing = {"RB": False, "PB": False}

        self.load_DEE_info()
        for mod in modules:
            self.add_module(mod)

    def __add__(self, mod):
        self.add_module(mod)
        return self
    
    def __str__(self):
        label_list = [mod.label for mod in self.modules[::-1]]
        modules_str = ", ".join(label_list)
        return f"| {modules_str:<30} | RB dist: {self.rb_distance:>10.2f}mm | PB dist: {self.pb_distance:>10.2f}mm | Modules: {self.num_modules:>10} |"
    
    def __eq__(self, other):
        return self.num_modules == other.num_modules
    
    def __lt__(self, other):
        return self.num_modules < other.num_modules
    
    def load_DEE_info(self):
        with open('dimensions.yaml', 'r') as f:
            data = safe_load(f)
        
        self.DEE = data["DEE"]
        self.origin_offset =  self.DEE["origin_offset"]
        self.additional_offset = self.DEE["small_dim_additional_offset"]
        if self.row_index in self.additional_offset:
            self.row_origin = (self.origin_offset["small_dim"] + self.additional_offset[self.row_index], self.origin_offset["big_dim"]-self.module_total_short*self.row_index)
        else:
            self.row_origin = (self.origin_offset["small_dim"], self.origin_offset["big_dim"]-self.module_total_short*self.row_index)

        if self.row_index <= 12:
            self.rb_corner = [self.row_origin[0], self.row_origin[1] + self.rb_short]
            self.pb_corner = [self.row_origin[0], self.row_origin[1] + self.module_total_short]
            if self.R < self.pb_corner[1]:
                raise ValueError("Entire top edge of first module outside keepout")
        else:
            self.rb_corner = [self.row_origin[0], self.row_origin[1]]
            self.pb_corner = [self.row_origin[0], self.row_origin[1] + self.rb_short]
            if self.R < abs(self.rb_corner[1]):
                raise ValueError("Entire bottom edge of first module outside keepout")
                    
        self.rb_target = np.sqrt(self.R**2-self.rb_corner[1]**2)
        self.pb_target = np.sqrt(self.R**2-self.pb_corner[1]**2)
        
    def add_module(self, mod):
        self.modules.append(mod)
        self.num_modules += mod.num
        self.pb_corner[0] += (self.rb_corner[0] - self.pb_corner[0]) + mod.PB_long
        self.rb_corner[0] += mod.RB_long

        self.rb_distance = self.rb_target - self.rb_corner[0]
        self.pb_distance = self.pb_target - self.pb_corner[0]
        self.check_distances()

    def check_distances(self):
        if self.rb_distance < 0 and abs(self.rb_distance) < self.tol:
            self.in_tolerance["RB"] = True
            self.crossing["RB"] = True
        elif self.rb_distance > 0 and abs(self.rb_distance) < self.tol:
            self.in_tolerance["RB"] = True
            self.crossing["RB"] = False
        elif self.rb_distance < 0 and abs(self.rb_distance) > self.tol:
            self.over_tolerance = True
            return
        else:
            pass

        if self.pb_distance < 0 and abs(self.pb_distance) < self.tol:
            self.in_tolerance["PB"] = True
            self.crossing["PB"] = True
        elif self.pb_distance > 0 and abs(self.pb_distance) < self.tol:
            self.in_tolerance["PB"] = True
            self.crossing["PB"] = False
        elif self.pb_distance < 0 and abs(self.pb_distance) > self.tol:
            self.over_tolerance = True
            return
        else:
            pass
        
        return