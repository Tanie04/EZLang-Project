import sys
import io
from main import run_compiler

# ============================================================
# EZLANG COMPREHENSIVE TEST REGISTRY
# ============================================================

TEST_CASES = [
    # --- 1. FUNDAMENTAL SYNTAX & VARIABLES ---
    {
        "id": "ST-01",
        "name": "Basic Declaration & Print",
        "code": 'let x = 10. print x.',
        "expected": "10",
        "type": "success"
    },
    {
        "id": "ST-02",
        "name": "Variable Re-assignment",
        "code": 'let y = 5. set y to 20. print y.',
        "expected": "20",
        "type": "success"
    },
    {
        "id": "ST-03",
        "name": "String Concatenation",
        "code": 'let msg = "Hello". print msg + " World".',
        "expected": "Hello World",
        "type": "success"
    },
    {
        "id": "ST-04",
        "name": "Case Sensitivity",
        "code": 'let myVar = 1. let myvar = 2. print myVar.',
        "expected": "1",
        "type": "success"
    },

    # --- 2. COMPUTATIONAL & LOGICAL DEPTH ---
    {
        "id": "COMP-01",
        "name": "Math Precedence (PEMDAS)",
        "code": 'let result = (10 + 3) * 2 - (10 mod 4). print result.',
        "expected": "24",
        "type": "success"
    },
    {
        "id": "COMP-02",
        "name": "Boolean Logic Operators",
        "code": '''
            let val = 50.
            when val > 10 and not val == 100 then
                print "Logic holds".
            else
                print "Logic fails".
            stop.
        ''',
        "expected": "Logic holds",
        "type": "success"
    },

    # --- 3. INTEGRATION & CONTROL FLOW ---
    {
        "id": "FLOW-01",
        "name": "Nested Conditionals",
        "code": '''
            let x = 10.
            let y = 20.
            when x < y then
                when x == 10 then
                    print "Nested Success".
                stop.
            stop.
        ''',
        "expected": "Nested Success",
        "type": "success"
    },
    {
        "id": "FLOW-02",
        "name": "Loop Execution",
        "code": '''
            let i = 1.
            let total = 0.
            keep going :
                set total to total + i.
                set i to i + 1.
            until i > 5.
            print total.
        ''',
        "expected": "15",
        "type": "success"
    },

    # --- 4. RESILIENCE & ERROR HANDLING (NEGATIVE TESTS) ---
    {
        "id": "ERR-01",
        "name": "Semantic Error: Re-declaration",
        "code": 'let a = 1. let a = 2.',
        "expected": "already declared",
        "type": "error"
    },
    {
        "id": "ERR-02",
        "name": "Semantic Error: Undeclared Use",
        "code": 'set b to 10.',
        "expected": "undeclared variable",
        "type": "error"
    },
    {
        "id": "ERR-03",
        "name": "Syntax Error: Missing Terminator",
        "code": 'let x = 5',
        "expected": "Expected '.'",
        "type": "error"
    },
    {
        "id": "ERR-04",
        "name": "Syntax Error: Unclosed Block",
        "code": 'when 1 == 1 then print "hi".',
        "expected": "Missing 'stop'",
        "type": "error"
    },
    {
        "id": "ERR-05",
        "name": "Runtime Error: Division by Zero",
        "code": 'let x = 10 / 0.',
        "expected": "Division by zero",
        "type": "error"
    },

    # --- 5. COMPLEX ALGORITHMIC VERIFICATION ---
    {
        "id": "ALGO-01",
        "name": "Even/Odd Counter Algorithm",
        "code": '''
            let count = 1.
            let evens = 0.
            keep going :
                when count mod 2 == 0 then
                    set evens to evens + 1.
                stop.
                set count to count + 1.
            until count > 10.
            print evens.
        ''',
        "expected": "5",
        "type": "success"
    }
]

# ============================================================
# AUTOMATED TEST RUNNER
# ============================================================

def run_suite():
    print("="*70)
    print(f"{'EZLANG PROFESSIONAL TEST SUITE':^70}")
    print("="*70)

    stats = {"pass": 0, "fail": 0}

    for test in TEST_CASES:
        print(f"[{test['id']}] {test['name']:.<45}", end=" ")
        
        # Capture stdout
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        try:
            run_compiler(test['code'])
            success_execution = True
        except Exception:
            success_execution = False
        finally:
            sys.stdout = sys.__stdout__

        actual_output = output_buffer.getvalue()
        
        is_passed = False
        if test['type'] == "success":
            # Check if expected value exists in any of the [EZLang Output] lines
            if f"[EZLang Output]: {test['expected']}" in actual_output:
                is_passed = True
        else:
            # Check if expected error message exists in the logs
            if test['expected'].lower() in actual_output.lower():
                is_passed = True

        if is_passed:
            print("\033[92mPASSED\033[0m")
            stats["pass"] += 1
        else:
            print("\033[91mFAILED\033[0m")
            print(f"   > Expected: {test['expected']}")
            print(f"   > Logs: {actual_output.strip().splitlines()[-1] if actual_output.strip() else 'No output'}")
            stats["fail"] += 1

    print("="*70)
    print(f"RESULTS: {stats['pass']} Passed, {stats['fail']} Failed")
    if stats["fail"] == 0:
        print(f"{'STATUS: ALL SYSTEMS OPERATIONAL':^70}")
    else:
        print(f"{'STATUS: FIX REQUIRED IN PARSER OR INTERPRETER':^70}")
    print("="*70)

if __name__ == "__main__":
    run_suite()