import json
def get_sections(data):
    sections_check = set()
    sections = []
    for p in data:
        docs = p['documents']
        for doc in docs:
            passages = doc['passages']
            for passage in passages:
                info = passage['infons']

                section_type = info['section_type'].lower()
                print(section_type)
                if section_type not in sections_check:
                    sections_check.add(section_type)
                    sections.append(section_type)

    return sections

# Function to parse the JSON data from PubMed
# input - data: JSON data from PubMed, section_list: List of sections to extract (otherwise all seections are extracted)
# output - text: Text extracted by concatenating all required sections, sections: Dictionary containing the extracted text for each section

def parse_pubmed_data(data, section_list = None):

    sections = {}
    if section_list is None:
        section_list = get_sections(data)

    for section in section_list:
        sections[section] = ""
        extracted_text = ""
    for p in data:
        docs = p['documents']
        for doc in docs:
            # print("Doc",doc)
            passages = doc['passages']
            for passage in passages:

                txt = passage['text']
                info = passage['infons']
                type = info['type']
                section_type = info['section_type']

                section_type = section_type.lower()
                if section_type in section_list:
                    sections[section_type] = sections[section_type] + txt
                    extracted_text += txt  + " "

    return({"text":extracted_text,"sections":sections})

def parse_pubmed_json(json_string, section_list = None):
    data = json.loads(json_string)
    return parse_pubmed_data(data, section_list)

