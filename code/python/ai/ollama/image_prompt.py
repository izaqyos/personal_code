import ollama
import json

def print_line_sep(char='=',width=100):
    print(char*width)

def list_models():
    models_list = ollama.list()
    print(f"List of available models: {json.dumps(models_list, indent=4)}")
    
def show_model(model_name):
    print(ollama.show(model_name))

def analize_image_prompt():
    with open('cricket.jpg', 'rb') as file:
        response = ollama.chat(
            model = 'llava', #don't forget to install and run the model. e.g. $ollama run llava
            messages = [{'role':'user',
                         'content':'what is in this image',
                        'images':[file.read()],
                        },
                        ],
                        )
    
    print(response['message']['content'])

def main():
    print_line_sep()
    print('List of available models: ')
    list_models()

    print_line_sep()
    print('Show model: ')
    show_model('llava')

    print_line_sep()
    print('Analize image prompt: ')
    analize_image_prompt()
    print_line_sep()

main()