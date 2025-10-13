import ollama
import json

def print_line_sep(char='=',width=100):
    print(char*width)

def list_models():
    models_list = ollama.list()
    print(f"List of available models: {json.dumps(models_list, indent=4)}")
    
def show_model(model_name):
    print(ollama.show(model_name))

def create_model(model_name):
    modelfile = f"""
FROM {model_name}
SYSTEM you are the joker from batman
    """
    print(f"Creating new model {modelfile}...")
    create_model_response = ollama.create(model="ExampleModel", modelfile=modelfile)
    print("Create model response", create_model_response)
    """
    more api examples here:
    copy_resoponse = ollama.copy('mistral', '/user/mistral')
    delete_resoponse = ollama.delete('ExampleModel')
    pull_resoponse = ollama.pull('mistral')
    push_resoponse = ollama.push('/user/mistral')
    embeddings_resoponse = ollama.embeddins('/user/mistral')

    """

def main():
    print_line_sep()
    print('List of available models: ')
    list_models()

    print_line_sep()
    print('Show model: ')
    show_model('llava')

    print_line_sep()
    create_model("mistral")

main()
