import sys
import io
from main import run_compiler

# ============================================================
# EZLANG COMPREHENSIVE TEST REGISTRY (V3 - 20 CASES)
# ============================================================

TEST_CASES = [
    # ==========================================
    # CẤP ĐỘ 1: CƠ BẢN (BASIC SYNTAX & MATH)
    # ==========================================
    {"id": "B-01", "name": "Basic Number Print", "code": 'let x = 42. print x.', "expected": "42", "type": "success"},
    {"id": "B-02", "name": "Basic String Print", "code": 'let name = "Mike". print name.', "expected": "Mike", "type": "success"},
    {"id": "B-03", "name": "Variable Re-assignment", "code": 'let a = 1. set a to 5. print a.', "expected": "5", "type": "success"},
    {"id": "B-04", "name": "Basic Arithmetic (+, *)", "code": 'let result = 10 + 5 * 2. print result.', "expected": "20", "type": "success"},
    {"id": "B-05", "name": "Modulo Operator (mod)", "code": 'let m = 17 mod 5. print m.', "expected": "2", "type": "success"},
    {"id": "B-06", "name": "Negative Numbers", "code": 'let n = -10 + 5. print n.', "expected": "-5", "type": "success"},
    {"id": "B-07", "name": "String Concatenation", "code": 'let h = "Hi ". print h + "Mike".', "expected": "Hi Mike", "type": "success"},

    # ==========================================
    # CẤP ĐỘ 2: TRUNG BÌNH (LOGIC, CONTROL FLOW)
    # ==========================================
    {"id": "I-01", "name": "Simple Condition (True)", "code": 'when 5 > 3 then print "Yes". stop.', "expected": "Yes", "type": "success"},
    {"id": "I-02", "name": "Condition with Else", "code": 'let x = 10. when x == 5 then print "Five". else print "Not Five". stop.', "expected": "Not Five", "type": "success"},
    {"id": "I-03", "name": "Boolean Logic (AND/OR)", "code": 'when 1 == 1 and 2 > 5 or 3 == 3 then print "Logic Works". stop.', "expected": "Logic Works", "type": "success"},
    {"id": "I-04", "name": "Boolean Logic (NOT)", "code": 'when not 10 == 5 then print "Not equal". stop.', "expected": "Not equal", "type": "success"},
    {"id": "I-05", "name": "Basic Loop (keep going)", "code": 'let i = 0. keep going: set i to i + 1. until i > 2. print i.', "expected": "3", "type": "success"},
    {"id": "I-06", "name": "List Declaration", "code": 'let arr = [1, 2, 3]. print arr.', "expected": "[1, 2, 3]", "type": "success"},
    {"id": "I-07", "name": "Task Definition & Call", "code": 'define task sayHi print "Hello Task". end task. sayHi.', "expected": "Hello Task", "type": "success"},

    # ==========================================
    # CẤP ĐỘ 3: NÂNG CAO (NESTED & ALGORITHMS)
    # ==========================================
    {"id": "A-01", "name": "Task Modifying State", "code": 'let count = 0. define task inc set count to count + 1. end task. inc. inc. print count.', "expected": "2", "type": "success"},
    {"id": "A-02", "name": "Nested Block (If inside Loop)", "code": '''
        let x = 0. 
        let evens = 0. 
        keep going: 
            set x to x + 1. 
            when x mod 2 == 0 then 
                set evens to evens + 1. 
            stop. 
        until x == 4. 
        print evens.
    ''', "expected": "2", "type": "success"},
    {"id": "A-03", "name": "Nested Block (Loop inside If)", "code": '''
        let flag = 1. 
        let v = 0. 
        when flag == 1 then 
            keep going: 
                set v to v + 1. 
            until v == 3. 
        stop. 
        print v.
    ''', "expected": "3", "type": "success"},
    {"id": "A-04", "name": "Complex Math & Logic", "code": '''
        let a = (10 + 5) * 2. 
        when a >= 30 and not a == 40 then 
            print "Passed". 
        else 
            print "Failed". 
        stop.
    ''', "expected": "Passed", "type": "success"},
    {"id": "A-05", "name": "List with Math Expressions", "code": 'let a = 5. let lst = [a, a * 2, a + 10]. print lst.', "expected": "[5, 10, 15]", "type": "success"},
    
    # Bài test "Trùm cuối": Mô phỏng dãy Fibonacci để ép Interpreter phải chạy biến đổi trạng thái liên tục
    {"id": "A-06", "name": "The Boss (Fibonacci Logic)", "code": '''
        let a = 0. 
        let b = 1. 
        let temp = 0. 
        let i = 0. 
        keep going: 
            set temp to a + b. 
            set a to b. 
            set b to temp. 
            set i to i + 1. 
        until i == 5. 
        print b.
    ''', "expected": "8", "type": "success"}
]

# ============================================================
# AUTOMATED TEST RUNNER
# ============================================================

def run_suite():
    print("="*70)
    print(f"{'EZLANG PROFESSIONAL TEST SUITE (V3)':^70}")
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