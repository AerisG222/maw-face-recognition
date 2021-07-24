from deepface import DeepFace

result = DeepFace.verify("/facedb/wan_choi/wan1.jpg", "/facetests/Z62_2341.jpg")
print(result)
