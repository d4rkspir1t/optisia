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
        self.ct_min_comp = ['0.0', '0.33', '0.67', '1.0']  # -cta
        self.ct_max_comp_prefix = '-ctb'
        self.ct_max_comp = ['1', '3', '10']  # -ctb

        self.r_superdiags = ['', '-rsd']  # -rsd
        self.r_count_prefix = '-r'
        self.r_count = ['1', '5', '10']  # -r

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
            self.cmin = ['0', '5', '15', '30']  # -cmin

            self.bbcomp = ['', '-bbcomp']  # -bbcomp
