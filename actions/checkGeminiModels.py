import google.generativeai as genai

genai.configure(api_key="AIzaSyDCwNZjhMJgOOKmzIcSmY8C1lwvDQEN7To")

models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)
