import sys
from functional import seq

FILE_NAME=None

lines = lambda s: s.split('\n')
clean_whitespace = lambda s: s.split('//')[0].strip()


def increment_stack() -> str:
    return '\n'.join(['@SP', 'M=M+1'])


def decrement_stack() -> str:
    return '\n'.join(['@SP', 'M=M-1'])


def push_value_onto_stack() -> str:
    return '\n'.join([
        '@SP',
        'A=M',
        'M=D',
        increment_stack(),
    ])


def push_value_onto_stack_i(value: str) -> str:
    return '\n'.join([
        f'@{value}',
        'D=A',
        push_value_onto_stack(),
    ])


def pop_value_from_stack() -> str:
    return '\n'.join([
        decrement_stack(),
        'A=M',
        'D=M',
    ])


def _do_math_op(op: str) -> str:
    return '\n'.join([
        decrement_stack(),
        pop_value_from_stack(),
        decrement_stack(),
        '@SP',
        'A=M',
        f"D=D{'+' if op == 'add' else '-'}M",
        increment_stack()
    ])


def add() -> str:
    return _do_math_op('add')


def sub() -> str:
    return _do_math_op('sub')


def mem_type_to_base_address(mem_type: str) -> str:
    return {
        'local': '@LCL',
        'argument': '@ARG',
        'this': '@THIS',
        'that': '@THAT',
        'temp': '@5'
    }[mem_type]


def pop_to_mem_segment(mem_type: str, offset: str) -> str:
    mem_base_address = mem_type_to_base_address(mem_type)

    return '\n'.join([
        f'@{offset}',
        'D=A',
        mem_base_address,
        'A=A+D',
        pop_value_from_stack(),
        'M=D',
    ])


def push_from_static(index: str) -> str:
    global FILE_NAME
    return '\n'.join([
        f'@{FILE_NAME}.{index}',
        'D=M',
        push_value_onto_stack(),
    ])


def push_from_pointer(pointer: str) -> str:
    points_to = '@THIS' if pointer == '0' else '@THAT'

    return '\n'.join([
        points_to,
        'D=M',
        push_value_onto_stack(),
    ])


def pop_to_pointer(pointer: str) -> str:
    points_to = '@THIS' if pointer == '0' else '@THAT'

    return '\n'.join([
        pop_value_from_stack(),
        points_to,
        'M=D',
    ])


def pop_to_static(index: str) -> str:
    global FILE_NAME
    return '\n'.join([
        pop_value_from_stack(),
        f'@{FILE_NAME}.{index}',
    ])


def push_from_mem_segment(mem_type: str, offset: str) -> str:
    mem_base_address = mem_type_to_base_address(mem_type)

    return '\n'.join([
        f'@{offset}',
        'D=A',
        mem_base_address,
        'A=A+D',
        'D=M',
        push_value_onto_stack(),
    ])


def parse_instruction(instruction: [str]):
    global FILE_NAME
    words = instruction.split(' ')
    match words:
        case ['add']:
            return add()
        case ['sub']:
            return sub()
        case ['push', 'local' | 'this' | 'that' | 'argument' | 'temp' as mem_segment, offset]:
            return pop_to_mem_segment(mem_segment, offset)
        case ['push', 'static', index]:
            return push_from_static(index)
        case ['push', 'constant', value]:
            return push_value_onto_stack_i(value)
        case ['push', 'pointer', pointer]:
            return push_from_pointer(pointer)
        case ['pop', 'local' | 'this' | 'that' | 'argument' | 'temp' as mem_segment, offset]:
            return push_from_mem_segment(mem_segment, offset)
        case ['pop', 'static', index]:
            return pop_to_static(index)
        case ['pop', 'pointer', pointer]:
            return pop_to_pointer(pointer)


def translate(vm_code: str) -> str:
    return (
        seq(lines(vm_code))
            .map(clean_whitespace)
            .filter(lambda line: line.strip() != '')
            .map(parse_instruction)
            .make_string('\n')
    ) + '\n'


def main():
    global FILE_NAME

    path_to_asm = sys.argv[1]
    FILE_NAME = path_to_asm.split('.')[0].split('/')[-1]
    output_path = path_to_asm.split('.')[0] + '.asm'

    with open(path_to_asm, 'r') as source_file:
        with open(output_path, 'w') as output_file:
            output_file.write(translate(source_file.read()))


if __name__ == '__main__':
    main()
