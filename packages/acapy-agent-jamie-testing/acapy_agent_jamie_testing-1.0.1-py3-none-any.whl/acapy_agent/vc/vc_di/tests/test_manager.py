"""Test VCDIManager."""

import pytest
from anoncreds import W3cPresentation

from acapy_agent.anoncreds.registry import AnonCredsRegistry
from acapy_agent.tests import mock

from ....core.in_memory.profile import InMemoryProfile
from ....core.profile import Profile
from ....resolver.default.key import KeyDIDResolver
from ....resolver.did_resolver import DIDResolver
from ....wallet.default_verification_key_strategy import (
    BaseVerificationKeyStrategy,
    DefaultVerificationKeyStrategy,
)
from ....wallet.did_method import DIDMethods
from ...ld_proofs.document_loader import DocumentLoader
from ...vc_ld.models.presentation import VerifiablePresentation
from ..manager import VcDiManager, VcDiManagerError

CHALLENGE = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
OPTIONS = {
    "options": {
        "challenge": CHALLENGE,
        "domain": "4jt78h47fh47",
    },
    "presentation_definition": {
        "id": "5591656f-5b5d-40f8-ab5c-9041c8e3a6a0",
        "name": "Age Verification",
        "purpose": "We need to verify your age before entering a bar",
        "input_descriptors": [
            {
                "id": "age-verification",
                "name": "A specific type of VC + Issuer",
                "purpose": "We want a VC of this type generated by this issuer",
                "schema": [
                    {"uri": "https://www.w3.org/2018/credentials#VerifiableCredential"}
                ],
                "constraints": {
                    "statuses": {"active": {"directive": "disallowed"}},
                    "limit_disclosure": "required",
                    "fields": [
                        {
                            "path": ["$.issuer"],
                            "filter": {
                                "type": "string",
                                "const": "GUBgy9MWF5KdmBjsC2wgTB",
                            },
                        },
                        {"path": ["$.credentialSubject.name"]},
                        {"path": ["$.credentialSubject.degree"]},
                        {
                            "path": ["$.credentialSubject.birthdate_dateint"],
                            "predicate": "preferred",
                            "filter": {"type": "number", "maximum": 20060710},
                        },
                    ],
                },
            }
        ],
        "format": {
            "di_vc": {
                "proof_type": ["DataIntegrityProof"],
                "cryptosuite": ["anoncreds-2023", "eddsa-rdfc-2022"],
            }
        },
    },
}
ISSUER_ID = "TNuyNH2pAW2G6z3BW8ZYLf"
VC = {
    "@context": [
        "https://www.w3.org/2018/credentials/v1",
        "https://w3id.org/security/data-integrity/v2",
        {"@vocab": "https://www.w3.org/ns/credentials/issuer-dependent#"},
    ],
    "type": ["VerifiableCredential"],
    "issuer": ISSUER_ID,
    "issuanceDate": "2024-07-09T14:44:36.380996753Z",
    "credentialSubject": {
        "name": "Alice Smith",
        "timestamp": 1720536272,
        "date": "2018-05-28",
        "birthdate_dateint": 20000709,
        "degree": "Maths",
    },
    "proof": {
        "type": "DataIntegrityProof",
        "proofPurpose": "assertionMethod",
        "verificationMethod": "TNuyNH2pAW2G6z3BW8ZYLf:3:CL:1230422:faber.agent.degree_schema",
        "proofValue": "ukgGEqXNjaGVtYV9pZNkvVE51eU5IMnBBVzJHNnozQlc4WllMZjoyOmRlZ3JlZSBzY2hlbWE6ODQuMjEuOTirY3JlZF9kZWZfaWTZPVROdXlOSDJwQVcyRzZ6M0JXOFpZTGY6MzpDTDoxMjMwNDIyOmZhYmVyLmFnZW50LmRlZ3JlZV9zY2hlbWGpc2lnbmF0dXJlgqxwX2NyZWRlbnRpYWyEo21fMtwAICvM6gcffsyHT8ycH8y_zJQIBGvMpMzHDsytSkYRfMzLzM7MqcyScMzUzLk9AlGhYdwBAQENzMDM8MyJG8yhzIwAzPx9zPEDzKnM5czVzOfMxMyFBMyCzOsPZcygzJ8qzKdmzPHMkMznzMLMpkllzO5kY8yceUZ_Qsz1zPxmzJvMjEoeLyrMy8yUNSkhzNXMg0vMgczXzPbMwVbM88yzLALMjsyxzI_Mq8ziHVjMh8z4zLUxZjPM6El5D8ycB8zqzMTMy0I4BFHM9sz2zJHMlMy0c8yECFbM7szUzN_M_szGzNs0TGcrzI7M98zyzPfMqDjM5k7Mn0vMlcz9bVjM62ZwIMyvO8zKzIhVdXrMs2DM9BbMr8yNYMy7zNHMkhvMsA53zMXMlGQ1PczpzM3Ms8yffcyEeDYIzJpjzKHM6syNMULMjczPaSlVzIZaMMyTK8zvzNHMo8zUPh7M0syufW0wzJHMolnMiC9Sa8y7zLk_G8yIUMzBzPLMlcyQYnfM9cy4QMz5Ckg1YEl9zMXM-xxGZ0xZD8zdzJ_M6cy1WGbMkkNLMsyiN1_MoDpuzNjM7WsdIMyTPFqhZdwASxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHbMwwLMoszPzLDMjsz4zN_Ms20ga17Mu6F23AFVCVluBkc_OMzvMsyAzJANzOUJfQvMlV3MnkzMj0RfzLpZzOXM12ZmzI7M9syHES8UNwjMiMzVzOQLcMz-zJ7Mn19szODM88znzMbMmVnMkczpzKbMyD7MvyHMy8y9zKFqE3tUdcyENyUCL8y8G1HM2cyZzPkBzO_MggLMiMzKzIbMxszkdMyVZ3UIzJ3M58zcbwVMzPDMwszjSszUEC9Ma8z_f8yVBczrCwPMmDfMylDMniZCzIx9bnogEsz4zK18zO3M3FUAdA7M3cyAG8zmaRTMncySIgszzKjM6SXM4szoe3wazNHMvBc2RczLzKjM2Aowc8zLR8ywzLvM_T_Mp3HMmCfMrczKGsyyzOlvzIxvBhxtCMykzM4KNithzM7MiDHMpBrM2szIzJA-UhHMvk8nzKvMqxIhDsytzM_Mp20jbHp4Fld8ccyRzNQEDGjMhVdVzMAiMQzMuVtUzMfMvGjM-cy0UsyIZMyXzLrM0GDMnnVhD03M4SJcWszBX8zuzOvMsszhzM1mzPQszIHMnAA5RMyhzP7MtMy0zMZzbyFRzP7MiSwczLXMml5BdyfMh8z7zIjMgsyZzLUzfUvM0MyAaszJzJ0YzPNhK8yPd8zJf8yUzL8rESnM3EI2zLbMzUTM-WTM6xYqzLLM_n4SeHfM36xyX2NyZWRlbnRpYWzAu3NpZ25hdHVyZV9jb3JyZWN0bmVzc19wcm9vZoKic2XcAQDMmAJ-zITM6czSElnMxMzCEsywa17MlWVEzP0SzNs1bGrMjszHX8zwB8zSJyRJzO9gXijMpsyWUScgcwxxzPHM9ULM6szPfCMHXcznAWQqbz4RzONpzJQKGsywTMzIaczazOtbzPMHNAEBzM5VzN7M3cy6zLzMmczYQUPM98z5zL3MsMykLsyQTmlvzLDMvzrM3sybzPHM6EgBzMPM9kx1zME3L1HMn8yCzNLM6BnMiiXMukXMlzjM9czvO0kizObM68ykzKPM78yyzJU5ccy4zLdQXynMx8yrFsy7zMoIzLhGPBTM08yPSMzUDwIXzKrMmkDM_MyqTFR0X8yGS2fMjsztecyNHXB1zPvMmSTMuEfM6czGUsyRzJbM_sykzNMXzJ1LasyVXDERzOoKWzUYGX0QzMoAzPsqzJXMpczdzOTM8CYrzNtczKTM7wtgNSARzNrMqHXMnlhQQ1IjzM1AUMzkfsyuSRcOJH7M2G4nzKNrOg-hY9wAIHXMx8yQzNDMpsyOzINHzIRADhkQJAQuzKvMrszTGsy2GgQWzLvMrUfM6SYwbzs",
        "cryptosuite": "anoncreds-2023",
    },
}

VP = {
    "@context": [
        "https://www.w3.org/2018/credentials/v1",
        "https://w3id.org/security/data-integrity/v2",
        {"@vocab": "https://www.w3.org/ns/credentials/issuer-dependent#"},
    ],
    "type": ["VerifiablePresentation"],
    "verifiableCredential": [
        {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                "https://w3id.org/security/data-integrity/v2",
                {"@vocab": "https://www.w3.org/ns/credentials/issuer-dependent#"},
            ],
            "type": ["VerifiableCredential"],
            "issuer": ISSUER_ID,
            "credentialSubject": {
                "birthdate_dateint": True,
                "name": "Alice Smith",
                "degree": "Maths",
            },
            "proof": {
                "cryptosuite": "anoncreds-2023",
                "type": "DataIntegrityProof",
                "proofPurpose": "assertionMethod",
                "verificationMethod": "JaAFqv91MMWh7Ne7aNPXCf:3:CL:1242241:faber.agent.degree_schema",
                "proofValue": "ukgKDqXNjaGVtYV9pZNkvSmFBRnF2OTFNTVdoN05lN2FOUFhDZjoyOmRlZ3JlZSBzY2hlbWE6NDIuODkuNTirY3JlZF9kZWZfaWTZPUphQUZxdjkxTU1XaDdOZTdhTlBYQ2Y6MzpDTDoxMjQyMjQxOmZhYmVyLmFnZW50LmRlZ3JlZV9zY2hlbWGpc3ViX3Byb29mgq1wcmltYXJ5X3Byb29mgqhlcV9wcm9vZoaucmV2ZWFsZWRfYXR0cnOCpmRlZ3JlZdwAIAEEzIFizO3MnzzMkDFNzK0UG8yCzN7MtEnM28yabszSGCskzMfMi8yoF1xcbSSkbmFtZdwAIMyKzOENzPzMmmnM-X3MzMyRzOHM9RvMzszTzK_M9ELMvFfMqGnM4EEmzL0MzKfMy0rM8sydp2FfcHJpbWXcAQDMusyxbzYxzMTMsszEOcyjzOBZzNA8Pl3MsUbMomXMqcz3zJA8zL7M2MzlzIDMnsz7zLPM4yEea3hqTU3M_syMzI45ZMy3zIjM5czmzIjMoMznzMZLD8zfEsyUzKHMmmg-CmAmzLJXTXpzzLBUJcymVSbMtgxdbEpZzI1ozJ1pzKYrAczgzMNBzIXM9mFSzIwCzONazLnMm21RFjs1zJjM4sz8BMz6F8yDzK5XzM3MsDcYZTtsQMyCzOsSzIXMx8ziExzM4MzvzIXM08zOcE_MpczUMXg8zPDMt8zNBcyyMsytKX0FzPPMlMzCDcyozPjMrnHMhEY_J2clzJE5zP9vzNjM9kHMlg_M9cyLzOh3c18BKczozNDMomPM-hLMmMzazM3M3VpAzK7Mpsz0YszkXic6NRxVzL9hzPRKbBPMx8zgzKx_zL89zMbMsjdfzJRwBw4OfxROzNTM7cyqBgkWzNNqb8y2zPfMozzMyszpOcyRzKQbOMyqTTTMj1ihZdwAOSnMgAPMymwYzJrMjsygCm7MkcztVwQnY8yBWXnMkE1xEXfM8syzIczVIMzOzMLMksyazN4cOmVjVxl3LRzM2VIdflnM-CrMuyZYzLIvdaF23AF_C3w7zJrMiMzHzJbM-Mz6YXxGzMvMo8z_f8zfTMyzFXItSMzkD8zdzP52zMpVaczFD3wpajjMkMyfUTHMisykzKrMu21DzIA2zO8czKQuzMpvzMNIG8zzzI_MpcyuFkzMrMzkaMz1zLYiX8y9NMylzLvM_FwUzN1fzMoDzL5UDQHM7hRdzKEVzNzMgX9ZchPMucyCfDMQzMLM0Mz8e8yYZjzM1czRdXbMg0ICLMzFzLrMy8zNzIVyWSnMr8zSzKp4zLfM53AGAcyZzJ_Mm8yYESLM-MyszOcZOMzSN1N7zN_M1szKUczPJczezKfMz2PMx8zOKkcezKxSzPXM18yiNxVMzOrMgMzJzK3M1szoTszczI0VRR5OSMzBzNXMucy6zL4aY8zAzKI8d8zezNfMkMyezMHM1D_Ml8zPzPhvzNbMixzMt8zvJszyzMtbaBnMth7MpMymBsy-zKVCW2bMpHPMqitAzOrMrczzzIAazNXMkczGzMgFWMyiP8y5ahZ8zOA9CgjM5MzVzK_MokTMiczLzJZrzP0ozKHMtMyYzK1-zKEwzLDM7MytLigRMsz9DszUzP5qzI9SGcy5zOI1R8y6Tm0wImhPLszlUMzPD0lnYkQyOzgsb8yMzMzMpczAZ8yeQcyozIrM3cy6BcyUAszzzIrMoyIVzL_Mv0p8zM7M-3nMrQnMpndwTsyvcczsH8zYzILM7EjM31kULszAzJ0nBjsbTMzgzNddzOrMxg7MjMyBzMLMjczczLfMg0xafi3MtMzuoW2EpGRhdGXcAErMv8zYzNUlYyBzWcyXZsyFzLBlzIrM2hcXzIJZzMDMusyWBGrMjcyiAgPMuCvM08yKZsykzMtfPMyCCwh_zNjM6sybFczgzPJBGMz8OszKUczezMzM88zZGcyQA1LMy8yqzNsBfMzCPyJyzKYvzL08sWJpcnRoZGF0ZV9kYXRlaW503ABKzPJ0zOc6LDTM6syUzLMAVsz_cczBzOpSDRxyzIl3L8zyzLFxCczBzPbMgRxYOsznzN_M61bMzczYzLFBLszpzIY2zNDM7szQeFTMjMyPzI4NbMyXZHPMz8y7A8ztMczRzNFmejfMsMzea8yRzLnM33-tbWFzdGVyX3NlY3JldNwASsyGUTvMh8zVGwPMysykKMy7awrMgcy_Zx3MsRs6zIJTzPbMkH_M0nxMPVBUzPjMtcz8zKDMu0jM6yJHWcylzO7M2iwrzJ5KRSEYeA_M6syZPE9AISoGaMyWQMyEWMyuH8z8WczLYszCzMypdGltZXN0YW1w3ABKzJDM_l4SzIjM8hbMgTzMuMySVik4OcyPYB5XJcybzMRBzI7M_syVzN_MxT7MlMywzMMsS2HMj0HM88zjzN7M4cyyzO0lzIM3VwIKzLDM2FN7YghVREklc1YvQMzHIszVUVrMxMz8zPohWGGibTLcATA4NVtazKLMy17MqszaW8z1zIoUzKPMyyHMyHrMlSouc1VnA8zpPndQKTpfDC_MhMzOYMzQA8zYzM7MiMyDzMTMsMyBCMy2zNZ8BRN9zMXMrRRrShHMuXVDzI1gYD5seRfMgsycXHfMjx_Mm8zUdBAnzPPMhW4mG0jM5RzMhsy5zJPM5EtkzLA3zKIvzPFdzN1iSczbeBDMhGRLzM_M9BJzzJHMy2kazMx8zKFdzJnM6gbM98yiUMyODnJfzKx9ZEBheCknMD5zzJx9zM1RzKfM7GHMgyrM-2UdzP3M73zM0wbMi8zXdBzM5UfMz054EMzWzPoxzLgbO8zOMEXMrirM8nLM6HUrd8zVzIzMpDAXIklKzNTMm0h9e8yyAMzOzI7MxzlxzJBLzM_M6zZYdi7M_H7Mq8yJzPHMlWHMq8zyzPjM6X4-YMyZajrMqsy2zKfM6UHM3MzFHMz7zOISzIEgzJ9zzILM0MzqzJXM51zM2l3My2YBzJgqzJcLanvMr8z4X8yVWyImEMzSzIDMqkdadsyWLX3MnCLM_8yfzI1LbszHzIBLzMluBsyPZxTMjAgmzOTM5MyRIcyNqWdlX3Byb29mc5GGoXWEoTDcAErM81xrFsyWYGnM-czSzJttEEVXzMfMpcz5zMlYzJDMvcyfMBDMh8zYzIrMlhDM6My7zPZHzOxzzItmAERFRSwofczCzPDMoczXN8yfO8zYKczYzJ0aOXTMhUbMiMyEzIcvAizMu8yqzNsQSMyNzMpvoTPcAErMzMy5zJw3X8yYzM05Rg3MmMzIzO7M5j_MhzgzzIjM2BPMoMy_zLXMpnRVzO8pYsz1zPDM8cz_M8zPY8ytLszpFcyiURfM8lxgzIDM5XYHPF3MucyOzN0qdzdJzNl8zI3M4HhdXszazKs0SxFTT6Ex3ABKzPjMzMyrR8yKH0Q4zOJLzPkLS8yQzIjMrcyMMWFEzMHMhHERzJdOzP0azIjMnMz9zOzMnlQUzIAPQwEcZcyTWgvM2lViUszzzM3MrRXM2szZzLI9OlhpCcz4zKUVIQEpLXF1QszufsyiOqEy3ABKzOvMpcybOMz_zJvMp8zNBw5JzNYFLHbM1H1QzPY1V8znzK7MkMzazNQHQ8z3JXPMsAxUzP_Mr8yrzNV3zKPM60NtzMVZzMjMtMyCV8zyzL_MjczyK8yvasyFzKTM31LMlTrMhFdvCl1rzIrMtVPMu8ztEaFyhaEy3AEqA8ztzIDM3MyST8yczI3Mj8yAzNNezNRRNnrM3czNzI_M78z5zLU1zPTMu8ymzP_M7syBQUzM8lB9zO3MkszYZszUS8zmMl4YMnzMgwzMtMzselPMyMyBzKRxXXrM5F3M3czhzN0VJAkhzLrMi1jM-syuHQPMrsyKzLrM8k7M1Mzjbkw4zIFXzI3MlszfzIfMki3MlszJzN_MuszgzIHMpsz9QMzoasyIcX3M_DR1zKPMwV3MgkLMiQtGzLPM88yaM8yozI9KT1A9Oi3M43nMz8yazIHMy3jMqszpzLnM0czCzPfM0wY9C8zcW8ywzOnMjMzVbcy8O8z8HwfMuMyQfAkxVyp6zJPMosz1ccz_HlU8RszbzJfMg8zzzPFUzII0OszcdMySzNnM2synzM8_R1bMmQpZzLkHzP7Mr8yBZMyLHszyzNPM28yFJi1FzPhAUsymQ8yAFMz_FkDMo8yRZUpISUpjAMzwzIXMoQ_M6DPMisztzPTMrFLMlsyVzPc3RlHMxcyNGHhpAczRzP7MnszEBVTMxCvMpyfMwMz0aMz_zPHMoQsHzLRqzMZGQ2rMr1jMpwZSZ8ySWsyczK4SHGTM1syfzPoDzIpszO2lREVMVEHcASoHzMnMnczZzPjMkcziPXF_Q8ziC8zezI1jKypQKkEkUczizOIYzLIKzLHMpn41aMzRzOnMhszYzM0izMPMp3vMnCpIcFEBHyfMxszCFnDM_2ISzLlyTkDMizkczPPMpCvMolM_zOVyzOXM-UZJzMzMq8zvKAsKV8yQzI7MtMyYFMy0zLPMwwtGzJlNbw8WzMrMhwIDzLVNUBDM4mMXR8yiVMzZzKdezL99VCpgdUfMksydzNbM-1lyK8z0RMy3zL3MzCLMrMzGzO7M_MzLMkTM98zUzMs3zIlWGRMtzK7M9cz0zPTMiMyoAXd-AMzIzNTMs3s4zIHMrFIQclYMzN_M68ywzPzM2czlJ2nM2sy7KMybEMzfzITMzAPMlczoFMy2LszgZ8zQzP3M9wLMtH8yzPYzRzdubVB9zN_Mysy3GsyicEfMwQg0C8yAzL1hzKLMo8zfzMjMyk3M90nM103Mw8z-XMyozPsjzPkxzP7Mg1_MwszgzI13zMfMg8zezLDMh8zhzMhOzPQ_S8y0zNZTzPzMvDXMgcyZJFNdJsy_zLbMj8zgYczXzPtizIAZbGbM48ydBADMphbMzszvZ3bM2cy7oTHcASoIzNHM2MyqzP7MkShNzLLMsMz6zLDM3sylzInMk3NtzLVEzKTMiznMpFsKZXkQKEcZzOd8zO58zKkAF0XMi0tKzKUfzJFCzP7M58z4UCzM4AFnzPrM6kjMuSfM1yTMyxQDJCvMo8y-zKAZzKjMqSVwzNPMwFpdcczpzLNwUiZezOtNHBHM7Mz_LMyFecytzO7MwTtUA8y-KMz7zMrMkcyizM_M2F3MrsyPT8zLE1JozOR2zOjMwMyzAWXMyWjM9MzizLkFEszDzJJASCvMzU_Mz8zczIwjzKVHzINtzIHMi8zAecyyHszRAMzsJcyUPFhTzIbMvsyizNZwzJrM_8zTzLzM7cycf8zvzLp6KjxFzJ7M9cyNFn4wDcy4OMzmzIBNCszVzKnM_mLM3HvM637M3syczNLMp8zizOjMswXMlsyOzNPMyVF4IRDMhmrM5MzJzPzMisy5VmVFzOVAeMz3zI7M-8zTzPLM_8zlzMLMkHfM_XdpzInM6B0mzOknVUoeGwTMyicpzJJ7YjU2KMyKFcyAzIYrVsyTJszuzOfM_SLM5RzMp8zMQmp8zNDM3MylI8yvM8yeYWvMisz5zJtec8y3zMLM38z0oTDcASnMqjEHEzlfzMNqFl7M88z3zIUqzJNrzLt5zJ08dzzMkTnMnsyQzPkLzPnM1El3zOMCzOHMg2jMjX0TzPRPzNDM6sy_F1_M4czozPo1zK08XBjMvszIzOIvScziV0vMuBlfzOEfb8yESMzjMsy-BRbM1Mz3zJc6zKZ8zLXMyczGzPzMrjFezLLMl8zWzObMj8zUzPxcKsz8Isy-zIFiPztcPXjMrWbMpWHMxQDMkmPMt8yhEDlPAVlIzLwCGczpzJ5BBQ_M_8zezIIfzKUozKTM-czfzJA-zKnM1MyVWSXM2nfMtsyRWczuzKnM2cyCzPvMwilfzNHMnCzM0Mz3zJ0SKsySHczlfMzSe8z1zJgHzIvMzE0oXsy6U8yvzKdPLC9ezIBWzOnMwszszIzMzMzBzKLMgcyme8ybCszhzOjMzszkdszuWMyRzMo6zNvM7zIhzO3MzX03zMfMt0FLzIodQAUKzLpwbMzFzOIWzNsiXjJgzKg2IMyLzPrMg8ylWjrM6H_MmwzMqczCJcypUTpMzKnMhsyHzJbMkMzWzO3MuGPM-8yLzL3M6szRzJ1xI8ztzIUuE8yTzL96eCwqW1IjUXzMmMyloTPcASoGzO7M9XNkesy-zMZqd8yPHzRMORjMmcytKVNBzPbMo1przMRszKPM5GU1zJ3MjMywN0AfTcz6f3TMzMzGCszhPcyhAcy8SndgNszOKsz5zJYUaGkzLncxzPUszOdgzOR_zMHMjcyBQ8y2ORhQzKpXzIfMicywZhRJEEolWMynzOMdcxA9zMEtzJ1SzLLM_MyALyzMsszlzPkiGczszJ5qE8y4zOzMiyrMq17MvlcfzNbM5ARzzNkfHS_MugdyT8yfzPB-zKXMvTHMoxDM3A_MlsyhIMz7dczFNsyUecy8zL3M8FrM2cyXzOPMwMzhRgEcZkXM9szpU8zHVwrMz8yzNDMSWGvMvszWGMytzJRTBF3M8cyyzI8gzO3M2BEezIs6zPE5zLsBzK59eAp0zOseaMyNzMLMiBhaGMz5zIXMy8zIYBxuBTcUTA_MkAZsLszpzON1aFVeFznMv8zFAjJUFirMlszxzIHM3syuawgMXsyjVxFhCEsizKwrzMcyOn52zL3MokDM0TDM0sylzOTMtBrM9TnMpMzkzITMtczqzO3M_knMp8zWzMjM1MzsfV-ibWrcAErM8nTM5zosNMzqzJTMswBWzP9xzMHM6lINHHLMiXcvzPLMsXEJzMHM9syBHFg6zOfM38zrVszNzNjMsUEuzOnMhjbM0MzuzNB4VMyMzI_Mjg1szJdkc8zPzLsDzO0xzNHM0WZ6N8ywzN5rzJHMuczff6VhbHBoYdwBXQLMsHJpC8ysLczrGsziQEXMvkY6EyUyzPMCzInM8syWzMxTO8yCdxtozITMssydzMfM7syNPzRSCMzHzILMs3XMlnIzzNfM2WfMvczFzMBfzPxezJwdzKbMigJwzJnM8xFxzKjMuxNxZ8zJzNrM68yOL3TMriTMo3MrzKrMqszkK8zPOXkEzMPM_szEzLDM3MzizLnMxzovzJXMrXpMNMyczPBFzL3MhsyoHcyxWcyNzMDM3syrTMzkeg1wzNnM_MyHBszMdcy2zM49dHsTb8zJzPnMq8zjDkrM8316f8yCbsy4YcygzIHMmijM0MyEZsyzzL8GJ1t-S8ynBsz7D2ILbgTMwkxVaCXM2MzEzNXMjR7M5sykzMstJszOQBnM8nsWzPsqbVfMlDrM_8zSzOcgHsy9zMnMjGbMgcy4zJXM-GnM3GpnNHB-zNdfZUnM18yMzMA5zJLMk1ETci3MqnktzPR-zPtuPTlxIMzbLCDM-My0zNpbDcyBIAQpzPciImVcR2BNU8y9csz5zME_zPnMssy3zKTMpszHzLnMvxlvP8y0zNjM3nrMilotzLrM91bMpMyeESvMzRNszPpSzOxMF8yZFczjzJbMisygzMxFQDnMksytzMNHzItvEMypzNBgNR7Mwsz-zMQuzPB4c3AePV4ozOXMrMy9zK9nzKkcYcyVdDB6oXSFoTLcAQECS3crzL45zNbMgUxzY31AC8zHzL7MhnVAClB7JMy3WhzMjMzOzKHM4nnMhszQzNQYzPF5zJzM1syxzJzM9SPMoU7MrQrMoHbM1QLMisy_bczBfszqTMyizPvMylVubMyvzI3MrczXIWYOJ8zxzLfMkMzAEMyDHT3Mrg12HDk-zOTM_8z6C8yWUnPM38zDzLQsNcz_A0c2YczRKWzMu3fMsMyKzPnMw8yJzIrM8ivM88zcJcz8zI5wR8y_O8ygIMyTzJ1wG2lbHsy7zIIyGSpdT8zlYGMnfQYszKhFzOLMrgfMhSPMi8zeOF9ce28sIXLMnGnM9QTMgTJMdsyJzIxdzP4yDXY4zIpozJ10zNfMwMzBzJTMhMybzLzMjsyUSXNrzKpMG8z2fcyqzN7MsnXMi1p2J8yazINLzLPM_SlNzNMwLRldzNFtV8zUFcyGX8zpADxwc8yWzP_MmT_Mu8z1ZDxxM3NGzIx6zI3Mk8yiUMzxzLdszOB5oTHcAQBDc8zGzNhWK8zBORvMk3fM7DVxzM7Mi8zkzINTzJLMn8z9L39MzN4KbcyQBsypzPLMvsy6SMzLzNXMjx1ZP8zAzMTMm8zNKU9bUsy9GczTzL7MqsysKcyZUTwle3rMpczHeMyczOh0S8z5WcyGNG3M8MyGzJ_M3FZazOTM7y_M98zIVTJxPszyEy7M-mnM0sztzKDM4Cw0am1ECjTMzzAeVAXMtcymzNNmAszZMMyxzJ8BzI9VW8ySTR1zzKo8zNJJzJd-UGdTzKHM3WPM9MzDEszdfwrMk8y9S8z7zIw8zNRTAcyKEgp-zKZTzM_Mxn9YIcyENMzMzLnM68yxzNtxSxZPzMFONcyNzKg-zKIseEccJlvM6ytnzOjMmcztPRnM9CdYYcylM8zmzM_MxnbMpczEzNh-zOJQBhFdfczHFE3M-MyMD1VEzOEDCnh9zNI2Fz5TS8z0zNfMj0dzzPfMw1zMsEPMjcyEzKjMlCFEzK09bsz-oTDcAQECZFLM-gA1ay9GY3HM_g4cTnbMtmHMzxnMxcz7d8zzzLzMoGzM7MzrMczDBsyMOMy3zKPMjcy0P2TM2hlTBQnMo1XMuAHM1HFIzMPM9szLZsztf29rG8y2IjE1QGDMhMz9OFfMpsz1zP9ZzNLMkHTM4czZfXfM9CXM4gvMq33M4095zK01MAQBzMHMu3bMsMzKzOnMtVsWMhPMxzLMonHMyQbMl27M0wjM98zHNF5WIMy4KMzHzOHMsxXMlszfzJPMrcz0zObM28zgzPXMw8yMzKVTMwnM9y7M9Mz0zPPMpVnMiczKHDPMi8yazK_MoQjM8cybCGfMzj4RzLjM2zI7zNjMuArM2HZQzPkOzNLMskTM6cyCzMpUzNQxzKldIsz2THnM18z6JMz_J33M0czdWmU4NczozJHMhQvM6BhraczKWcyWzPggVz4_zJ4BJh0fzLXM2szdGMzWzMp2Lih-Ccy8zOTM7czEzN3MyszXzNHMoszCzOvMhsyozMBbzJhPEmGlREVMVEHcAQECWMzHHczNzJbM7czIRlTMkHUTI8zXzJ7M9FpDNMybNSHMjMyVzNwlzPPMjsy-YB8HzMQHJT7MsMy0zPASzPMXzIjM7syYcmPMu8yuDsyqzIE-zKMfzKrM6StBWThHI8yZzOVJRVvM5zTMrkMtMszVETXMgczYVTMaWGxGzKbMiDcizJYFGsyRzKVLzNrMmcyuSxLM-RV8zJ3M_GfMz8y2MsyyzK1czNTM2czazPFGGxUVzJ3M2DsjzIfM9RvMu8yAB8yGQEpNb8zQzIjMqylLzKnM2TwYzNgZzNUzzLpdzJQoB8yZzMo3PQbMni7MwlIlzOzMx2vMnHHM4gzMm8yCXMzEQVPMocyozL47PGfM7x1ZeMyfzLtZzITM4xhXzLLM1MyIzLIjzNHMyMyEzPxnXsyiQ3vMv8zPzJ8dzL5fzJPMgERkzK3MvXHM8MyNzMlNzO3MjXMSzK1wzNDM5nvMilXMixjMo8yxFHIjzMLMhypmzKzMgUw3zOQOzJhabcz7oTPcAQB2ejzMpcz3zNTMm0DMwWVJRmR9WnzM18zSzJRpzN8uzODMyczDzO8mbMzyzJQDMjLMwn3MsMyFzIfMlcyzYszlPCoEzO_MgcysW1fMoBjMzRITXhfMjMz1T2LMkcyJzKnM0BDMwMyeIszyzILM8sz1H8y3zKDMv8zHG2TM7cyjb8zqVsygzPgSzJzMusyVzKfMyMyxHMzGVWTM_A_M-sy8zNBYzIXMq8yezJ1nzKQvKMzKUjQ7zK9RzKpGzNxuVTFEzMDMxCI8zLNLzLRHzKFYWszpzOjMnCAHzIhrzNcJzLnMiczjzKcIIGRZzPnMgnZuP8ypQWwTzNJYWMz7zPUlW8zpRjDM9cz9OCTMmsyRAcy2M8zVH8yqI8yKQ0wgzKfM9szVUjPMh1JjBQvM5SrMnsypzMFozNnMssywzKbMgil7zN58zJQ0UVdSzK0ATMziClXMwAAGUcyDzI92GszpzJVbAsyzzMUdzIljH1XMo1M9zOI0fcz8zOHMmsyeZsz4qXByZWRpY2F0ZYOpYXR0cl9uYW1lsWJpcnRoZGF0ZV9kYXRlaW50pnBfdHlwZaJMRaV2YWx1Zc4BMhomr25vbl9yZXZvY19wcm9vZsA",
            },
            "issuanceDate": "2024-07-10T13:32:18.596054178Z",
        }
    ],
    "proof": {
        "type": "DataIntegrityProof",
        "proofPurpose": "authentication",
        "verificationMethod": "JaAFqv91MMWh7Ne7aNPXCf:3:CL:1242241:faber.agent.degree_schema",
        "challenge": "10275921379803826423",
        "proofValue": "ukgOBqmFnZ3JlZ2F0ZWSCpmNfaGFzaNwAIAl7Bsy4zOAyNxZ9bsySX1fMh8zgWiRLBczrIVXMy8y3B8zuGczzzIrM6MzXzLGmY19saXN0ltwBAMy6zLFvNjHMxMyyzMQ5zKPM4FnM0Dw-XcyxRsyiZcypzPfMkDzMvszYzOXMgMyezPvMs8zjIR5reGpNTcz-zIzMjjlkzLfMiMzlzObMiMygzOfMxksPzN8SzJTMocyaaD4KYCbMsldNenPMsFQlzKZVJsy2DF1sSlnMjWjMnWnMpisBzODMw0HMhcz2YVLMjALM41rMucybbVEWOzXMmMzizPwEzPoXzIPMrlfMzcywNxhlO2xAzILM6xLMhczHzOITHMzgzO_MhczTzM5wT8ylzNQxeDzM8My3zM0FzLIyzK0pfQXM88yUzMINzKjM-MyuccyERj8nZyXMkTnM_2_M2Mz2QcyWD8z1zIvM6HdzXwEpzOjM0MyiY8z6EsyYzNrMzczdWkDMrsymzPRizOReJzo1HFXMv2HM9EpsE8zHzODMrH_Mvz3MxsyyN1_MlHAHDg5_FE7M1MztzKoGCRbM02pvzLbM98yjPMzKzOk5zJHMpBs4zKpNNMyPWNwBAQJkUsz6ADVrL0Zjccz-DhxOdsy2YczPGczFzPt3zPPMvMygbMzszOsxzMMGzIw4zLfMo8yNzLQ_ZMzaGVMFCcyjVcy4AczUcUjMw8z2zMtmzO1_b2sbzLYiMTVAYMyEzP04V8ymzPXM_1nM0syQdMzhzNl9d8z0JcziC8yrfczjT3nMrTUwBAHMwcy7dsywzMrM6cy1WxYyE8zHMsyicczJBsyXbszTCMz3zMc0XlYgzLgozMfM4cyzFcyWzN_Mk8ytzPTM5szbzODM9czDzIzMpVMzCcz3Lsz0zPTM88ylWcyJzMocM8yLzJrMr8yhCMzxzJsIZ8zOPhHMuMzbMjvM2My4CszYdlDM-Q7M0syyRMzpzILMylTM1DHMqV0izPZMeczXzPokzP8nfczRzN1aZTg1zOjMkcyFC8zoGGtpzMpZzJbM-CBXPj_MngEmHR_MtczazN0YzNbMynYuKH4JzLzM5MztzMTM3czKzNfM0cyizMLM68yGzKjMwFvMmE8SYdwBAENzzMbM2FYrzME5G8yTd8zsNXHMzsyLzOTMg1PMksyfzP0vf0zM3gptzJAGzKnM8sy-zLpIzMvM1cyPHVk_zMDMxMybzM0pT1tSzL0ZzNPMvsyqzKwpzJlRPCV7esylzMd4zJzM6HRLzPlZzIY0bczwzIbMn8zcVlrM5MzvL8z3zMhVMnE-zPITLsz6aczSzO3MoMzgLDRqbUQKNMzPMB5UBcy1zKbM02YCzNkwzLHMnwHMj1VbzJJNHXPMqjzM0knMl35QZ1PMoczdY8z0zMMSzN1_CsyTzL1LzPvMjDzM1FMBzIoSCn7MplPMz8zGf1ghzIQ0zMzMuczrzLHM23FLFk_MwU41zI3MqD7Moix4RxwmW8zrK2fM6MyZzO09Gcz0J1hhzKUzzObMz8zGdsylzMTM2H7M4lAGEV19zMcUTcz4zIwPVUTM4QMKeH3M0jYXPlNLzPTM18yPR3PM98zDXMywQ8yNzITMqMyUIUTMrT1uzP7cAQECS3crzL45zNbMgUxzY31AC8zHzL7MhnVAClB7JMy3WhzMjMzOzKHM4nnMhszQzNQYzPF5zJzM1syxzJzM9SPMoU7MrQrMoHbM1QLMisy_bczBfszqTMyizPvMylVubMyvzI3MrczXIWYOJ8zxzLfMkMzAEMyDHT3Mrg12HDk-zOTM_8z6C8yWUnPM38zDzLQsNcz_A0c2YczRKWzMu3fMsMyKzPnMw8yJzIrM8ivM88zcJcz8zI5wR8y_O8ygIMyTzJ1wG2lbHsy7zIIyGSpdT8zlYGMnfQYszKhFzOLMrgfMhSPMi8zeOF9ce28sIXLMnGnM9QTMgTJMdsyJzIxdzP4yDXY4zIpozJ10zNfMwMzBzJTMhMybzLzMjsyUSXNrzKpMG8z2fcyqzN7MsnXMi1p2J8yazINLzLPM_SlNzNMwLRldzNFtV8zUFcyGX8zpADxwc8yWzP_MmT_Mu8z1ZDxxM3NGzIx6zI3Mk8yiUMzxzLdszOB53AEAdno8zKXM98zUzJtAzMFlSUZkfVp8zNfM0syUaczfLszgzMnMw8zvJmzM8syUAzIyzMJ9zLDMhcyHzJXMs2LM5TwqBMzvzIHMrFtXzKAYzM0SE14XzIzM9U9izJHMicypzNAQzMDMniLM8syCzPLM9R_Mt8ygzL_MxxtkzO3Mo2_M6lbMoMz4EsyczLrMlcynzMjMsRzMxlVkzPwPzPrMvMzQWMyFzKvMnsydZ8ykLyjMylI0O8yvUcyqRszcblUxRMzAzMQiPMyzS8y0R8yhWFrM6czozJwgB8yIa8zXCcy5zInM48ynCCBkWcz5zIJ2bj_MqUFsE8zSWFjM-8z1JVvM6UYwzPXM_TgkzJrMkQHMtjPM1R_MqiPMikNMIMynzPbM1VIzzIdSYwULzOUqzJ7MqczBaMzZzLLMsMymzIIpe8zefMyUNFFXUsytAEzM4gpVzMAABlHMg8yPdhrM6cyVWwLMs8zFHcyJYx9VzKNTPcziNH3M_MzhzJrMnmbM-NwBAQJYzMcdzM3MlsztzMhGVMyQdRMjzNfMnsz0WkM0zJs1IcyMzJXM3CXM88yOzL5gHwfMxAclPsywzLTM8BLM8xfMiMzuzJhyY8y7zK4OzKrMgT7Mox_MqszpK0FZOEcjzJnM5UlFW8znNMyuQy0yzNURNcyBzNhVMxpYbEbMpsyINyLMlgUazJHMpUvM2syZzK5LEsz5FXzMncz8Z8zPzLYyzLLMrVzM1MzZzNrM8UYbFRXMnczYOyPMh8z1G8y7zIAHzIZASk1vzNDMiMyrKUvMqczZPBjM2BnM1TPMul3MlCgHzJnMyjc9BsyeLszCUiXM7MzHa8ycccziDMybzIJczMRBU8yhzKjMvjs8Z8zvHVl4zJ_Mu1nMhMzjGFfMsszUzIjMsiPM0czIzITM_GdezKJDe8y_zM_Mnx3Mvl_Mk8yARGTMrcy9cczwzI3MyU3M7cyNcxLMrXDM0Mzme8yKVcyLGMyjzLEUciPMwsyHKmbMrMyBTDfM5A7MmFptzPs",
        "cryptosuite": "anoncreds-2023",
    },
    "presentation_submission": {
        "id": "bd3db08f-29b0-4f62-843b-91919f331d19",
        "definition_id": "5591656f-5b5d-40f8-ab5c-9041c8e3a6a0",
        "descriptor_map": [
            {
                "id": "age-verification",
                "format": "ldp_vc",
                "path": "$.verifiableCredential[0]",
            }
        ],
    },
}


@pytest.fixture
def resolver():
    yield DIDResolver([KeyDIDResolver()])


@pytest.fixture
def profile(resolver: DIDResolver):
    profile = InMemoryProfile.test_profile(
        {},
        {
            DIDMethods: DIDMethods(),
            BaseVerificationKeyStrategy: DefaultVerificationKeyStrategy(),
            DIDResolver: resolver,
        },
    )
    profile.context.injector.bind_instance(DocumentLoader, DocumentLoader(profile))
    yield profile


@pytest.fixture
def manager(profile: Profile):
    yield VcDiManager(profile)


@pytest.mark.asyncio
async def test_assert_no_callenge_error(manager: VcDiManager):
    with pytest.raises(VcDiManagerError) as context:
        await manager.verify_presentation({}, {"options": {}})


@pytest.mark.asyncio
async def test_assert_verify_presentation(manager: VcDiManager, profile: Profile):
    profile.context.injector.bind_instance(
        AnonCredsRegistry,
        mock.MagicMock(
            get_schema=mock.CoroutineMock(
                return_value=mock.MagicMock(
                    schema=mock.MagicMock(
                        serialize=mock.MagicMock(
                            return_value={
                                "issuerId": ISSUER_ID,
                                "attrNames": [
                                    "degree",
                                    "name",
                                    "date",
                                    "birthdate_dateint",
                                    "timestamp",
                                ],
                                "name": "degree schema",
                                "version": "68.37.38",
                            }
                        )
                    )
                ),
            ),
            get_credential_definition=mock.CoroutineMock(
                return_value=mock.MagicMock(
                    credential_definition=mock.MagicMock(
                        serialize=mock.MagicMock(
                            return_value={
                                "issuerId": ISSUER_ID,
                                "schemaId": "1242274",
                                "type": "CL",
                                "tag": "faber.agent.degree_schema",
                                "value": {
                                    "primary": {
                                        "n": "110191895107383177944225186787127045472400456419044508847920073749118325816882879555888693590503408107531218246551508200778858813446764597252042460295740219285296989541107769089502181778576777417930436325553990675031577262316859960188786027427415918907113489291521324039356114616863101480866513302357191568489145237650236954578848085540776058357840327446186761324850043360872510240168860114128657413033422322367730714244593033343815255367880227269514752281182456165390304117532268729405376542376337985308310279351286237047011259755660096523481882637528390140070572293678914392133356847907443964699396666368223294158061",
                                        "s": "9415812539608195450966883098870652296916491635505203853080983952632805384302967432306788150605939803147875077062094749099736966082292346688785945337831356656890556951983186155154365222554857316130536164238857088110797546973073757951768643832909466949503368156244645826883930998004092294090171380523954224832439522626754713977466892117127635439861663437421962242296372559287964629293301712321588335521469805244310171886131183734977508209622245349508899886419257943124600270414702700150921447687226557458680951807835253145114264110732291146813141269571018474399690170085303553149912953395770110046436238930438812780147",
                                        "r": {
                                            "birthdate_dateint": "39968681640304788380009477273748351837529664198759676077165379337792646675901616432152370797900826515094147804138445249213613945496792933661400605498715980120831712924000357777147499418810050923414071460841739245157420435453468918475700941287524373324079549579873246517784186882218530939272891114746579591872034727864365855842228114509998007945460010480245507010064392110362136591952150320820422225826544285688677068642300714078641169340591902569248592823824054227933825730852985690007682552923384746004484874059862968040467406436797474876079422807683482900156405231629390843729772887675489043282470807407031205186969",
                                            "date": "1189483679228280739072650972354053068606455987118485184085207434597201188158334235777355692068087062063721870127753534657818335769737924323208415920434077874887496282538032440486476302782516445945959644735720202525994434469144049628428271543868582987595621454107048590112351992445017094207270819619996701213546548131486236291413202271720647291688756231888188593794699964380031588638888843772851461391755221206371940247603348559507718057920345380550594583486893575953718560696958190724499821774481967602504818394556262808918356126374081669920344874855870303258253201308390418654588788321421245107716899898452672677669",
                                            "degree": "7930507600973622255761968698285828306846788291380201483787889093576185243433070380250482080700646211095178134232253270069460369492303935894012408118127081015494559256719242506733590055152439637360319677447051969350390638377492011800932771226273035358153040455317319159092480932337395314046192165987582330687751669998427678060271101315462477794016231639142468258481489055468781240927905148904953855558036223028111290216890655943559980456204339868018478633494472724669957163721224817260017913056937034080193667933454564153001308165996679854735603451224195324968916426779531862123459043377650779177644556309703126058569",
                                            "master_secret": "276481248076029901397915904197571939766835573218052607192738620704710670905748562925445909482694999303080385244124333488797597869947177554955868568791587429441803954589662661470453559603193697529455695636193068394109938416082954992003652270737665467573503772195889460315616035410445104017129549757818399000451038212677658874397388131875030264607848961441095008175483303770912033940379028110558590125358672540783519319152844457014577027814244423449014637405165845051430105495276716743166413876676529214061455612429316323214502293979149015655581759299623912651153921930483011898615547608936905586870150072549489722497",
                                            "name": "82868656041023829484169603686526910742809130312561664067502441442293881789487387499604367473067725155834966664040618821809499511114213661657225202206321891616189181748382445256076664775972124872336589185892368887947537027000430124719570575062210504764164198906984696516109885071145245277063304337918433238788453702459065343194907264612324316538889460640366702448456177503504044952464912882387589287029922982523474901886018581567364020613890822736197654463892632953961461903659266302672901927472391491520220790086494421629530104134487848960992291400448418880719301301643211538480715261724678645854026893882662935786454",
                                            "timestamp": "7031267523384255931724229734709668852236981666398664500628609312084184839422714066646111517571504367881906999946906142205880431579116282139457459430490628368074988968893818537384306625760198775803846638688715282693724689063695143781851672316171826804538178049496230705683899355140338093894078404749873276975725352612375324676593660719462779985715395422238940426215008469041353116398836478202492841783866649731302994305254257899941902815383605743664381990123198126148381917220067404201702094151978496034163563512821780561363033330132250212505439974465744473015256287665802141980858496388564369684473390614913213492963",
                                        },
                                        "rctxt": "57595457065224964384532723809214070177221283698619189163273994795484340422910421565194502650047793930986106754378617657953634148479003200343596849944404829819454759272470409952906484645890312928698071525795674306099322535554040769358088959541527217412947857624113771388855906636033132647358149811523979540215755447957501980890442007680654813076936017670559128454293737368578572852087014890823425797572658699153814350307873126659084777516770578065919757432552875676249519945052600028967301682399735687262474002867432540942797659023173846671235714105519229325988649284822140546012838121486756140885474564667338033508925",
                                        "z": "92392248633579159734489059262157658066602172492655376458258465743015720279931884516580613066265472490833888951133646441506435308647071645829490880133890938400531213056849488446865347760761739826520600426315831962473284037732716361460703303047650224879262380737182724193613502180709449361207809530289742931388401783902150303407116160750968583373664158158828048355594343560019377499225431222258609781090866038688202681876195069528239050879910722452167883110680950451692711483330249956590291961929310759534360045884090140017202751268354570741889324005873479145636960045391944928193003593085006050343477314073342608326752",
                                    }
                                },
                            }
                        )
                    )
                )
            ),
        ),
    )

    # TODO: this mock should removed
    with mock.patch.object(W3cPresentation, "verify", return_value=True):
        vp = await manager.verify_presentation(
            VerifiablePresentation.deserialize(VP), OPTIONS
        )

    assert vp.verified and vp.errors == []
