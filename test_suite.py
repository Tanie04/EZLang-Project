import sys
import io
from main import run_compiler

# ============================================================
# EZLANG COMPREHENSIVE TEST REGISTRY (V2 - UPDATED EBNF)
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
        "name": "String Concatenation",
        "code": 'let msg = "Hello". print msg + " World".',
        "expected": "Hello World",
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

    # --- 4. NEW FEATURE: LISTS ---
    {
        "id": "LIST-01",
        "name": "Basic List Declaration",
        "code": 'let arr = [1, 2, 3, 4]. print arr.',
        "expected": "[1, 2, 3, 4]",
        "type": "success"
    },
    {
        "id": "LIST-02",
        "name": "Empty List",
        "code": 'let emptyArr = []. print emptyArr.',
        "expected": "[]",
        "type": "success"
    },

    # --- 5. NEW FEATURE: FUNCTIONS (TASKS) ---
    {
        "id": "FUNC-01",
        "name": "Define and Call Function",
        "code": '''
            define task greet
                print "Hello from Task".
            end task.
            greet.
        ''',
        "expected": "Hello from Task",
        "type": "success"
    },
    {
        "id": "FUNC-02",
        "name": "Function Modifying State",
        "code": '''
            let counter = 0.
            define task increment
                set counter to counter + 1.
            end task.
            
            increment.
            increment.
            print counter.
        ''',
        "expected": "2",
        "type": "success"
    },

    # --- 6. RESILIENCE & ERROR HANDLING (NEGATIVE TESTS) ---
    {
        "id": "ERR-01",
        "name": "Semantic Error: Re-declaration",
        "code": 'let a = 1. let a = 2.',
        "expected": "already declared",
        "type": "error"
    },
    {
        "id": "ERR-02",
        "name": "Syntax Error: Unclosed Block",
        "code": 'when 1 == 1 then print "hi".',
        "expected": "Missing 'stop'",
        "type": "error"
    },
    {
        "id": "ERR-03",
        "name": "Syntax Error: Unclosed Task",
        "code": 'define task myFunc print "hi".',
        "expected": "Expected 'end'",
        "type": "error"
    }
]

# ============================================================
# AUTOMATED TEST RUNNER
# ============================================================

def run_suite():
    print("="*70)
    print(f"{'EZLANG PROFESSIONAL TEST SUITE (V2)':^70}")
    print("="*70)

    stats = {"pass": 0, "fail": 0}

    for test in TEST_CASES:
        print(f"[{test['id']}] {test['name']:.<45}", end=" ")
        
        # Capture stdout
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        try:
            run_compiler(test['code'])
        except Exception:
            pass
        finally:
            sys.stdout = sys.__stdout__

        actual_output = output_buffer.getvalue()
        
        is_passed = False
        if test['type'] == "success":
            # Check if expected value exists in any of the [EZLang Output] lines
            if f"[EZLang Output]: {test['expected']}" in actual_output or test['expected'] in actual_output:
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