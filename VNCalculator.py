import math
import random as r
from decimal import Decimal

# symptom and drug concentration global arrays
symptomArray=['Vomiting', 'Diarrhoea', 'Pneumonia', 'Cystitis', 'Ventricular Tachycardia', 'Bacterial Infection']
concArray = [1, 2, 5, 10, 25, 50]
circuitsArray = [['T-piece', 2.5, 3], ['Bain', 2.5, 3], ['Mini Lack', 1, 1], ['Lack', 1, 1.5], ['Magill', 1, 1.5]]


#--------Patient Classes Start--------#


class Dog():
    def __init__(self):
        self.species = "Dog"
        self.dailyFluids = 50
        self.respirationRate = r.randint(10, 35)
        size = r.randint(1, 2)
        if size == 1:
            self.bodyweight = r.randint(101, 501) / 10
            if self.bodyweight < 20:
                self.medStrength = concArray[r.randint(2, 4)]
            else:
                self.medStrength = concArray[r.randint(3, 5)]
        else:
            self.bodyweight = r.randint(35, 99) / 10
            self.medStrength = concArray[r.randint(0, 2)]
        if self.bodyweight < 10:
            self.tidalVolume = 15
        else:
            self.tidalVolume = 10


class Cat():
    def __init__(self):
        self.species = "Cat"
        self.bodyweight = r.randint(20, 61) / 10
        self.dailyFluids = 50
        self.respirationRate = r.randint(10, 35)
        self.tidalVolume = 15


class Rabbit():
    def __init__(self):
        self.species = "Rabbit"
        self.bodyweight = r.randint(10, 50) / 10
        self.dailyFluids = 60

#-------------------FLUIDS CALCULATOR CLASS START--------------------------------#


class Fluids(Cat, Dog, Rabbit):
    def __init__(self):
        self.questType = "Fluids"

        # sets patient conditions

        self.unitArray = ["mls/hr", "s/drop", "ml", "second"]
        self.mlVsSec = r.randint(0, 1)
        self.dehydration = r.randint(0, 12)
        self.onGoingLoss = r.randint(0, 5) * 10
        pickCalc = r.randint(1, 4)
        if pickCalc < 2:
            self.dehydration = 0
        if self.dehydration == 0:
            self.onGoingLoss = 0
        self.dropsPerMl = 20

        # generates an patient object
        animalType = r.randint(1, 3)
        if animalType == 1:
            Dog.__init__(self)
        elif animalType == 2:
            Cat.__init__(self)
        else:
            Rabbit.__init__(self)

        # calculates fluid requirements and rounds to avoid rounding errors
        self.dailyMaintenanceMl = round(self.bodyweight * self.dailyFluids, 5)
        self.replace = round(((self.bodyweight * 1000) * self.dehydration / 100), 5)
        self.replaceLoss = round(self.replace + self.onGoingLoss, 5)
        self.requiredFluid = round(self.dailyMaintenanceMl + self.replaceLoss, 5)
        self.unroundedMlPerHour = round(self.requiredFluid / 24, 5)
        self.dailyDrops = round((self.requiredFluid * self.dropsPerMl), 5)
        self.dropsPerSec = round((self.requiredFluid * self.dropsPerMl/86400), 5)
        self.unroundedSecPerDrop = round(1/(self.requiredFluid * self.dropsPerMl/86400), 5)

        # saves questions Answer
        if self.mlVsSec == 0:
            self.ANS = math.floor(self.unroundedMlPerHour)
        else:
            self.ANS = math.floor(self.unroundedSecPerDrop)
        self.ANSml = math.floor(self.unroundedMlPerHour)
        self.ANSdrop = math.floor(self.unroundedSecPerDrop)

        # generates question text
        if self.dehydration > 0:
            self.question = {
                'intro': "A patient has been admitted for fluid therapy. The decision has been made to fully rehydrate the patient over the next 24 hours.",
                'question': "What is the required fluid rate to ensure this is the case? ",
                'otherinfo': f"(Give your answer rounded down to the nearest {self.unitArray[self.mlVsSec + 2]})",
                'units': self.unitArray[self.mlVsSec]}
        else:
            self.question = {
                'question': "Using the details listed calculate the daily maintenance fluid rate for the patient above",
                'otherinfo': f"(Give your answer rounded down to the nearest {self.unitArray[self.mlVsSec + 2]})",
                'units': self.unitArray[self.mlVsSec]}

#-------------------FLUIDS CALCULATOR CLASS END--------------------------------#

#-------------------ANASESTHETIC GAS CLASS START--------------------------------#


class Gasflow(Cat, Dog):
    def __init__(self):
        self.questType = "gasFlow"
        # initialises patient
        animalType = r.randint(1, 2)
        if animalType == 1:
            Dog.__init__(self)
        else:
            Cat.__init__(self)

        if self.bodyweight < 10:
            circuitSelect = r.randint(0, 2)
        else:
            circuitSelect = r.randint(3, 4)

        self.breathVolume = round(self.tidalVolume * self.bodyweight, 5)
        self.minuteVolume = round(self.respirationRate * self.breathVolume, 5)
        self.circuit = circuitsArray[circuitSelect][0]
        self.minFactor = circuitsArray[circuitSelect][1]
        self.maxFactor = circuitsArray[circuitSelect][2]
        self.minGasFlow = math.floor(self.minFactor * self.minuteVolume)
        self.maxGasFlow = math.floor(self.maxFactor * self.minuteVolume)

        # generates question
        self.question = {
            'intro': "Calculate the fresh gas flow rate requirement for the patient giving both the maximum and minimum flow rate",
            'maxgas': "Max. Flow Rate:",
            'mingas': "Min. Flow Rate: ",
            'units': "ml/minute", 'otherinfo': "(Give your answer to the nearest ml rounded down)"}

#-------------------ANASESTHETIC GAS CLASS START--------------------------------#


#-----------------START OF TABLET CALC----------------------------------#
class Tablet(Cat,Dog):
    def __init__(self):
        self.questType = "Tablet"

        # durg and course length details
        self.dose = r.randint(1, 3)
        self.interval = r.randint(1, 2)
        self.symptom = symptomArray[r.randint(0, len(symptomArray) - 1)]
        self.courseLength = ((r.randint(1, 3)) * 7)
        if self.interval == 1:
            self.wordDaily = "Once daily"
        else:
            self.wordDaily = "Twice daily"

        # generates animal
        self.species = r.randint(1, 2)
        if self.species == 1:
            Dog.__init__(self)
            if self.bodyweight < 10:
                self.medStrength = concArray[r.randint(0, 1)]
            elif self.bodyweight < 20:
                self.medStrength = concArray[r.randint(2, 4)]
            else:
                self.medStrength = concArray[r.randint(3, 5)]
        else:
            Cat.__init__(self)
            self.medStrength = concArray[r.randint(0, 2)]

        self.mgPerDose = round(self.bodyweight * self.dose, 5)
        self.unroundedTabsPer = round(self.mgPerDose / self.medStrength, 2)
        self.tabPer = self.unroundedTabsPer - self.unroundedTabsPer % 0.25
        # calculates number of tablets required
        self.unroundedANS = round((self.tabPer * self.courseLength * self.interval), 5)
        self.ANS = math.ceil(self.unroundedANS)

        self.question = {
            'intro': "A patient is being sent home with medication in tablet form. You have been asked to determine the number of whole tablets that are required for the complete treatment course.",
            'question': "How many tablets does this patient require? ",
            'otherinfo': "(The tablets can be broken into quarters and the dose rate must not be exceeded with any single dose)",
            'units': "tablets"
        }

#-----------------END OF TABLET CALC----------------------------------#


#---------------START OF LIQUID CLASS--------------------#

class Liquid(Cat, Dog):
    def __init__(self):
        self.questType = "Liquid"

        # durg and course length details
        self.dose = r.randint(1, 3)
        self.interval = r.randint(1, 2)
        self.symptom = symptomArray[r.randint(0, len(symptomArray) - 1)]
        self.courseLength = ((r.randint(1, 3)) * 7)
        if self.interval == 1:
            self.wordDaily = "Once daily"
        else:
            self.wordDaily = "Twice daily"

        # generates animal
        self.species = r.randint(1, 2)
        if self.species == 1:
            Dog.__init__(self)
            if self.bodyweight < 10:
                self.medStrength = concArray[r.randint(0, 2)]
            elif self.bodyweight < 20:
                self.medStrength = concArray[r.randint(2, 4)]
            else:
                self.medStrength = concArray[r.randint(3, 5)]
        else:
            Cat.__init__(self)
            self.medStrength = concArray[r.randint(0, 2)]

        # determines if (1) mg/ml or 2 (% solution)
        self.lType = r.randint(1, 2)

        # volume of liquid required for patient
        self.mgPerDose = round((self.bodyweight * self.dose), 5)
        self.unroundedVolPer = round(self.mgPerDose / self.medStrength, 5)
        print(self.medStrength)
        self.liquidPer = round((math.floor(self.unroundedVolPer * 10) / 10), 1)
        self.unroundANS = round((self.liquidPer * self.courseLength * self.interval), 5)
        self.ANS = math.ceil(self.unroundANS)

        # if percentage solution modify medstrength to percentage
        if self.lType == 2:
            self.percMedStrength = self.medStrength / 10
            print(self.percMedStrength)

        self.question = {
            'intro': "A patient is being sent home with medication in liquid form. You have been asked to determine the volume of liquid required to complete the full course of treatment.",
            'question': "What volume of liquid is required to complete the full treatment course?",
            'otherinfo': "(The total volume of liquid should be calculated to the nearest 1ml and the dose rate must not be exceeded with any single dose)",
            'units': "ml",
        }


#------------------END OF LIQUID CLASS-------------------#

#-------------START OF INJECTABLE CLASS -----------------#

class Injectable(Cat, Dog):
    def __init__(self):
        self.questType = "Injectable"

        # durg and course length details
        self.dose = r.randint(1, 5)

        # generates patient details
        animalType = r.randint(1, 2)
        if animalType == 1:
            Dog.__init__(self)
            if self.bodyweight < 10:
                self.medStrength = concArray[r.randint(0, 2)]
            elif self.bodyweight < 20:
                self.medStrength = concArray[r.randint(2, 4)]
            else:
                self.medStrength = concArray[r.randint(3, 5)]
        else:
            Cat.__init__(self)
            self.medStrength = concArray[r.randint(0, 2)]

        # determines if (1) mg/ml or 2 (% solution)
        self.lType = r.randint(1, 2)

        # injectable calculations
        self.mgPerDose = round(self.bodyweight * self.dose, 5)
        self.unroundedVolumePerDose = round(self.mgPerDose / self.medStrength, 5)
        self.ANS = (math.floor(self.unroundedVolumePerDose * 10)) / 10

        if self.lType == 2:
            self.percMedStrength = self.medStrength / 10

        self.question = {
            'intro': "While a patient is under anaesthesia you have been asked to administer an injection of pain medication.",
            'question': "Using the information given what volume of solution should be drawn up for administration? ",
            'otherinfo': "(Give your answer rounded down to the nearest 0.1ml)",
            'units': "ml"
        }


#---------------END OF INJECTABLE CLASS-----------------#

#-------------- TEST GENERATING ALGORITHM-------#
def tabletTestQuestion(data, i):
    question = Tablet()
    data.update({i: {
        'questType': 'Tablet',
        'ANS': question.ANS,
        'box1' : {
            'Weight': f"{question.bodyweight}kg",
            'Species': question.species,
            'Presenting Complaint': question.symptom
            },
        'box2' : {
            'Max Dose Rate': f"{question.dose}mg/kg",
            'Course Length': f"{question.courseLength} days",
            'Tablet Strength Available': f"{question.medStrength}mg/tablet",
            'Daily Doses': question.wordDaily
            },
        'question': question.question
    }})

def liquidTestQuestion(data, i):
    question = Liquid()
    data.update({i: {
        'questType': 'Liquid',
        'ANS': question.ANS,
        'box1' : {
            'Weight': f"{question.bodyweight}kg",
            'Species': question.species,
            'Presenting Complaint': question.symptom
            },
        'box2' : {
            'Max Dose Rate': f"{question.dose}mg/kg",
            'Course Length': f"{question.courseLength} days",
            'Liquid Strength Available': f"{question.medStrength}mg/tablet",
            'Daily Doses': question.wordDaily
            },
        'question': question.question
    }})
    if question.lType == 2:
        data[i]['box2']['Liquid Strength Available'] = f"{question.percMedStrength}% solution"

def fluidsTestQuestion(data, i):
    question = Fluids()
    if question.dehydration > 0:
        data.update({i: {
            'questType': 'Fluids',
            'ANS': question.ANS,
            'box1': {
                'Weight': f"{question.bodyweight}kg",
                'Species': question.species,
            },
            'box2': {
                'Dehydration': f"{question.dehydration}%",
                'On Going Losses': f"{question.onGoingLoss}ml/day",
                'Drops Per Ml': f"{question.dropsPerMl} drops",
            },
            'question': question.question
        }})
    else:
        data.update({i: {
            'questType': 'Fluids',
            'ANS': question.ANS,
            'box1': {
                'Weight': f"{question.bodyweight}kg",
                'Species': question.species,
            },
            'box2': {
                'Drops Per ml': f"{question.dropsPerMl} drops",
            },
            'question': question.question
        }})
def gasflowTestQuestion(data, i):
    question = Gasflow()
    data.update({i: {
        'questType': 'Gasflow',
        'box1': {
            'Species': question.species,
            'Weight': f"{question.bodyweight}kg",
            'Respiration Rate': f"{question.respirationRate}breaths/minute",
            'Tidal Volume': f"{question.tidalVolume}ml"
        },
        'box2': {
            'Circuit': question.circuit,
            'Minimun Circuit Factor': question.minFactor,
            'Maximum Circuit Factor': question.maxFactor
        },
        'minGasFlow': question.minGasFlow,
        'maxGasFlow': question.maxGasFlow,
        'question': question.question
    }})
def injectableTestQuestion(data, i):
    question = Injectable()
    data.update({i: {
        'questType': 'Injectable',
        'box1': {
            'Species': question.species,
            'Weight': f"{question.bodyweight}kg",
        },
        'box2': {
            'Liquid Concentration': f"{question.medStrength}mg/ml solution",
        },
        'ANS': question.ANS,
        'question': question.question
    }})
    if question.lType == 2:
        data[i]['box2']['Liquid Concentration'] = f"{question.percMedStrength}% solution"

def testGen(testType):
    data = {}
    if testType == "Tablet":
        for i in range(10):
            tabletTestQuestion(data, i)      
    if testType == "Liquid":
        for i in range(10):
            liquidTestQuestion(data, i)    
    if testType == "Fluids":
        for i in range(10):
            fluidsTestQuestion(data, i)   
    if testType == "Gasflow":
        for i in range(10):
            gasflowTestQuestion(data,i)
    if testType == "Injectable":
        for i in range(10):
            injectableTestQuestion(data, i)
    if testType == "Hazard":
        for i in range(10):
            qSelector = r.randint(1, 5)
            if qSelector == 1:
                tabletTestQuestion(data, i)
            elif qSelector == 2:
                liquidTestQuestion(data, i)    
            elif qSelector == 3:
                fluidsTestQuestion(data, i)
            elif qSelector == 4:
                gasflowTestQuestion(data, i)
            elif qSelector == 5:
                injectableTestQuestion(data, i)
    data.update({10: testType})
    return data