every clock tick
the cpu does something

run noop instruction
run addx V instruction
    1: step 1 ->
    2. step 2 -> write x register

0   1

states
    idle
    addx
    done

    busy -> running current instruction
    idle -> ready to take text instruction
    done -> no more instructions left