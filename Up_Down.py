# import cv2 as cv
# import dlib

# # Load dlib's face detector and predictor
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# # Capture video
# cap = cv.VideoCapture(0)


# while True:
#     ret, frame = cap.read()
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
#     faces = detector(gray)
#     for face in faces:
#         landmarks = predictor(gray, face)

#         # Points of interest
#         points_idx = [68, 67, 66]

#         visible = True
#         for idx in points_idx:
#             x = landmarks.part(idx-1).x  # dlib's points start from 1
#             y = landmarks.part(idx-1).y

#             # Here, let's say a threshold of 50 is used for simplicity
#             # Darker points (less than 50 in grayscale) are considered "not visible"
#             if gray[y, x] < 50:
#                 visible = False
#                 break


#         if visible:
#             cv.putText(frame, "UP", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#         else:
#             cv.putText(frame, "DOWN", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        

            
    
#     cv.imshow("Frame", frame)
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv.destroyAllWindows()










import cv2 as cv
import dlib

# Load dlib's face detector and predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Capture video
cap = cv.VideoCapture(0)

vis = 0
not_vis = 0

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)

        # Determine mouth status (open or closed)
        top_lip_center = ((landmarks.part(51).x + landmarks.part(52).x + landmarks.part(53).x + landmarks.part(50).x) // 4, 
                        (landmarks.part(51).y + landmarks.part(52).y + landmarks.part(53).y + landmarks.part(50).y) // 4)

        bottom_lip_center = ((landmarks.part(57).x + landmarks.part(58).x + landmarks.part(59).x + landmarks.part(56).x) // 4, 
                            (landmarks.part(57).y + landmarks.part(58).y + landmarks.part(59).y + landmarks.part(56).y) // 4)

        tongue_tip = (landmarks.part(67).x, landmarks.part(67).y)  # Assuming landmark 67 is the tip, adjust as necessary

        distance_to_top_lip = abs(tongue_tip[1] - top_lip_center[1])
        distance_to_bottom_lip = abs(tongue_tip[1] - bottom_lip_center[1])

        if distance_to_top_lip < distance_to_bottom_lip:
            mouth_status = "closed"
        else:
            mouth_status = "open"
            # If the mouth is open, check for tongue status
            points_idx = [68, 67, 66]
            visible = True
            for idx in points_idx:
                x = landmarks.part(idx-1).x
                y = landmarks.part(idx-1).y
                if gray[y, x] < 53:
                    visible = False
                    break
            if visible:
                tongue_status = "UP"
                vis += 1
                vis / 100 == 0
                print('UP')
            else:
                tongue_status = "DOWN"
                not_vis += 1
                not_vis / 100 == 0
                print('DOWN')

            cv.putText(frame, tongue_status, (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display mouth status
        cv.putText(frame, "Mouth: " + mouth_status, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv.imshow("Frame", frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
