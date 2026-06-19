import proofread_eng_scifi.proof_01
import proofread_eng_scifi.proof_02
import proofread_eng_scifi.proof_03
import proofread_eng_scifi.proof_04
import proofread_eng_scifi.proof_05
import proofread_eng_scifi.proof_06
import proofread_eng_scifi.proof_07
import proofread_eng_scifi.proof_08
import proofread_eng_scifi.proof_09
import proofread_eng_scifi.proof_10
import proofread_eng_scifi.proof_11
import proofread_eng_scifi.proof_12
import proofread_eng_scifi.proof_13

modules = {
    "01": proofread_eng_scifi.proof_01,
    "02": proofread_eng_scifi.proof_02,
    "03": proofread_eng_scifi.proof_03,
    "04": proofread_eng_scifi.proof_04,
    "05": proofread_eng_scifi.proof_05,
    "06": proofread_eng_scifi.proof_06,
    "07": proofread_eng_scifi.proof_07,
    "08": proofread_eng_scifi.proof_08,
    "09": proofread_eng_scifi.proof_09,
    "10": proofread_eng_scifi.proof_10,
    "11": proofread_eng_scifi.proof_11,
    "12": proofread_eng_scifi.proof_12,
    "13": proofread_eng_scifi.proof_13,
}

registry = {
    "01": {
        "model": "random_00",
        "error_threshold": 0.05,
    },
    "02": {
        "model": "fomm_00",
        "error_threshold": 0.0005,
    },
    "03": {
        "model": "somm_00",
        "error_threshold": 0.0005,
    },
    "04": {
        "model": "fomm_01",
        "error_threshold": 0.0005,
    },
    "05": {
        "model": "somm_01",
        "error_threshold": 0.0005,
    },
    "06": {
        "model": "somm_02",
        "error_threshold": 0.0005,
    },
    "07": {
        "model": "fomm_02",
        "error_threshold": 0.0005,
    },
    "08": {
        "model": "somm_03",
        "error_threshold": 1e-8,
    },
    "09": {
        "model": "somm_04",
        "error_threshold": 1e-8,
    },
    "10": {
        "model": "somm_05",
        "error_threshold": 1e-8,
    },
    "11": {
        "model": "fomm_03",
        "error_threshold": 0.0005,
    },
    "12": {
        "model": "somm_06",
        "error_threshold": 1e-8,
    },
    "13": {
        "model": "somm_07",
        "error_threshold": 1e-8,
    },
}
