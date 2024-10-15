"""Package-wide code and data."""

TEST_DID = "LjgpST2rjsoxYegQDRm7EL"
SCHEMA_NAME = "bc-reg"
SCHEMA_TXN = 12
SCHEMA_ID = f"{TEST_DID}:2:{SCHEMA_NAME}:1.0"
SCHEMA = {
    "ver": "1.0",
    "id": SCHEMA_ID,
    "name": SCHEMA_NAME,
    "version": "1.0",
    "attrNames": ["legalName", "jurisdictionId", "incorporationDate"],
    "seqNo": SCHEMA_TXN,
}
CRED_DEF_ID = f"{TEST_DID}:3:CL:12:tag1"
CRED_DEF = {
    "ver": "1.0",
    "id": CRED_DEF_ID,
    "schemaId": SCHEMA_TXN,
    "type": "CL",
    "tag": "tag1",
    "value": {
        "primary": {
            "n": "...",
            "s": "...",
            "r": {
                "master_secret": "...",
                "legalName": "...",
                "jurisdictionId": "...",
                "incorporationDate": "...",
            },
            "rctxt": "...",
            "z": "...",
        },
        "revocation": {
            "g": "1 ...",
            "g_dash": "1 ...",
            "h": "1 ...",
            "h0": "1 ...",
            "h1": "1 ...",
            "h2": "1 ...",
            "htilde": "1 ...",
            "h_cap": "1 ...",
            "u": "1 ...",
            "pk": "1 ...",
            "y": "1 ...",
        },
    },
}
REV_REG_DEF_TYPE = "CL_ACCUM"
REV_REG_ID = f"{TEST_DID}:4:{CRED_DEF_ID}:{REV_REG_DEF_TYPE}:tag1"
TAILS_DIR = "/tmp/indy/revocation/tails_files"
TAILS_HASH = "8UW1Sz5cqoUnK9hqQk7nvtKK65t7Chu3ui866J23sFyJ"
TAILS_LOCAL = f"{TAILS_DIR}/{TAILS_HASH}"
REV_REG_DEF = {
    "ver": "1.0",
    "id": REV_REG_ID,
    "revocDefType": "CL_ACCUM",
    "tag": "tag1",
    "credDefId": CRED_DEF_ID,
    "value": {
        "issuanceType": "ISSUANCE_ON_DEMAND",
        "maxCredNum": 5,
        "publicKeys": {"accumKey": {"z": "1 ..."}},
        "tailsHash": TAILS_HASH,
        "tailsLocation": TAILS_LOCAL,
    },
}
INDY_OFFER = {
    "cred_def_id": CRED_DEF_ID,
    "schema_id": SCHEMA_ID,
    "nonce": "1234567890",
    "key_correctness_proof": {
        "c": "565827556",
        "xz_cap": "287165348434097",
        "xr_cap": [
            [
                "remainder",
                "24717",
            ],
            [
                "number",
                "133504566766407",
            ],
            [
                "master_secret",
                "10339928600136745",
            ],
        ],
    },
}
INDY_CRED_REQ = {
    "prover_did": TEST_DID,
    "cred_def_id": CRED_DEF_ID,
    "blinded_ms": {
        "u": "12345",
        "ur": "1 123467890ABCDEF",
        "hidden_attributes": ["master_secret"],
        "committed_attributes": {},
    },
    "blinded_ms_correctness_proof": {
        "c": "77777",
        "v_dash_cap": "12345678901234567890",
        "m_caps": {"master_secret": "271283714"},
        "r_caps": {},
    },
    "nonce": "9876543210",
}
INDY_CRED = {
    "schema_id": SCHEMA_ID,
    "cred_def_id": CRED_DEF_ID,
    "rev_reg_id": REV_REG_ID,
    "values": {
        "legalName": {
            "raw": "The Original House of Pies",
            "encoded": "108156129846915621348916581250742315326283968964",
        },
        "busId": {"raw": "11155555", "encoded": "11155555"},
        "jurisdictionId": {"raw": "1", "encoded": "1"},
        "incorporationDate": {
            "raw": "2021-01-01",
            "encoded": "121381685682968329568231",
        },
        "pic": {"raw": "cG90YXRv", "encoded": "125362825623562385689562"},
    },
    "signature": {
        "p_credential": {
            "m_2": "13683295623862356",
            "a": "1925723185621385238953",
            "e": "253516862326",
            "v": "26890295622385628356813632",
        },
        "r_credential": {
            "sigma": "1 00F81D",
            "c": "158698926BD09866E",
            "vr_prime_prime": "105682396DDF1A",
            "witness_signature": {"sigma_i": "1 ...", "u_i": "1 ...", "g_i": "1 ..."},
            "g_i": "1 ...",
            "i": 1,
            "m2": "862186285926592362384FA97FF3A4AB",
        },
    },
    "signature_correctness_proof": {
        "se": "10582965928638296868123",
        "c": "2816389562839651",
    },
    "rev_reg": {"accum": "21 ..."},
    "witness": {"omega": "21 ..."},
}
INDY_CRED_INFO = {
    "referent": "reft",
    "attrs": {
        "legalName": "The Original House of Pies",
        "busId": "11155555",
        "jurisdictionId": "1",
        "incorporationDate": "2021-01-01",
        "pic": "cG90YXRv",
    },
    "schema_id": SCHEMA_ID,
    "cred_def_id": CRED_DEF_ID,
    "rev_reg_id": REV_REG_ID,
    "cred_rev_id": "1",
}
