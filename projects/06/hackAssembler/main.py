import sys
from functional import seq

lines = lambda s: s.split('\n')
clean_whitespace = lambda s: s.split('//')[0].strip()


def parse_to_command(line: str = 'A=D'):
    if line.startswith('@'):
        return { 'type': 'A', 'address': line[1:] }
    else:
        rest_of_line = line
        dest = None
        value = None
        jump = None

        if '=' in rest_of_line:
            [dest, rest] = rest_of_line.split('=')
            rest_of_line = rest

        if ';' in rest_of_line:
            [value, jump] = rest_of_line.split(';')

        if value is None:
            value = rest_of_line

        return {
            'type': 'C',
            'dest': dest,
            'value': value,
            'jump': jump,
        }


def value_to_machine_code(value):
    match value:
        case '0': return '101010'
        case '1': return '111111'
        case '-1': return '111010'
        case 'D': return '001100'
        case 'A' | 'M': return '110000'
        case '!D': return '001101'
        case '!A' | '!M': return '110001'
        case '-D': return '001111'
        case '-A' | '-M': return '110011'
        case 'D+1': return '011111'
        case 'A+1' | 'M+1': return '110111'
        case 'D-1': return '001110'
        case 'A-1' | 'M-1': return '110010'
        case 'D+A' | 'D+M': return '000010'
        case 'A-D' | 'M-D': return '000111'
        case 'D&A' | 'D&M': return '000000'
        case 'D|A' | 'D|M': return '010101'


def substitute_labels_refs(line: str, labels, counter) -> str:
    if not line.startswith('@'):
        return line
    elif line.startswith('@R') and line[2].isnumeric():
        return '@' + line[2:]
    elif line[1:].isnumeric():
        return line
    elif labels.get(line[1:]) is not None:
        return '@' + str(labels.get(line[1:]))
    else:
        newValue = counter['v']
        labels[line[1:]] = newValue
        counter['v'] = counter['v'] + 1
        return '@' + str(newValue)


def resolve_labels(source_code: str) -> str:
    variable_register_counter = {'v': 16}

    labels = (
        seq(lines(source_code))
            .enumerate(start=1)
            .filter(lambda tup: tup[1].startswith('('))
            .map(lambda tup: (tup[1][1:-1], tup[0]))
            .enumerate(start=1)
            .map(lambda posTup: (posTup[1][0], posTup[1][1] - posTup[0]))
            .to_dict()
    )

    # predefined labels
    labels['SP'] = 0
    labels['LCL'] = 1
    labels['ARG'] = 2
    labels['THIS'] = 3
    labels['THAT'] = 4

    return (
        seq(lines(source_code))
            .filter_not(lambda line: line.startswith('('))
            .map(lambda a: substitute_labels_refs(a, labels, variable_register_counter))
            .make_string('\n')
    )


def command_to_machine_code(command):
    if command['type'] == 'A':
        return format(int(command['address']), '016b')

    elif command['type'] == 'C':
        opcode = '1'
        fill = '11'
        memory = '1' if 'M' in command['value'] else '0'
        value = value_to_machine_code(command['value'])
        dest = '000' if command['dest'] is None else ''.join([
            '1' if 'A' in command['dest'] else '0',
            '1' if 'D' in command['dest'] else '0',
            '1' if 'M' in command['dest'] else '0',
        ])
        jump = {
            None: '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }[command['jump']]

        return f'{opcode}{fill}{memory}{value}{dest}{jump}'


def assembly(source_code: str) -> str:
    clean_source_with_labels = (
        seq(lines(source_code))
            .map(clean_whitespace)
            .filter(lambda line: line.strip() != '')
            .make_string('\n')
    )

    section_lookup_table = resolve_labels(clean_source_with_labels)

    return (
        seq(lines(section_lookup_table))
            .map(parse_to_command)
            .map(command_to_machine_code)
            .make_string('\n')
    ) + '\n'


def main():
    path_to_asm = sys.argv[1]
    output_path = path_to_asm.split('.')[0] + '.hack'
    
    with open(path_to_asm, 'r') as source_file:
        with open(output_path, 'w') as output_file:
            output_file.write(assembly(source_file.read()))


if __name__ == '__main__':
    main()
