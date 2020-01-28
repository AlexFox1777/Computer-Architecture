"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 0xFF
        self.registers = [0] * 8
        self.pc = 0
        self.opcodes = {
            0b10000010: 'ldi',
            0b01000111: 'prn',
            0b00000001: 'hlt',
            0b10100010: 'mul',
        }

    def ram_read(self, address):
        return self.ram[address]

    def raw_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        # address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            address = 0
            if len(sys.argv) != 2:
                print("Usage: file.py filename", file=sys.stderr)
                sys.exit(1)
            else:
                with open(sys.argv[1]) as f:
                    for line in f:
                        comment_split = line.split("#")
                        num = comment_split[0].strip()

                        if num == "":
                            continue  # Ignore blank lines

                        value = int(num, 2)
                        self.ram[address] = value
                        address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def prn(self):
        """
        Print numeric value stored in the given register
        """
        adr = self.ram_read(self.pc + 1)
        reg = self.registers[adr]
        print('Value = ', reg)
        self.pc += 1

    def ldi(self):
        """
        Set the value of a register to an integer
        """
        # Memory Address Register, holds the memory address we're reading or writing
        mar = self.ram_read(self.pc + 1)
        #  Memory Data Register, holds the value to write or the value just read
        mdr = self.ram_read(self.pc + 2)
        self.registers[mar] = mdr
        self.pc += 2

    def mul(self):
        r0 = self.ram[self.pc + 1]
        r1 = self.ram[self.pc + 2]
        result = self.registers[r0] * self.registers[r1]
        print(f"Multiplying operation result: {result}")

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            ir = self.ram_read(self.pc)
            opcode = self.opcodes.get(ir)
            if opcode:
                if opcode == 'hlt':
                    running = False
                else:
                    func = getattr(self, opcode)
                    func()
                    self.pc += 1
            else:
                running = False
