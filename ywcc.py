# -*- coding: utf-8 -*-
def tolocstr(localstr):
    if (localstr in ['en_US','en-US','en','enus','EN-US','english','English','US']):
        return 'en_US'
    elif (localstr in ['pt_BR','pt-BR','pt','ptbr','PT-BR','portuguese','Portuguese','Portugues','PT']):
        return 'pt_BR'
    elif (localstr in ['de_DE','de-DE','de','dede','DE-DE','deutsch','Deutsch','DE']):
        return 'de_DE'
    else:
        return 'pt_BR'

def totempstr(tempstr):
    if (tempstr in ['C','Celsius','celsius','c']):
        return 'C'
    elif (tempstr in ['F','f','Fahrenheit','fahrenheit']):
        return 'F'
    else:
        return 'K'

ywcc_ptbr = {
    '0':  'tornado',                        # tornado
    '1':  'tempestade tropical',            # tropical storm
    '2':  'furacão',                        # hurricane
    '3':  'tempestade severa',              # severe thunderstorms
    '4':  'trovoadas',                      # thunderstorms
    '5':  'chuva e neve',                   # mixed rain and snow
    '6':  'chuva e granizo fino',           # mixed rain and sleet
    '7':  'neve e granizo fino',            # mixed snow and sleet
    '8':  'garoa gélida',                   # freezing drizzle
    '9':  'garoa',                          # drizzle
    '10': 'chuva gélida',                   # freezing rain
    '11': 'chuvisco',                       # showers
    '12': 'chuva',                          # showers
    '13': 'neve em flocos finos',           # snow flurries
    '14': 'leve precipitação de neve',      # light snow showers
    '15': 'ventos com neve',                # blowing snow
    '16': 'neve',                           # snow
    '17': 'chuva de granizo',               # hail
    '18': 'pouco granizo',                  # sleet
    '19': 'pó em suspensão',                # dust
    '20': 'neblina',                        # foggy
    '21': 'névoa seca',                     # haze
    '22': 'enfumaçado',                     # smoky
    '23': 'vendaval',                       # blustery
    '24': 'ventando',                       # windy
    '25': 'frio',                           # cold
    '26': 'nublado',                        # cloudy
    '27': 'muitas nuvens (noite)',          # mostly cloudy (night)
    '28': 'muitas nuvens (dia)',            # mostly cloudy (day)
    '29': 'parcialmente nublado (noite)',   # partly cloudy (night)
    '30': 'parcialmente nublado (dia)',     # partly cloudy (day)
    '31': 'céu limpo (noite)',              # clear (night)
    '32': 'ensolarado',                     # sunny
    '33': 'tempo bom (noite)',              # fair (night)
    '34': 'tempo bom (dia)',                # fair (day)
    '35': 'chuva e granizo',                # mixed rain and hail
    '36': 'quente',                         # hot
    '37': 'tempestades isoladas',           # isolated thunderstorms
    '38': 'tempestades esparsas',           # scattered thunderstorms
    '39': 'tempestades esparsas',           # scattered thunderstorms
    '40': 'chuvas esparsas',                # scattered showers
    '41': 'nevasca',                        # heavy snow
    '42': 'tempestades de neve esparsas',   # scattered snow showers
    '43': 'nevasca',                        # heavy snow
    '44': 'parcialmente nublado',           # partly cloudy
    '45': 'chuva com trovoadas',            # thundershowers
    '46': 'tempestade de neve',             # snow showers
    '47': 'relâmpagos e chuvas isoladas',   # isolated thundershowers
    '3200': 'não disponível'                # not available
}

ywcc_enus = {
    '0':  'tornado',                        # tornado
    '1':  'tropical storm',                 # tropical storm
    '2':  'hurricane',                      # hurricane
    '3':  'severe thunderstorms',           # severe thunderstorms
    '4':  'thunderstorms',                  # thunderstorms
    '5':  'mixed rain and snow',            # mixed rain and snow
    '6':  'mixed rain and sleet',           # mixed rain and sleet
    '7':  'mixed snow and sleet',           # mixed snow and sleet
    '8':  'freezing drizzle',               # freezing drizzle
    '9':  'drizzle',                        # drizzle
    '10': 'freezing rain',                  # freezing rain
    '11': 'showers',                        # showers
    '12': 'showers',                        # showers
    '13': 'snow flurries',                  # snow flurries
    '14': 'light snow showers',             # light snow showers
    '15': 'blowing snow',                   # blowing snow
    '16': 'snow',                           # snow
    '17': 'hail',                           # hail
    '18': 'sleet',                          # sleet
    '19': 'dust',                           # dust
    '20': 'foggy',                          # foggy
    '21': 'haze',                           # haze
    '22': 'smoky',                          # smoky
    '23': 'blustery',                       # blustery
    '24': 'windy',                          # windy
    '25': 'cold',                           # cold
    '26': 'cloudy',                         # cloudy
    '27': 'mostly cloudy (night)',          # mostly cloudy (night)
    '28': 'mostly cloudy (day)',            # mostly cloudy (day)
    '29': 'partly cloudy (night)',          # partly cloudy (night)
    '30': 'partly cloudy (day)',            # partly cloudy (day)
    '31': 'clear (night)',                  # clear (night)
    '32': 'sunny',                          # sunny
    '33': 'fair (night)',                   # fair (night)
    '34': 'fair (day)',                     # fair (day)
    '35': 'mixed rain and hail',            # mixed rain and hail
    '36': 'hot',                            # hot
    '37': 'isolated thunderstorms',         # isolated thunderstorms
    '38': 'scattered thunderstorms',        # scattered thunderstorms
    '39': 'scattered thunderstorms',        # scattered thunderstorms
    '40': 'scattered showers',              # scattered showers
    '41': 'heavy snow',                     # heavy snow
    '42': 'scattered snow showers',         # scattered snow showers
    '43': 'heavy snow',                     # heavy snow
    '44': 'partly cloudy',                  # partly cloudy
    '45': 'thundershowers',                 # thundershowers
    '46': 'snow showers',                   # snow showers
    '47': 'isolated thundershowers',        # isolated thundershowers
    '3200': 'not available'                 # not available
}

ywcc_de  = {
    '0':  'Tornado',                        # tornado
    '1':  'Tropischer Sturm',               # tropical storm
    '2':  'Orkan',                          # hurricane
    '3':  'Heftiges Gewitter',              # severe thunderstorms
    '4':  'Gewitter',                       # thunderstorms
    '5':  'Regen und Schnee',               # mixed rain and snow
    '6':  'Regen und Eisregen',             # mixed rain and sleet
    '7':  'Schnee und Eisregen',            # mixed snow and sleet
    '8':  'Gefrierender Nieselregen',       # freezing drizzle
    '9':  'Nieselregen',                    # drizzle
    '10': 'Gefrierender Regen',             # freezing rain
    '11': 'Schauer',                        # showers
    '12': 'Schauer',                        # showers
    '13': 'Schneeschauer',                  # snow flurries
    '14': 'Leichte Schneeschauer',          # light snow showers
    '15': 'Stürmiger Schneefall',           # blowing snow
    '16': 'Schnee',                         # snow
    '17': 'Hagel',                          # hail
    '18': 'Eisregen',                       # sleet
    '19': 'Staub',                          # dust
    '20': 'Neblig',                         # foggy
    '21': 'Dunst',                          # haze
    '22': 'Staubig',                        # smoky
    '23': 'Stürmisch',                      # blustery
    '24': 'Windig',                         # windy
    '25': 'Kalt',                           # cold
    '26': 'Bewölkt',                        # cloudy
    '27': 'Größtenteils bewölkt (nachts))', # mostly cloudy (night)
    '28': 'Größtenteils bewölkt (tagsüber)',# mostly cloudy (day)
    '29': 'Teilweise bewölkt (nachts)',     # partly cloudy (night)
    '30': 'Teilweise bewölkt (tagsüber)',   # partly cloudy (day)
    '31': 'Klar (nachts)',                  # clear (night)
    '32': 'Sonnig',                         # sunny
    '33': 'Schön (nachts)',                 # fair (night)
    '34': 'Schön (tagsüber)',               # fair (day)
    '35': 'Regen und Hagel',                # mixed rain and hail
    '36': 'Heiß',                           # hot
    '37': 'Einzelne Gewitter',              # isolated thunderstorms
    '38': 'Vereinzelte Gewitter',           # scattered thunderstorms
    '39': 'Vereinzelte Gewitter',           # scattered thunderstorms
    '40': 'Vereinzelte Schauer',            # scattered showers
    '41': 'Starker Schneefall',             # heavy snow
    '42': 'Vereinzelte Schneeschauer',      # scattered snow showers
    '43': 'Starker Schneefall',             # heavy snow
    '44': 'Teilweise bewölkt',              # partly cloudy
    '45': 'Donnerregen',                    # thundershowers
    '46': 'Schneeschauer',                  # snow showers
    '47': 'Einzelne Gewitterschauer',       # isolated thundershowers
    '3200': 'nicht verfügbar'               # not available
}

ywcc= {'pt_BR': ywcc_ptbr, 'en_US': ywcc_enus, 'de_DE': ywcc_de}
