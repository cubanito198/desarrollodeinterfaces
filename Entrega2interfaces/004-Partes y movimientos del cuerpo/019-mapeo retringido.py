import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# Resolución de la pantalla y video
anchura = 1920
altura = 1080

centropantallax = round(1920 / 2)
centropantallay = round(1080 / 2)

centrovideox = round(640 / 2)
centrovideoy = round(480 / 2)

cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convertir a RGB y procesar con MediaPipe
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Dibujar las anotaciones en el video
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Obtener las coordenadas de la nariz
                nose_landmark = face_landmarks.landmark[1]  # Punto 1 es la nariz
                h, w, _ = image.shape
                
                # Coordenadas en píxeles del video
                x_video = int(nose_landmark.x * w)
                y_video = int(nose_landmark.y * h)

                # Convertir coordenadas del video a dimensiones de la pantalla
                x_screen = int((x_video - centrovideox) * (anchura / w) + centropantallax)
                y_screen = int((y_video - centrovideoy) * (altura / h) + centropantallay)
                
                # Mover el cursor
                pyautogui.moveTo(x_screen, y_screen)

                # Dibujar un círculo en la nariz
                cv2.circle(image, (x_video, y_video), 5, (0, 255, 0), -1)
                
                # Dibujar la malla facial
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                
        # Mostrar la imagen con anotaciones
        cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
            
cap.release()

