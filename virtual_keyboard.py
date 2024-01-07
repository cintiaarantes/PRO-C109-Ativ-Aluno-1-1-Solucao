import cv2
import mediapipe as mp
# Aual 109: Importar as classes (Key e Controller) do módulo pynput.keyboard
from pynput.keyboard import Key, Controller

# Aula 109: Iniciando o objeto Controller usando a variável keyboard
keyboard = Controller()

# Capturando os quadros do vídeo da webcan 
cap = cv2.VideoCapture(0)

# Aula 109 - Obtendo a largura e a altura da janela do vídeo para verificar a contagem dos dedos
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

# Módulos da biblioteca MediaPipe 
mp_hands = mp.solutions.hands # Detecta 1º a palma da mão e, depois, os 21 pontos de referência na palma da mão.
mp_drawing = mp.solutions.drawing_utils # Desenha as linhas de conexão entre os 21 pontos de referência.

# Método Hands - usa 2 parâmetros: min_detection_confidence(confiança mínima de detecção) e min_tracking_confidence (confiança mínima de rastreamento)
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

# Aula 109: Crie uma variável chamada "state" inicialmente com valor "None" (nenhum) para receber o stado do vídeo
state = None

# Defina uma função para contar os dedos
def countFingers(image, hand_landmarks, handNo=0):

    # Aula 109: Definindo a variável state dentro do função, precisamos garantir que ela seja global
    global state

    if hand_landmarks:
        # Obtenha todos os pontos de referência da PRIMEIRA mão VISÍVEL
        landmarks = hand_landmarks[handNo].landmark

        # Contangem dos dedos - Inicialmente vazia
        fingers = []

        for lm_index in tipIds:
                # Obtenha os valores y da ponta e da parte inferior do dedo
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y

                # Verifique se ALGUM DEDO está ABERTO ou FECHADO
                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        # print("DEDO com id ",lm_index," está Aberto")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        # print("DEDO com id ",lm_index," está Fechado")

        totalFingers = fingers.count(1)
        
        # Aula 109: REPRODUZA ou PAUSE um Vídeo
        if totalFingers == 4:
            state = "Play"
        
        if totalFingers == 0 and state == "Play":
            state = "Pause"
            keyboard.press("k")  
            #keyboard.press(Key.space)        

        
        # Mova o Vídeo PARA A FRENTE e PARA TRÁS 
        # Vamos usar o dedo indicador para mover pra frente e pra trás (direita: frete, esquerda: trás)
        # Temos que achar a posição da ponta do dedo indicador (8) 
        finger_tip_x = (landmarks[8].x)*width

        if totalFingers == 1: # Verificando se temos somente 1 dedo
            if  finger_tip_x < width-400: # Se posição x da ponta do dedo indicador é MENOR que largura-400 - Apontando para a esquerda
                print("Reproduzir Para Trás")
                keyboard.press(Key.left)

            if finger_tip_x > width-50:
                print("Reproduzir Para a Frente")
                keyboard.press(Key.right) # Se posição x da ponta do dedo indicador é MAIOR que largura-50 - Apontando para a direita

        
# Defina uma função para 
def drawHandLanmarks(image, hand_landmarks):

    # Desenhar as conexões entre os pontos de referência
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detecte os pontos de referência das mãos 
    results = hands.process(image)

    # Obtenha a posição do ponto de referência do resultado processado
    hand_landmarks = results.multi_hand_landmarks

    # Desenhe os pontos de referência
    drawHandLanmarks(image, hand_landmarks)

    # Obtenha a posição dos dedos da mão        
    countFingers(image, hand_landmarks)

    cv2.imshow("Controlador de Midia", image)

    # Aula 109: Mudando da tecla que "Sair da tela" ao pressionar a barra ESC (código 27)
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
