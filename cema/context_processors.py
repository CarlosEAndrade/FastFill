from datetime import datetime

def constantes_globais(request):
    current_date = datetime.now()
    return {
        'SITE_NAME': "CEMA",
        'FACEBOOK_LINK': "https://www.facebook.com/meu_facebook",
        'INSTAGRAM_LINK': "https://www.instagram.com/meu_instagram",
        'TELEFONE': "(XX) XXXX-XXXX",
        'ENDERECO': "Endereço completo",
        'CURRENT_DATE': current_date,

    }