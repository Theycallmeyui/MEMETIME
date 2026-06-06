import cv2
import mediapipe as mp
import math

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

finger_heart_count = 0
smile_count = 0
smirk_count = 0
me_count = 0
finger_bite_count = 0
stressed_count = 0
mouth_open_count = 0

def dist(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def dist_xy(p, x, y):
    return math.sqrt((p.x - x) ** 2 + (p.y - y) ** 2)

def get_caption(label):
    captions = {
        "PEACE": "Peace mode: hamster approved.",
        "HOLD ON": "Pause. Let them cook.",
        "THUMBS UP": "Approved energy detected.",
        "THUMBS DOWN": "Not today bestie.",
        "BIG SMILE": "Certified happy hamster energy.",
        "MOUTH OPEN": "Wait... what did I just see?",
        "SMIRK": "Suspicious rizz detected.",
        "ME?": "Who, me?",
        "FINGER BITE": "Shy mode activated.",
        "STRESSED": "Brain loading...",
        "FINGER HEART": "Cute attack detected.",
        "NO POSE": "Just existing... still meme-worthy."
    }
    return captions.get(label, "Show your pose, get your meme!")

def draw_menu(frame):
    cv2.rectangle(frame, (10, 10), (330, 90), (0, 0, 0), -1)

    cv2.putText(frame,"MEME-Time!",(25, 40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 255, 255),2)

    cv2.putText(frame,"Show your pose, get your meme!",(25, 70),cv2.FONT_HERSHEY_SIMPLEX,0.45,(255, 255, 255), 1)

def draw_result(frame, label, caption):
    cv2.rectangle(frame, (10, 260), (620, 340), (0, 0, 0), -1)

    cv2.putText(frame,label,(25, 295),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0, 255, 0),2)

    cv2.putText(frame, caption,(25, 325),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255, 255, 255),1)

def draw_meme_on_frame(frame, meme_image):
    if meme_image is None:
        return

    meme_image = cv2.resize(meme_image, (220, 220))

    h, w, _ = frame.shape

    x1 = w - 240
    y1 = 20
    x2 = x1 + 220
    y2 = y1 + 220

    frame[y1:y2, x1:x2] = meme_image
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)

with mp_holistic.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5) as holistic:

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(rgb)

        label = "NO POSE"
        meme_image = cv2.imread("memes/no_pose/confused_math.jpg")

        detected_finger_heart_now = False
        detected_smile_now = False
        detected_smirk_now = False
        detected_me_now = False
        detected_finger_bite_now = False
        detected_stressed_now = False
        detected_mouth_open_now = False

        mouth_center_x = None
        mouth_center_y = None
        forehead_x = None
        forehead_y = None

        if results.face_landmarks:
            mp_drawing.draw_landmarks(frame,results.face_landmarks,mp_holistic.FACEMESH_CONTOURS)

            face = results.face_landmarks.landmark

            left_mouth = face[61]
            right_mouth = face[291]
            upper_lip = face[13]
            lower_lip = face[14]

            mouth_center_x = (left_mouth.x + right_mouth.x) / 2
            mouth_center_y = (upper_lip.y + lower_lip.y) / 2

            forehead_x = face[10].x
            forehead_y = face[10].y

            mouth_width = dist(left_mouth, right_mouth)
            mouth_height = dist(upper_lip, lower_lip)

            smile_ratio = mouth_width / (mouth_height + 0.001)
            mouth_corner_diff = abs(left_mouth.y - right_mouth.y)

            if smile_ratio > 5.8 and mouth_width > 0.09 and mouth_height < 0.04:
                detected_smile_now = True

            if mouth_height > 0.045:
                detected_mouth_open_now = True

            if mouth_corner_diff > 0.025 and smile_ratio > 4.0 and mouth_height < 0.04:
                detected_smirk_now = True

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_holistic.POSE_CONNECTIONS)

        for hand_landmarks in [results.left_hand_landmarks, results.right_hand_landmarks]:

            if hand_landmarks:
                mp_drawing.draw_landmarks(frame,hand_landmarks,mp_holistic.HAND_CONNECTIONS)

                thumb_tip = hand_landmarks.landmark[4]
                thumb_ip = hand_landmarks.landmark[3]

                index_tip = hand_landmarks.landmark[8]
                index_pip = hand_landmarks.landmark[6]

                middle_tip = hand_landmarks.landmark[12]
                middle_pip = hand_landmarks.landmark[10]

                ring_tip = hand_landmarks.landmark[16]
                ring_pip = hand_landmarks.landmark[14]

                pinky_tip = hand_landmarks.landmark[20]
                pinky_pip = hand_landmarks.landmark[18]

                distance_thumb_index = dist(thumb_tip, index_tip)

                index_up = index_tip.y < index_pip.y
                middle_up = middle_tip.y < middle_pip.y
                ring_up = ring_tip.y < ring_pip.y
                pinky_up = pinky_tip.y < pinky_pip.y

                ring_down = ring_tip.y > ring_pip.y
                pinky_down = pinky_tip.y > pinky_pip.y

                if distance_thumb_index < 0.07:
                    detected_finger_heart_now = True

                peace_detected = (index_up and middle_up and ring_down and pinky_down and distance_thumb_index > 0.08)

                stop_hand_detected = (index_up and middle_up and ring_up and pinky_up)

                thumbs_up_detected = (thumb_tip.y < thumb_ip.y and distance_thumb_index > 0.09 and not index_up and not middle_up)

                thumbs_down_detected = (thumb_tip.y > thumb_ip.y and distance_thumb_index > 0.09 and not index_up and not middle_up)

                if mouth_center_x is not None:
                    index_to_mouth = dist_xy(index_tip, mouth_center_x, mouth_center_y)

                    if index_to_mouth < 0.08:
                        detected_finger_bite_now = True

                if forehead_x is not None:
                    wrist = hand_landmarks.landmark[0]
                    index_to_forehead = dist_xy(index_tip, forehead_x, forehead_y)
                    wrist_to_forehead = dist_xy(wrist, forehead_x, forehead_y)

                    if index_to_forehead < 0.13 or wrist_to_forehead < 0.16:
                        detected_stressed_now = True

                if results.pose_landmarks:
                    pose = results.pose_landmarks.landmark

                    left_shoulder = pose[11]
                    right_shoulder = pose[12]

                    chest_x = (left_shoulder.x + right_shoulder.x) / 2
                    chest_y = (left_shoulder.y + right_shoulder.y) / 2 + 0.12

                    distance_to_chest = math.sqrt((index_tip.x - chest_x) ** 2 + (index_tip.y - chest_y) ** 2)

                    pointing_finger = (index_up and not middle_up and ring_down and pinky_down)

                    if distance_to_chest < 0.18 and pointing_finger:
                        detected_me_now = True

                if peace_detected:
                    label = "PEACE"
                    meme_image = cv2.imread("memes/peace/peace_hamster.jpg")

                elif stop_hand_detected:
                    label = "HOLD ON"
                    meme_image = cv2.imread("memes/stop_hand/hold_on_please.jpg")

                elif thumbs_up_detected:
                    label = "THUMBS UP"
                    meme_image = cv2.imread("memes/thumbs_up/hamster.jpg")

                elif thumbs_down_detected:
                    label = "THUMBS DOWN"
                    meme_image = cv2.imread("memes/thumbs_down/thumbsdown.jpg")

        if detected_finger_heart_now:
            finger_heart_count += 1
        else:
            finger_heart_count = 0

        if detected_smile_now:
            smile_count += 1
        else:
            smile_count = 0

        if detected_smirk_now:
            smirk_count += 1
        else:
            smirk_count = 0

        if detected_me_now:
            me_count += 1
        else:
            me_count = 0

        if detected_finger_bite_now:
            finger_bite_count += 1
        else:
            finger_bite_count = 0

        if detected_stressed_now:
            stressed_count += 1
        else:
            stressed_count = 0

        if detected_mouth_open_now:
            mouth_open_count += 1
        else:
            mouth_open_count = 0

        if smile_count >= 3:
            label = "BIG SMILE"
            meme_image = cv2.imread("memes/smile/hamster.jpg")

        if mouth_open_count >= 3:
            label = "MOUTH OPEN"
            meme_image = cv2.imread("memes/questioning/questioning.jpg")

        if smirk_count >= 3:
            label = "SMIRK"
            meme_image = cv2.imread("memes/smirk/smirk.jpg")

        if me_count >= 3:
            label = "ME?"
            meme_image = cv2.imread("memes/me/me.jpg")

        if finger_bite_count >= 3:
            label = "FINGER BITE"
            meme_image = cv2.imread("memes/finger_bite/finger_bite.jpg")

        if stressed_count >= 3:
            label = "STRESSED"
            meme_image = cv2.imread("memes/stressed/stressed.jpg")

        if finger_heart_count >= 2:
            label = "FINGER HEART"
            meme_image = cv2.imread("memes/finger_heart/monkey.jpg")

        draw_menu(frame)
        draw_meme_on_frame(frame, meme_image)
        draw_result(frame, label, get_caption(label))

        cv2.imshow("MEME-Time!", frame)

        key = cv2.waitKey(1)

        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()