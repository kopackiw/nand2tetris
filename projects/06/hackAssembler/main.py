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


to_machine_code = lambda line: command_to_machine_code(parse_to_command(line))

def assembly(source_code: str) -> str:
    return (
        seq(lines(source_code))
            .map(clean_whitespace)
            .filter(lambda line: line.strip() != '')
            .map(to_machine_code)
            .make_string('\n')
    ) + '\n'

def main():
    path_to_asm = sys.argv[1]
    output_path = path_to_asm.split('.')[0] + '.hack'
    
    with open(path_to_asm, 'r') as source_file:
        with open(output_path, 'w') as output_file:
            output_file.write((assembly(source_file.read())))


if __name__ == '__main__':
    main()