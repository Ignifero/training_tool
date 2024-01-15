#!usr/bin/env python
"""Módulo controlador para el escáner de códigos de barras."""

# Importación de módulos

import cv2
from pyzbar.pyzbar import decode

# Definición de funciones

def barcode_scaner():
    """Función para escanear códigos de barras. Devuelve el código de barras leído.
    
    Todo el código de esta función fue hecho por la IA ChatGPT-3."""
    # Inicializa la cámara
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        
        # Convierte el marco a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Busca los códigos de barras en el marco
        barcodes = decode(gray)
        
        # Si se encuentra un código de barras, guarda el resultado en una variable
        if len(barcodes) > 0:
            barcode_data = barcodes[0].data.decode('utf-8')
            print(f"Código de barras leído: {barcode_data}")
            break
        
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 27: # Presiona 'ESC' para salir
            break
            
    cap.release()
    cv2.destroyAllWindows()

    return str(barcode_data)


def qr_scanner():
    """Función para escanear códigos QR.
    
    Todo el código de esta función fue hecho por la IA ChatGPT-3."""
    # Inicializa la cámara
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        
        # Convierte el marco a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Busca los códigos QR en el marco
        barcodes = decode(gray)
        
        # Si se encuentra un código QR, guarda el resultado en una variable
        if len(barcodes) > 0:
            barcode_data = barcodes[0].data.decode('utf-8')
            print(f"Código QR leído: {barcode_data}")
            break
        
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 27: # Presiona 'ESC' para salir
            break
            
    cap.release()
    cv2.destroyAllWindows()

    return str(barcode_data)




if __name__ == "__main__":
    print(barcode_scaner())
