import json
import re
from typing import OrderedDict
from bs4 import BeautifulSoup
import argparse

IS_TARGET = lambda section: section.text.startswith('4')


def format_title(title):
    txt = re.sub(r'\s+', ' ', title.text).strip()
    return 'Sec. ' + re.sub(r'\[.*]', '', txt)


def get_all_tables_after_section(section_tag):
    tables = []
    next_el = section_tag.find_next()

    while next_el:

        if next_el.name in ["h2", "h3"]:
            break  # stop at next section
        if next_el.name == "table":
            tables.append(next_el)
        next_el = next_el.find_next()

    return tables


def fill_dict(df, entry, key):
    if key == 'codelist_code':
        entry_split = entry.split('%%')
        if len(entry_split) == 1:
            link = entry_split[0]
            df[key] = link
        else:
            name, link = entry_split
            df[key] = name
            df['url'].append(link)
    else:
        if type(entry) == tuple:
            entry = list(entry)
            for i in range(len(entry)):
                entry[i] = entry[i][entry[i].find('%%') + 2:]
            clean_struct = entry
        else:
            pos = entry.find('%%')
            if pos == -1:
                clean_struct = entry
            else:
                clean_struct = entry[pos + 2:]
        if key == 'url':
            if clean_struct.startswith('http://') or clean_struct.startswith('https://') or clean_struct.startswith(
                    'file://'):
                df[key].append(clean_struct)
            else:
                df[key] = ''
        else:
            df[key] = clean_struct


def parse_table(table):
    df_table = OrderedDict({'codelist_name': '', 'agency': [], 'codelist_code': '', 'url': [], 'items': []})
    is_from_codelist = False

    rows = table.find_all("tr")
    is_exception = len(rows) == 1

    for row in rows:
        struct = []
        item = OrderedDict({'code_tag': '', 'code_value': '', 'description': ''})

        for col in row.find_all("td"):
            txt, a = re.sub(r'\s+', ' ', col.get_text().strip().replace('\n', ': ')), col.find_all('a')
            if a is not None and a != []:
                entry = []
                for aa in a:
                    if 'href' not in aa.attrs:
                        entry.append(txt)
                    else:
                        url = aa['href']
                        # footnote link
                        if url.startswith('#_'):
                            entry.append(re.sub(r'\[.*]', '', txt))
                        else:
                            entry.append(f'{txt.strip()}%%{url}')
                if len(entry) == 1:
                    struct.append(entry.pop())
                else:
                    struct.append(tuple(entry))
            else:
                struct.append(txt)

        # invalid Code Tags
        is_tuple = lambda x: type(x) == tuple
        if not is_tuple(struct[0]) and struct[0].strip() == 'ETC':
            continue
        elif len(struct) > 1:
            if not is_tuple(struct[1]) and (len(struct[1].strip()) == 0 or struct[1].strip() == 'ETC'):
                continue

        # is it Code List or Code Tag
        if is_tuple(struct[0]):
            is_header_codelist = False
        else:
            is_header_codelist = struct[0].lower().strip() == 'code list' or is_exception

        if is_tuple(struct[0]):
            is_header_codetag = False
        else:
            is_header_codetag = struct[0].lower().strip() == 'code tag' or struct[
                0].lower().strip() == 'code tag: (un/cas no)'

        if is_header_codelist:
            is_from_codelist = True
            if is_exception:
                i = 0
                for k in df_table:
                    if i < len(struct):
                        fill_dict(df_table, struct[i], k)
                    i += 1
        elif is_header_codetag:
            is_from_codelist = False
        else:
            # is the row from Code List or from Code Tag
            if is_from_codelist:
                i = 0
                for k in df_table:
                    if i < len(struct):
                        fill_dict(df_table, struct[i], k)
                    i += 1
            else:
                i = 0
                for k in item:
                    if i < len(struct):
                        item[k] = struct[i]
                    i += 1
                df_table['items'].append(item)

    if not df_table['items']:
        df_table.pop('items')

    return df_table


class Extractor(object):
    def __init__(self, fhtml):
        with open(fhtml, "r", encoding="utf-8") as f:
            self.soup = BeautifulSoup(f, "html.parser")

    def extract(self):
        sections = self.soup.find_all(['h2', 'h3'])
        pages = []
        for section in sections:
            # thesauri from Section 4
            if IS_TARGET(section):
                # if format_title(section) == 'Sec. 4.2 Assurance Level':
                page = {'section': format_title(section), 'thesauri': []}
                tables = get_all_tables_after_section(section)

                thesauri, last_is_thes = [], False
                for table in tables:
                    df = parse_table(table)
                    if 'items' not in df or not df['items']:
                        thesauri.append(df)
                        last_is_thes = True
                    elif last_is_thes and len(df['codelist_name'].strip()) == 0:
                        thesauri[-1]['items'] = df['items'].copy()
                        last_is_thes = False
                    elif len(df['items']) > 0 and len(df['codelist_name'].strip()) > 0:
                        thesauri.append(df)
                        last_is_thes = True

                # only keep Items for requested thesauri
                for i in range(len(thesauri)):
                    if thesauri[i]['url'] != '':
                        thesauri[i].pop('items')
                    else:
                        thesauri[i]['codelist_code'] = 'UNCLnnn'
                        thesauri[i]['url'] = []

                    if thesauri[i]['codelist_code'].startswith('eBIZ'):
                        thesauri[i]['codelist_code'] = '-'.join(thesauri[i]['codelist_code'].split(' '))

                page['thesauri'] = thesauri.copy()
                pages.append(page)
        return pages

    @staticmethod
    def save(p, fn):
        with open(fn, 'w') as fw:
            json.dump(p, fw, indent=2)


if __name__ == '__main__':
    argv = argparse.ArgumentParser(description='Parse the UneceRefGuide-v1.2')
    argv.add_argument('--fhtml', type=str, default='unece-202209-v1.2-tidy.htm')
    argv.add_argument('--out', type=str, default='unece-202209-v1.2.json')
    args = argv.parse_args()

    extractor = Extractor(args.fhtml)
    p = extractor.extract()
    extractor.save(p, args.out)
