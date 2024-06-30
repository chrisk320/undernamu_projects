import jwt
from jwt.algorithms import RSAAlgorithm
import time

privateKey = {
  "alg": "RS256",
  "d": "mcf2gbjExYkJbL5xmVzOPBxDofAx3n2rg7Y7zmlE5zKv1zdvOLy0LLUIl4EuX5kIvvuSSpgECv-kBpw9GIrDyy9ja8iPkFKKpeBJDmmDJyAY1JT9jV49CllMNXGPj5pK02Z77uULZtp9KAwU1evRF7OSaYnQVYRqT9THNR86tGnbQiHcQd_gr-VMkjKBl6K7o8qVyOU4zWWQhk3XCXAwMDQKDy11KRXN-_seEwl6ASITBvnnoYpbiKDd2CcFNs6fl30NcR4WP5NZ5gJ75jBA4feIaK24mz1--j8JQrMrj0ZfUB91T-cyjqF-7v-_uDCXWWaqN5aeNmb-BEqsXr2ooQ",
  "dp": "jnBmpQuJVP4YW1KCzisliJCXriNCE37AMYS4XEEhj34povQczpW-bz8Ain78T58YaTi4-pzwJzNtvM7uhhRgUgRJB5iYMpDoiGaLMP0F3S8h0O9xxCze0C4nvKvo8uryGM1vAp85FWWO_Q9g-EJiw6SvZ4n8NZ4Ntw5pN7A88Ls",
  "dq": "eDMfMmAY-_nYY3sk05V5_WQGCkZ2bJO7hfg5MWds21uP5Xqh9ykUqb7tpbpygGzBWHIXprjEuty8PVqdoU65BJsQiBHIZklSnEcta6YneQjCCtB4bq1AXvsD7aAJppuU-S4jbxt6BXTUZmuC98UgJBw1iXneB7TxYyORlBM6LME",
  "e": "AQAB",
  "kty": "RSA",
  "n": "wZR2yUYYkUK3HMoBvV18uiyn8Ld8fXaEccpuNypglZivxFKAaBDIHTGnkDaMx-1bIQoo_WuGme8NAcvJ4E22OSmTxSbd2t3OY2i5d6Qn6RUg7uwFvDEfwLLbqUVNScBLwGsSaVvoR4EUULSy2vZpZCPx2BqFtn4kmCuox5aJaX8eMYu7OSHfQTrJB2PpeMtg4twDgS3UOVmdQAi14DO-R7QI8cuSFlQtF6-sNSYDwyXbggKsH1TzS0Vgs2FUGyilkuYniGTA321xFyvFKODvAwUC2sm8kLz6GBGYHwjvNzIV_gxtvQklMkXXNxqhW7sRrkabarxQ9YxhbldvdWU4Fw",
  "p": "9d9HO50IgZBWJ3237NZBAtpe416-OuVzr6_oz8sDvxRWO69GWeyg3Ee2wec_CqSJGDvxpaW0-0-eCy8Uar4zYcseCbT6tv2kBmLHG9QcXHZsCC4_A8KNwIfg10BiKnAVfng4lciq3TgALfJ84sQcjHy03h0j5vWa4WjDXRRLAyc",
  "q": "yY3Dnm05OKL-EeQ646P4Q3pnD0BuKiTJEd3h1ApdIglZN75xqtFPe6lGKvf1Rt23QCJFLFv8Cpgp4Zm8HYeZod0wC4sL3nmtt2Knb7bD6wqhko2NtclXMe7iXzyYhwQ93Pb9wUUmLfJ-M0yKCwEtrLZqQIAdWrKWEvLnmwEdeZE",
  "qi": "nS-r3j17ZDiBIVlUkl-aNj_m8cCOZFTl0gqP9im92tvd7rXEhsumryOtWjT8lnE6h4yi-BOnzh3RVcFFTnECMlbHnvOdN9bxVemD71VACLUXJWEnBfJRLmk8uCckkB9_f5r2Al_lVEh2ZyZRuXS9a2hiR0opZFHXRLHLuE52I_g",
  "use": "sig"
}

headers = {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "66493771-853b-4ffa-b9f3-9f3697ff6874"
}

payload = {
  "iss": "2005723717",
  "sub": "2005723717",
  "aud": "https://api.line.me/",
  "exp":int(time.time())+(60 * 30),
  "token_exp": 60 * 60 * 24 * 30
}

key = RSAAlgorithm.from_jwk(privateKey)

JWT = jwt.encode(payload, key, algorithm="RS256", headers=headers, json_encoder=None)
print(JWT)