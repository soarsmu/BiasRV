import sys
sys.path.append('./fine-tuning')
sys.path.append('./gender')
from bias_rv.MutantGeneration import MutantGeneration
import random
import numpy as np

seed = 42
random.seed(seed)
np.random.seed(seed)


def check_property_1(original_result, female_mut_results, male_mut_results, N):
    return sum(female_mut_results) == sum(male_mut_results) and sum(female_mut_results) == original_result * N


class biasRV():
    def __init__(self, predict, X, Y, alpha):
        self.predict = predict
        self.X = X
        self.Y = Y
        self.alpha = alpha

    def set_predictor(self, predict):
        self.predict = predict
    
    def set_X(self, X):
        self.X = X

    def set_Y(self, Y):
        self.Y = Y

    def set_alpha(self, alpha):
        self.alpha = alpha


    def verify_only_property_2(self, text:str):
        '''
        Only verify using the distributional individual fairness.
        '''
        is_satisfy_prop_2 = True
        original_result = self.predict(text)
        mg = MutantGeneration(text)
        alpha = self.alpha
        
        if len(mg.getMutants()) > 0:
            ### if there are mutants generated
            male_mutants = mg.get_male_mutants()
            female_mutants = mg.get_female_mutants()
            
            
            male_mut_results = []
            for each_text in male_mutants:
                male_mut_results.append(self.predict(each_text))
            female_mut_results = []
            for each_text in female_mutants:
                female_mut_results.append(self.predict(each_text))

            pos_M = 1.0 * sum(male_mut_results) / (len(male_mut_results))
            pos_F = 1.0 * sum(female_mut_results) / (len(female_mut_results))

            is_satisfy_prop_2 = True if abs(pos_M - pos_F) < alpha else False

        return original_result, is_satisfy_prop_2

    def verify(self, text: str):
        N = self.X
        L = self.Y
        alpha = self.alpha
        is_bias = False
        is_satisfy_prop_1 = True
        is_satisfy_prop_2 = True

        # generate mutants
        original_result = self.predict(text)

        mg = MutantGeneration(text)

        
        if len(mg.getMutants()) > 0:
            ### if there are mutants generated
            male_mutants = mg.get_male_mutants()
            female_mutants = mg.get_female_mutants()

            assert len(male_mutants) == len(female_mutants)

            if N > len(female_mutants):
                N = len(female_mutants)
                L = 0
            elif N + L > len(female_mutants):
                L = len(female_mutants) - N

            ### select N mutants from each gender
            # random selection
            sampled_male_mutants = random.sample(male_mutants, N + L)
            sampled_female_mutants = random.sample(female_mutants, N + L)

            ## processing male_mutants
            male_mut_results = []
            for each_text in sampled_male_mutants[0: N]:
                male_mut_results.append(self.predict(each_text))
            
            ## processing female_mutants
            female_mut_results = []
            for each_text in sampled_female_mutants[0: N]:
                female_mut_results.append(self.predict(each_text))

            ### verify property (1)
            is_satisfy_prop_1 = check_property_1(original_result, female_mut_results, male_mut_results, N)
            if is_satisfy_prop_1:
                ### satisfy property (1), no bias
                pass
            else:
                ### progress to step (2)

                # compute pos_M for male
                for each_text in sampled_male_mutants[N: N + L]:
                    male_mut_results.append(self.predict(each_text))
                pos_M = 1.0 * sum(male_mut_results) / (N + L)
                # compute pos_F for female
                for each_text in sampled_female_mutants[N: N + L]:
                    female_mut_results.append(self.predict(each_text))
                pos_F = 1.0 * sum(female_mut_results) / (N + L)

                ### verify property (2) |pos_M - pos_F| < alpha
                is_satisfy_prop_2 = True if abs(pos_M - pos_F) < alpha else False
        
        if not is_satisfy_prop_2:
            is_bias = True

        return original_result, is_bias