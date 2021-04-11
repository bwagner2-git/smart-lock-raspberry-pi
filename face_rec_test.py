import face_recognition
pic=face_recognition.load_image_file('test.jpg')
encoding=face_recognition.face_encodings(pic)
print(len(encoding))
