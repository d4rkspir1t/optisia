class Switches:
    def __init__(self, base, input_f, recalg):
        self.algorithm_prefix = '-a'
        self.algorithm = base
        self.input_file_prefix = '-i'
        self.input_file = input_f  # -i

        if self.algorithm == 'RecurSIA':
            self.recursia = '-recalg'  # -recalg, only when recursia
            self.recalg_alg = recalg
        else:
            self.recursia = ''
            self.recalg_alg = ''

        self.pitch = ['', '-d']  # -d

        self.comp_trawler = ['', '-ct']  # -ct
        self.ct_min_comp_prefix = '-cta'
        self.ct_min_comp = ['0.5', '0.67', '1.0']  # -cta more than 0.5
        self.ct_max_comp_prefix = '-ctb'
        self.ct_max_comp = ['3', '5', '7', '10']  # -ctb 3-10

        self.r_superdiags = ['', '-rsd']  # -rsd
        self.r_count_prefix = '-r'
        self.r_count = ['1', '5', '10']  # -r not too high

        self.rrt = ['', '-rrt']  # -rrt

        if self.algorithm == 'Forth' or self.recalg_alg == 'Forth':
            self.crlow_prefix = '-crlow'
            self.crlow = ['0.2', '0.6', '0.9']  # -crlow

            self.crhi_1 = '-crhi'  # -crhi
            self.crhi_2 = '1.0'  # -crhi

            self.comlow_prefix = '-comlow'
            self.comlow = ['0.2', '0.6', '0.9']  # -comlow

            self.comhi_1 = '-comhi'  # -comhi
            self.comhi_2 = '1.0'  # -comhi

            self.cmin_prefix = '-cmin'
            self.cmin = ['5', '15', '30']  # -cmin 5<

            self.bbcomp = ['', '-bbcomp']  # -bbcomp

# topn = 5