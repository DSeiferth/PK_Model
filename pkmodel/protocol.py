#
# Protocol class
#

class Protocol:
    """A Pharmokinetic (PK) protocol

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, dose_amount, subcutaneous=False,
                 k_a=1, continuous=False, continuous_period=[0, 0],
                 dose_times=[], multiple=False):
        self.subcutaneous = subcutaneous
        self.k_a = k_a
        self.dose_amount = dose_amount
        self.continuous = continuous
        self.multiple = multiple
        self.continuous_period = continuous_period
        self.dose_times = dose_times.sort()

    def dose(self, dose_amount):
        self.dose_amount = dose_amount
        return dose_amount

    def make_subcutaneous(self, k_a):
        self.k_a = k_a
        self.subcutaneous = True

    def make_continuous(self, time_added, time_removed):
        self.continuous = True
        self.continuous_period[0] = time_added
        self.continuous_period[1] = time_removed

    def add_dose_time(self, time):
        self.dose_times.append(time)
        self.dose_times.sort()

    def dose_time_function(self, t):
        dose_t_continuous, dose_t_multiple = 0, 0
        #if self.multiple:
        #    if t in self.dose_times:
        #        dose_t_multiple = self.dose_amount

        if self.continuous:
            if t <= self.continuous_period[1] and \
               t >= self.continuous_period[0]:
                dose_t_continuous = self.dose_amount

        dose_t = dose_t_continuous + dose_t_multiple
        return dose_t
