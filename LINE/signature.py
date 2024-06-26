import jwt
from jwt.algorithms import RSAAlgorithm
import time

privateKey = {
  "alg": "RS256",
  "d": "uOPF3u59m8catXs59TZh8adF8spZ266uOJbo3gEYs-DuwXqLCToUYM7kZfh8mUy8IZWRj-bC2Ibx2-wJ-eT2HGpaFLvAj37OB1alCqCij_S5BVVSBe23NszRJd6SaHYWCXkEwCFgvA9KZB-YT_nnCpXdWHrnwzTwG9tUj-pyaOfvrUoeOFmbXn1yY7w-AF2cFGVcWJYt6N67BupuVw3g-lusoWjlIdJq8bheuPqr6VTv6YGCJuKN30i7QUVnmhN-F1T99a0QFh0J0GrX3vyc4EhtF8erDRpT-FlvOkASZ79SxEH9BqiqKkc7RICCWpj5oHcvumk2lCXbnmS7C3dDAQ",
  "dp": "XRiy6dXxQyASHJJNLs1e2GB9rpiiqP-C4bTy5HGWumf5I-OnVHp_MVD8gH35O6-QccAQ0vcxRRprhOdn4Dbjp_Z_xEFzv8kLyhqJ4TlT_Gy_rbzNj7hj4Zh8W7wUeSKQutoRQe2Y2CSzQThzxXb7ZSnO6mObdAmyU0tM2jTdT2M",
  "dq": "KaG--zSKCSbl6SqmdwaOehDFcj0BVH_7mDbRczgbaSFWcT2_1p6P8_e9_ut9nq7q72NSo7tyAPNACo4Kh6i0guwomMKgv_84shA-Pq7Ow3QEIVmK8-2sf9MMa5yhS-9SL4mKOEqV61MouXDs19qsCaerWtgdMHTI0hZ0apQJpQE",
  "e": "AQAB",
  "kty": "RSA",
  "n": "xRmby-7QBp2ba90rK_IfGz4qQhYhi-4ztR3ROUC8G4HFNCt52LQMWsaPebwLFYe0EnIrWuJVXuEmPBjCeWoD7am4f2GEesX-1apx3Jpx_f1p-VJ1zQm2HyPEB9gXg-B2dczU7TMJDgERYgdFvmPxrWUq_xKLRD_TTAGNAf2RyehYfIar-WlGy7dMgU_6BqLg1UljuNmz-e4k0FxnhIWpNw5XJxW9HGbzLyw99pcctQkV8QECxouBtE2e1MY2Zu0caWZIbRCiejypEUHZ-Vh4ObOK6d2QU6w6dOjiQeBoZ6ACd4uBC8r9pVd6Q_MDtsSg0u2rGeWKhKl_5O60t717iw",
  "p": "_51UBCup0tx1jh_JcSVqndi0FoFAkpKRxMYJY4Y9Ebx9nLbruFURnph3tYz62-WTEUMoHNRclUqkteNUQ445wO_7_zKtObMNg-8uxSRs0LhuignhkUW948D07FhrvK2jwcfoiH-H8HGNU0Gz2aIe6V86327i4JOlqVYXwwNwBws",
  "q": "xWWxVu37vAHoqhvsUxFmlPh4qnC_wmLBvEHRcDryNMMhpSzz0eO_S_fjFQfTcPPE2VUfulMnwPog7VUISrzFbdfWTqnnhsv3391VgtDyJqZQCXCT04-MFcXGHW5dukwyzQ_Gi0tZH1IfuCsV6A_HLtprsRcBAr2bTEHCdGVHLYE",
  "qi": "agZo7bBTN2lI9fESai79cGg5KSETfUsd4dP0JlJmTvfQVNt0ufnA3wnXTeEXp683QQBA7drWlKaf3Ipy8sOPC5OYMFXZy4iCuMPki5hnSBsMFd5uWlJ3sGDgi56YmQXahr8QxFCr3qzotd2LHRTc2BiM7sRGy0U8hhCcBoBNwUI",
  "use": "sig"
}

headers = {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "875d3d0a-2f72-4f63-bd29-0e97e9b12d64"
}

payload = {
  "iss": "2005708757",
  "sub": "2005708757",
  "aud": "https://api.line.me/",
  "exp":int(time.time())+(60 * 30),
  "token_exp": 60 * 60 * 24 * 30
}

key = RSAAlgorithm.from_jwk(privateKey)

JWT = jwt.encode(payload, key, algorithm="RS256", headers=headers, json_encoder=None)
print(JWT)