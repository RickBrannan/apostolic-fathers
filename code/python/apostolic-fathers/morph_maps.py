

def get_af_files():
    af_files = ['001-i_clement.txt', '002-ii_clement.txt', '003-ignatius-ephesians.txt', '004-ignatius-magnesians.txt',
                '005-ignatius-trallians.txt', '006-ignatius-romans.txt', '007-ignatius-philadelphians.txt',
                '008-ignatius-smyrnaeans.txt', '009-ignatius-polycarp.txt', '010-polycarp-philippians.txt',
                '011-didache.txt', '012-barnabas.txt', '013-shepherd.txt', '014-martyrdom.txt', '015-diognetus.txt']

    return af_files


def get_morphgnt_files():
    morphgnt_files = ['61-Mt-morphgnt.txt', '62-Mk-morphgnt.txt', '63-Lk-morphgnt.txt', '64-Jn-morphgnt.txt',
                      '65-Ac-morphgnt.txt', '66-Ro-morphgnt.txt', '67-1Co-morphgnt.txt', '68-2Co-morphgnt.txt',
                      '69-Ga-morphgnt.txt', '70-Eph-morphgnt.txt', '71-Php-morphgnt.txt', '72-Col-morphgnt.txt',
                      '73-1Th-morphgnt.txt', '74-2Th-morphgnt.txt', '75-1Ti-morphgnt.txt', '76-2Ti-morphgnt.txt',
                      '77-Tit-morphgnt.txt', '78-Phm-morphgnt.txt', '79-Heb-morphgnt.txt', '80-Jas-morphgnt.txt',
                      '81-1Pe-morphgnt.txt', '82-2Pe-morphgnt.txt', '83-1Jn-morphgnt.txt', '84-2Jn-morphgnt.txt',
                      '85-3Jn-morphgnt.txt', '86-Jud-morphgnt.txt', '87-Re-morphgnt.txt']
    return morphgnt_files

def get_degree_map():
    # Tauber's degree doesn't support 'Positive' so mapping to '-'
    degree_map = {'Pos': '-', 'Cmp': 'C', 'Sup': 'S'}
    return degree_map

def get_case_map():
    case_map = {'Gen': 'G', 'Nom': 'N', 'Acc': 'A', 'Dat': 'D', 'Voc': 'V'}
    return case_map

def get_case_map_lat():
    case_map_lat = get_case_map()
    case_map_lat['Abl'] = 'B'
    case_map_lat['Loc'] = 'L'
    return case_map_lat

def get_tense_map():
    # this is icky, but I can only really map Past to Aorist.
    tense_map = {'Past': 'A', 'Pres': 'P', 'Fut': 'F', 'Pqp': 'Y'}
    return tense_map

def get_tense_map_lat():
    tense_map = {'Past': 'X', 'Pres': 'P', 'Fut': 'F', 'Pqp': 'I'} # what the what is 'Pqp'?
    return tense_map

def get_aspect_map():
    aspect_map = {'Imp': 'I', 'Perf': 'A'}
    return aspect_map


def get_verb_form_map():
    verb_form_map = {'Fin': 'F', 'Part': 'P', 'Inf': 'N'}
    return verb_form_map


def get_mood_map():
    mood_map = {'Ind': 'I', 'Sub': 'S', 'Imp': 'D', 'Opt': 'O'}
    return mood_map


def get_number_map():
    number_map = {'Sing': 'S', 'Plur': 'P'}
    return number_map


def get_voice_map():
    voice_map = {'Act': 'A', 'Mid': 'M', 'Pass': 'P'}
    return voice_map


def get_gender_map():
    gender_map = {'Masc': 'M', 'Fem': 'F', 'Neut': 'N'}
    return gender_map


def get_pron_type_map():
    pron_type_map = {'Prs': 'P', 'Rel': 'R', 'Int': 'I', 'Dem': 'D'}
    return pron_type_map

# greek
tense_map = get_tense_map()
aspect_map = get_aspect_map()
verb_form_map = get_verb_form_map()
mood_map = get_mood_map()
number_map = get_number_map()
voice_map = get_voice_map()
case_map = get_case_map()
gender_map = get_gender_map()
pron_type_map = get_pron_type_map()
degree_map = get_degree_map()

# latin
case_map_lat = get_case_map_lat()
tense_map_lat = get_tense_map()

pos_map = {'NOUN': 'N-', 'VERB': 'V-', 'ADJ': 'A-', 'DET': 'RA', 'ADV': 'D-', 'PRON': 'R-', 'PROPN': 'NP',
           'NUM': 'NU', 'CCONJ': 'C-', 'SCONJ': 'C-', 'PART': 'X-', 'INTJ': 'I-', 'X': 'TL', 'ADP': 'D-', 'AUX': 'V-'}
           # AUX == verb like ειμι
           # ADP == treat like adverb (adposition?)


def get_pronoun_type(pos, morph):
    dct_analysis = {}
    for analysis in str(morph).split("|"):
        if '=' in analysis:
            (category, parse_code) = analysis.split('=')
            dct_analysis[category] = parse_code

    if "PronType" in dct_analysis:
        if dct_analysis['PronType'] in pron_type_map:
            return 'R' + pron_type_map[dct_analysis['PronType']]
        elif pos == "RA":
            return "RA"
        else:
            return "R-"
    else:
        return "R-"


# for now, just shift latin through greek routines
def convert_morph_lat(morph):
    return convert_morph(morph)


def convert_morph(morph):
    return_analysis = []
    dct_analysis = {}
    for analysis in str(morph).split("|"):
        if '=' in analysis:
            (category, parse_code) = analysis.split('=')
            dct_analysis[category] = parse_code
        else:
            #print(f"Skipping '{analysis}' (from {morph})")
            return '--------'

    if "Person" in dct_analysis:
        return_analysis.append(f"{dct_analysis['Person']}")
    else:
        return_analysis.append("-")

    # perfective past == aorist
    # imperfective past == imperfect?
    if "Aspect" in dct_analysis:
        if dct_analysis['Aspect'] in aspect_map:
            return_analysis.append(f"{aspect_map[dct_analysis['Aspect']]}")
        else:
            return_analysis.append("-")
    elif "Tense" in dct_analysis:
        if dct_analysis['Tense'] in tense_map:
            return_analysis.append(f"{tense_map[dct_analysis['Tense']]}")
        else:
            return_analysis.append("-")
    else:
        return_analysis.append("-")

    if "Voice" in dct_analysis:
        if dct_analysis['Voice'] in voice_map:
            return_analysis.append(f"{voice_map[dct_analysis['Voice']]}")
        else:
            return_analysis.append("-")
    else:
        return_analysis.append("-")

    if "VerbForm" in dct_analysis:
        # is it finite?
        if dct_analysis['VerbForm'] == "Fin":
            if "Mood" in dct_analysis:
                if dct_analysis['Mood'] in mood_map:
                    return_analysis.append(f"{mood_map[dct_analysis['Mood']]}")
                else:
                    return_analysis.append("-")
        else:  # participle or infinitive
            if dct_analysis['VerbForm'] in verb_form_map:
                return_analysis.append(f"{verb_form_map[dct_analysis['VerbForm']]}")
            else:
                return_analysis.append("-")
    else:
        return_analysis.append("-")

    if "Case" in dct_analysis:
        if dct_analysis['Case'] in case_map:
            return_analysis.append(f"{case_map[dct_analysis['Case']]}")
        else:
            return_analysis.append("-")
    else:
        return_analysis.append("-")

    if "Number" in dct_analysis:
        if dct_analysis['Number'] in number_map:
            return_analysis.append(f"{number_map[dct_analysis['Number']]}")
        else:
            return_analysis.append("-")
    else:
        return_analysis.append("-")

    if "Gender" in dct_analysis:
        if dct_analysis['Gender'] in gender_map:
            return_analysis.append(f"{gender_map[dct_analysis['Gender']]}")
        else:
            return_analysis.append("-")
    else:
        return_analysis.append("-")

    if "Degree" in dct_analysis:
        if dct_analysis['Degree'] in degree_map:
            return_analysis.append(f"{degree_map[dct_analysis['Degree']]}")
        else:
            return_analysis.append("-")
    else:
        return_analysis.append("-")

    return_string = "".join(return_analysis)
    # print(f"Returning {return_string} (from {morph})")


    return "".join(return_analysis)

