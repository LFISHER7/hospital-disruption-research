from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    codelist_from_csv,
    Measure,
)

from codelists import *

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
    },
    index_date="2020-01-01",
    population=patients.registered_with_one_practice_between(
        "index_date", "index_date"
    ),
    AgeGroup=patients.categorised_as(
        {
            "0-4": "age >= 0 AND age < 5",
            "5-9": "age >= 5 AND age < 10",
            "10-14": "age >= 10 AND age < 15",
            "15-19": "age >= 15 AND age < 20",
            "20-24": "age >= 20 AND age < 25",
            "25-29": "age >= 25 AND age < 30",
            "30-34": "age >= 30 AND age < 35",
            "35-39": "age >= 35 AND age < 40",
            "40-44": "age >= 40 AND age < 45",
            "45-49": "age >= 45 AND age < 50",
            "50-54": "age >= 50 AND age < 55",
            "55-59": "age >= 55 AND age < 60",
            "60-64": "age >= 60 AND age < 65",
            "65-69": "age >= 65 AND age < 70",
            "70-74": "age >= 70 AND age < 75",
            "75-79": "age >= 75 AND age < 80",
            "80-84": "age >= 80 AND age < 85",
            "85-89": "age >= 85 AND age < 90",
            "90plus": "age >= 90",
            "missing": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0-4": 0.05,
                    "5-9": 0.05,
                    "10-14": 0.05,
                    "15-19": 0.05,
                    "20-24": 0.05,
                    "25-29": 0.05,
                    "30-34": 0.05,
                    "35-39": 0.05,
                    "40-44": 0.05,
                    "45-49": 0.1,
                    "50-54": 0.05,
                    "55-59": 0.05,
                    "60-64": 0.05,
                    "65-69": 0.05,
                    "70-74": 0.05,
                    "75-79": 0.05,
                    "80-84": 0.05,
                    "85-89": 0.05,
                    "90plus": 0.05,
                }
            },
        },
        age=patients.age_as_of("index_date",),
    ),
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    # ethnicity in 6 categories
    ethnicity=patients.with_these_clinical_events(
        ethnicity_codes,
        returning="category",
        find_last_match_in_period=True,
        include_date_of_match=False,
        return_expectations={
            "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
            "incidence": 0.75,
        },
    ),
    # IMD - quintile
    imd=patients.categorised_as(
        {
            "0": "DEFAULT",
            "1": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
            "2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
            "3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
            "4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
            "5": """index_of_multiple_deprivation >= 32844*4/5 AND index_of_multiple_deprivation < 32844""",
        },
        index_of_multiple_deprivation=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.05,
                    "1": 0.19,
                    "2": 0.19,
                    "3": 0.19,
                    "4": 0.19,
                    "5": 0.19,
                }
            },
        },
    ),
    CVD=patients.admitted_to_hospital(
        with_these_diagnoses=cvd_codelist,
        between=["index_date", "index_date + 6 days"],
        return_expectations={"incidence": 0.05},
    ),
    respiratory_disease=patients.admitted_to_hospital(
        with_these_diagnoses=resp_codelist,
        between=["index_date", "index_date + 6 days"],
        return_expectations={"incidence": 0.05},
    ),
    cancer=patients.admitted_to_hospital(
        with_these_diagnoses=cancer_codelist,
        between=["index_date", "index_date + 6 days"],
        return_expectations={"incidence": 0.05},
    ),
)


measures = [
    Measure(
        id="CVD_rate",
        numerator="CVD",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity", "imd"],
    ),
    Measure(
        id="respiratory_disease_rate",
        numerator="respiratory_disease",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity", "imd"],
    ),
    Measure(
        id="cancer_rate",
        numerator="cancer",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity", "imd"],
    ),
]
