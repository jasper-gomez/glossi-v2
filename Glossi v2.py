"""
Python model 'Glossi v2.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 30,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Probability to Wash",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "model_seed": 1,
        "time": 1,
        "discomfort_level_oily": 1,
        "oiliness_sensitivity": 1,
    },
)
def probability_to_wash():
    return if_then_else(
        float(np.random.uniform(0, 1, size=()))
        < discomfort_level_oily() * oiliness_sensitivity(),
        lambda: 1,
        lambda: 0,
    )


@component.add(
    name="Model Seed",
    limits=(0.0, 1000.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def model_seed():
    return 123


@component.add(
    name="Probability to Treat",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "model_seed": 1,
        "time": 1,
        "discomfort_level_dry": 1,
        "dryness_sensitivity": 1,
    },
)
def probability_to_treat():
    return if_then_else(
        float(np.random.uniform(0, 1, size=()))
        < discomfort_level_dry() * dryness_sensitivity(),
        lambda: 1,
        lambda: 0,
    )


@component.add(
    name="Atmospheric Factors 1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_exposure": 1},
)
def atmospheric_factors_1():
    return wind_exposure()


@component.add(
    name="Atmospheric Factors 2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"humidity": 1, "sweat": 1},
)
def atmospheric_factors_2():
    return humidity() + sweat()


@component.add(
    name="Moisturizing",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bath_intensity": 1, "leavein": 1, "conditioner": 1},
)
def moisturizing():
    return bath_intensity() + leavein() + conditioner()


@component.add(
    name="Dryness Sensitivity",
    limits=(0.01, 1.0, 0.01),
    comp_type="Constant",
    comp_subtype="Normal",
)
def dryness_sensitivity():
    return 0.5


@component.add(
    name='"Discomfort Level (Dry)"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dryness_level": 1, "target_dryness": 1},
)
def discomfort_level_dry():
    return float(np.maximum(0, dryness_level() - target_dryness()))


@component.add(
    name='"Discomfort Level (Oily)"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oiliness_threshold": 1, "dryness_level": 1},
)
def discomfort_level_oily():
    return float(np.maximum(0, oiliness_threshold() - dryness_level()))


@component.add(
    name="Moisture Rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "probability_to_treat": 1,
        "atmospheric_factors_2": 2,
        "moisturizing": 1,
    },
)
def moisture_rate():
    return if_then_else(
        float(np.random.uniform(0, 1, size=())) < probability_to_treat(),
        lambda: moisturizing() + atmospheric_factors_2(),
        lambda: atmospheric_factors_2(),
    )


@component.add(
    name="Hair Cleaning",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"shampoo": 1},
)
def hair_cleaning():
    return shampoo()


@component.add(
    name="Oiliness Sensitivity",
    limits=(0.01, 1.0, 0.01),
    comp_type="Constant",
    comp_subtype="Normal",
)
def oiliness_sensitivity():
    return 0.5


@component.add(
    name="Dryness Rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "probability_to_wash": 1,
        "atmospheric_factors_1": 2,
        "hair_cleaning": 1,
    },
)
def dryness_rate():
    return if_then_else(
        float(np.random.uniform(0, 1, size=())) < probability_to_wash(),
        lambda: hair_cleaning() + atmospheric_factors_1(),
        lambda: atmospheric_factors_1(),
    )


@component.add(name="Bath Intensity", comp_type="Constant", comp_subtype="Normal")
def bath_intensity():
    return 0.14


@component.add(name="Conditioner", comp_type="Constant", comp_subtype="Normal")
def conditioner():
    return 0.029


@component.add(
    name="Dryness Level",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dryness_level": 1},
    other_deps={
        "_integ_dryness_level": {
            "initial": {},
            "step": {"dryness_rate": 1, "moisture_rate": 1},
        }
    },
)
def dryness_level():
    return _integ_dryness_level()


_integ_dryness_level = Integ(
    lambda: dryness_rate() - moisture_rate(), lambda: 4.915, "_integ_dryness_level"
)


@component.add(name="Humidity", comp_type="Constant", comp_subtype="Normal")
def humidity():
    return 0.017


@component.add(
    name='"Leave-in"',
    limits=(0.0, 0.3, 0.01),
    comp_type="Constant",
    comp_subtype="Normal",
)
def leavein():
    return 0.265


@component.add(
    name="Oiliness Threshold",
    limits=(0.1, 10.0, 0.1),
    comp_type="Constant",
    comp_subtype="Normal",
)
def oiliness_threshold():
    return 2.5


@component.add(name="Shampoo", comp_type="Constant", comp_subtype="Normal")
def shampoo():
    return 0.647


@component.add(name="Sweat", comp_type="Constant", comp_subtype="Normal")
def sweat():
    return 0.035


@component.add(
    name="Target Dryness",
    limits=(0.1, 10.0, 0.1),
    comp_type="Constant",
    comp_subtype="Normal",
)
def target_dryness():
    return 4


@component.add(name="Wind Exposure", comp_type="Constant", comp_subtype="Normal")
def wind_exposure():
    return 0.066
