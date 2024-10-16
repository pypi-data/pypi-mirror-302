import re

"""
SAMPLE SHEET REGEXES
"""

EXPERIMENT_REGEX_STR = {
    "top_up": r"(?:_topup\d?)",
    "rerun": r"(?:_rerun\d?)"
}

SAMPLE_ID_REGEX_STR = {
    "sample_id_non_control": r"(?:PRJ|CCR|MDX|TGX)\d{6}",
    "sample_id_control": r"(?:NTC|PTC)_\w+"
}

SAMPLE_ID_REGEX_STR["sample_id"] = r"(?:(?:{})|(?:{}))".format(
    SAMPLE_ID_REGEX_STR["sample_id_non_control"],
    SAMPLE_ID_REGEX_STR["sample_id_control"]
)

LIBRARY_REGEX_STR = {
    "id_int": r"L\d{7}",
    "id_ext": r"L{}".format(SAMPLE_ID_REGEX_STR["sample_id"]),
    "year": r"(?:L|LPRJ)(\d{2})\d+"
}

LIBRARY_REGEX_STR["id"] = r"(?:{}|{})(?:{}|{})?".format(
    LIBRARY_REGEX_STR["id_int"],
    LIBRARY_REGEX_STR["id_ext"],
    EXPERIMENT_REGEX_STR["top_up"],                             # TODO - could a top_up/rerun exist?
    EXPERIMENT_REGEX_STR["rerun"]
)

SAMPLE_REGEX_OBJS = {
    # Sample ID: https://regex101.com/r/Z7fvHt/1
    "sample_id": re.compile(SAMPLE_ID_REGEX_STR["sample_id"]),
    # https://regex101.com/r/Z7fvHt/2
    "library_id": re.compile(LIBRARY_REGEX_STR["id"]),
    # https://regex101.com/r/Yf2t8E/2
    "unique_id_full_match": re.compile("{}_{}".format(SAMPLE_ID_REGEX_STR["sample_id"], LIBRARY_REGEX_STR["id"])),
    # https://regex101.com/r/Yf2t8E/3
    # Use brackets to capture the sample id and the library id
    "unique_id": re.compile("({})_({})".format(SAMPLE_ID_REGEX_STR["sample_id"], LIBRARY_REGEX_STR["id"])),
    # https://regex101.com/r/pkqI1n/1
    "topup": re.compile(EXPERIMENT_REGEX_STR["top_up"]),
    # TODO - add regex 101
    "rerun": re.compile(EXPERIMENT_REGEX_STR["rerun"]),
    # https://regex101.com/r/nNPwQu/1
    "year": re.compile(LIBRARY_REGEX_STR["year"])
}


"""
OrcaBus regexes
"""

# https://github.com/ulid/spec
ULID_REGEX_STR = r"[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}"
ULID_REGEX_OBJ = re.compile(ULID_REGEX_STR)

ORCABUS_ID_WM_PREFIXES = {
    "analysis": r"ana\.",
    "analysis_run": r"anr\.",
    "analysis_context": r"ctx\.",
    "state": r"stt\.",
    "payload": r"pld\.",
    "workflow": r"wfl\.",
    "workflow_run": r"wfr\."
}

ORCABUS_ID_WM_REGEX_OBJS = {
    "analysis": re.compile("({})?{}".format(ORCABUS_ID_WM_PREFIXES["analysis"], ULID_REGEX_STR)),
    "analysis_run": re.compile("({})?{}".format(ORCABUS_ID_WM_PREFIXES["analysis_run"], ULID_REGEX_STR)),
    "analysis_context": re.compile("({})?{}".format(ORCABUS_ID_WM_PREFIXES["analysis_context"], ULID_REGEX_STR)),
    "state": re.compile("({})?{}".format(ORCABUS_ID_WM_PREFIXES["state"], ULID_REGEX_STR)),
    "payload": re.compile("({})?{}".format(ORCABUS_ID_WM_PREFIXES["payload"], ULID_REGEX_STR)),
    "workflow": re.compile("({})?{}".format(ORCABUS_ID_WM_PREFIXES["workflow"], ULID_REGEX_STR)),
    "workflow_run": re.compile("({})?{}".format(ORCABUS_ID_WM_PREFIXES["workflow_run"], ULID_REGEX_STR))
}

ORCABUS_ID_MM_PREFIXES = {
    "contact": r"ctc\.",
    "individual": r"idv\.",
    "library": r"lib\.",
    "project": r"prj\.",
    "sample": r"smp\.",
    "subject": r"sbj\."
}

ORCABUS_ID_MM_REGEX_OBJS = {
    "contact": re.compile("({})?{}".format(ORCABUS_ID_MM_PREFIXES["contact"], ULID_REGEX_STR)),
    "individual": re.compile("({})?{}".format(ORCABUS_ID_MM_PREFIXES["individual"], ULID_REGEX_STR)),
    "library": re.compile("({})?{}".format(ORCABUS_ID_MM_PREFIXES["library"], ULID_REGEX_STR)),
    "project": re.compile("({})?{}".format(ORCABUS_ID_MM_PREFIXES["project"], ULID_REGEX_STR)),
    "sample": re.compile("({})?{}".format(ORCABUS_ID_MM_PREFIXES["sample"], ULID_REGEX_STR)),
    "subject": re.compile("({})?{}".format(ORCABUS_ID_MM_PREFIXES["subject"], ULID_REGEX_STR))
}
