import PySimpleGUI as sg
import clipboard, base64, webbrowser, io, os
from PIL import Image

# 
#      ___                            ____  ____                  __   _  _   
#     |_ _|_ __ ___   __ _  __ _  ___|___ \| __ )  __ _ ___  ___ / /_ | || |  
#      | || '_ ` _ \ / _` |/ _` |/ _ \ __) |  _ \ / _` / __|/ _ \ '_ \| || |_ 
#      | || | | | | | (_| | (_| |  __// __/| |_) | (_| \__ \  __/ (_) |__   _|
#     |___|_| |_| |_|\__,_|\__, |\___|_____|____/ \__,_|___/\___|\___/   |_|  
#                          |___/                                              
#

sg.theme('Material1')

# Exemplo de imagens Base64
img = b'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'
heart = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAnUlEQVRYhe2VyxGAIAxE0ZKgFC1TS4GW9K58NskyXPKOTAhvBtiE4DjOYrZRwRXj8107S/ntQ+tEArWmteZoHSzQa1hrPqrvSZgEJLQkdvZBUqYKHDmvFUBwgWkCyP03BZAEQw6/UxrWqpNQgjiImCKqKGZJmIeRRQJ9R+rHZpmAFIGWhPQHUXNA831pAtrsoAhYg0sNI6iWDyNnOS+NLETOLiFClgAAAABJRU5ErkJggg=='

menu = [['&Arquivo',['&Abrir Imagem', '&Sair']],
        ['&Ajuda', [['&Manual'], '&Autor', ['&GitHub', '&Linkedin']]]
        ]
layout = [[sg.Menu(menu)],
          [sg.Stretch(), sg.Image(img, key='-img-'), sg.Stretch()],
          [sg.Stretch(), sg.Text('Abrir imagem'),
           sg.Input('', key='-name-', size=(48,1)), sg.FileBrowse('Buscar imagem',
                                                     file_types=(("Image","*.jpg *.png *.bmp"),
                                                                 ("Outras", "*.*"),),
                                                     size = (12, 1)),
           sg.Stretch()],
          [sg.Stretch(), sg.Text('Clique em "Converter" para visualisar e converter a imagem para BASE64'),
           sg.Button('Converter', size=(12, 1)), sg.Stretch()],
          [sg.Stretch(), sg.Multiline(img.decode(),
                        key='-txt-',
                        size=(60,4)),            
           sg.Button('Copiar Código Base64', size=(12,4)), sg.Stretch()],
          [sg.Stretch(),
           sg.Text('Software feito com'),
           sg.Image(heart), sg.Stretch()]
          ]

window = sg.Window('Conversor de imagem para BASE64', layout, resizable=True)

while True:
    event, values = window.read()
    if event == 'Abrir Imagem':
        
        filename = sg.popup_get_file('Abrir Arquivo de Imagem',
                                       title='Abrir Arquivo',
                                       file_types=(("Image","*.jpg *.png *.bmp"),("Outras", "*.*"),),
                                       )
        window['-img-'].update(filename)
        window['-name-'].update(filename)
        
        try:    
            with open(filename, "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
            window['-txt-'].update(my_string.decode())
        except:
            sg.popup_timed('Erro!', 'Algo de errado não está certo, tente outra imagem!')
            window['-img-'].update(img)
            
    elif event == 'Converter':
        
        filename = values['-name-']
        window['-img-'].update(filename)
        window['-name-'].update(filename)
        
        try:    
            with open(filename, "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
            window['-txt-'].update(my_string.decode())
        except:
            sg.popup_timed('Erro!', 'Algo de errado não está certo, tente outra imagem!')
            window['-img-'].update(img)
            
    elif event == 'Copiar Código Base64':
        conteudo = values['-txt-']
        clipboard.copy(conteudo)
        sg.popup_timed('Conteúdo copiado','Conteudo copiado para área de transferência')
    
    elif event == sg.WINDOW_CLOSED or event == 'Sair':
        break
    
    elif event == 'Linkedin':
        webbrowser.open_new_tab('https://www.linkedin.com/in/elizeu-barbosa-abreu-69965b218/')
           
    elif event == 'GitHub':
        webbrowser.open_new_tab('https://github.com/elizeubarbosaabreu')
        
    elif event == 'Manual':
        sg.Popup('Manual',
                 '''
A função deste software é gerar imagens base64 para ser usada diretamente nos seus códigos sem necessitar ser hospedadas em servidores...

Por exemplo você pode inserir uma imagem em seu codigo html substituindo a palavra code pelo código gerado aqui neste software:

<img src = "data:image/jpeg;base64,code"/>

No PySimpleGui você pode usar:

imagem = b'code'
sg.Image(imagem)

Esse são apenas alguns exemplos. Você encontrará outras maneiras para inserir imagens base64 em seus códigos Java, PHP, Python, outros...

Desejo boas experiências com o software....''')

window.close()
