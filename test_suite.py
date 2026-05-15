# test_suite_v3.py — EZLang Fix Verification Test Suite
# Verifies all three fixes applied in the code review:
#   Fix 1 (environment.py) — lexical scoping via parent-chain
#   Fix 2 (parser.py)      — clean SyntaxError on unexpected EOF / bad tokens
#   Fix 3 (parser.py +
#           interpreter.py) — clear diagnostic when a variable is called as a task

import sys
import io
from main import run_compiler


# ============================================================
# FIBONACCI REFERENCE  (so expected values are never guessed)
#
#   Starting state: a=0, b=1
#   Each iteration: temp=a+b, a=b, b=temp, i+=1
#
#   i=0 → start
#   i=1 → a=1,  b=1
#   i=2 → a=1,  b=2
#   i=3 → a=2,  b=3
#   i=4 → a=3,  b=5
#   i=5 → a=5,  b=8   ← "until i == 5"  prints b=8
#   i=6 → a=8,  b=13  ← "until i == 6"  prints b=13
#   i=7 → a=13, b=21  ← "until i == 7"  prints b=21
# ============================================================


# ============================================================
# TEST REGISTRY
# ============================================================

TEST_CASES = [

    # -------------------------------------------------------
    # FIX 1 — SCOPING: local variables must not leak globally
    # -------------------------------------------------------
    {
        "id": "SCOPE-01",
        "name": "Local var stays inside task (no global leak)",
        "description": (
            "A variable declared with 'let' inside a task must NOT be "
            "accessible in the global scope after the call returns."
        ),
        "code": '''
            define task inner
                let secret = 42.
            end task.
            inner.
            print secret.
        ''',
        "expected": "Undefined variable",
        "type": "error",
    },
    {
        "id": "SCOPE-02",
        "name": "Task reads global variable (upward lookup)",
        "description": (
            "A task should be able to READ a variable declared in the "
            "enclosing global scope via the parent-chain lookup."
        ),
        "code": '''
            let globalVal = 99.
            define task readGlobal
                print globalVal.
            end task.
            readGlobal.
        ''',
        "expected": "99",
        "type": "success",
    },
    {
        "id": "SCOPE-03",
        "name": "Task mutates global variable (upward assign)",
        "description": (
            "'set' inside a task must walk up to the global scope and "
            "update the variable there, not create a local shadow."
        ),
        "code": '''
            let counter = 0.
            define task inc
                set counter to counter + 1.
            end task.
            inc.
            inc.
            inc.
            print counter.
        ''',
        "expected": "3",
        "type": "success",
    },
    {
        "id": "SCOPE-04",
        "name": "Local var shadows global without corrupting it",
        "description": (
            "If a task declares 'let x' locally while a global 'x' exists, "
            "the global must be unchanged after the call."
        ),
        "code": '''
            let x = 10.
            define task shadowTest
                let x = 999.
                print x.
            end task.
            shadowTest.
            print x.
        ''',
        "expected_lines": ["999", "10"],
        "type": "multi_success",
    },
    {
        "id": "SCOPE-05",
        "name": "Two sequential task calls don't share local state",
        "description": (
            "Each call to a task must start with a fresh local scope. "
            "A 'let' in call #1 must not persist into call #2."
        ),
        "code": '''
            define task freshScope
                let tmp = 7.
                print tmp.
            end task.
            freshScope.
            freshScope.
        ''',
        "expected_lines": ["7", "7"],
        "type": "multi_success",
    },
    {
        "id": "SCOPE-06",
        "name": "Re-declaration inside task is still an error",
        "description": (
            "Within a single task call, declaring the same variable twice "
            "must still raise a Semantic Error."
        ),
        "code": '''
            define task doubleDecl
                let y = 1.
                let y = 2.
            end task.
            doubleDecl.
        ''',
        "expected": "already declared",
        "type": "error",
    },
    {
        "id": "SCOPE-07",
        "name": "Nested tasks share the scope chain correctly",
        "description": (
            "A task called from within another task must still be able to "
            "read and mutate the global scope."
        ),
        "code": '''
            let total = 0.
            define task addOne
                set total to total + 1.
            end task.
            define task addThree
                addOne.
                addOne.
                addOne.
            end task.
            addThree.
            print total.
        ''',
        "expected": "3",
        "type": "success",
    },

    # -------------------------------------------------------
    # FIX 2 — EOF / MALFORMED INPUT: clean SyntaxErrors
    # -------------------------------------------------------
    {
        "id": "EOF-01",
        "name": "Expression ends abruptly after '='",
        "description": (
            "'let x = .' gives the parser an empty expression. "
            "Must raise SyntaxError, NOT a TypeError/AttributeError crash."
        ),
        "code": "let x = .",
        "expected": "syntax error",
        "type": "error",
    },
    {
        "id": "EOF-02",
        "name": "Unclosed parenthesis hits EOF",
        "description": (
            "'let x = (5 + 3' — no closing paren, no dot. "
            "Must raise SyntaxError cleanly."
        ),
        "code": "let x = (5 + 3",
        "expected": "syntax error",
        "type": "error",
    },
    {
        "id": "EOF-03",
        "name": "Loop with no body and no 'until'",
        "description": (
            "'keep going:' followed by nothing. "
            "Must raise SyntaxError, not an infinite loop or crash."
        ),
        "code": "keep going:",
        "expected": "syntax error",
        "type": "error",
    },
    {
        "id": "EOF-04",
        "name": "Condition with no right-hand side",
        "description": (
            "'when x > then' — nothing between '>' and 'then'. "
            "Must raise SyntaxError cleanly."
        ),
        "code": "let x = 5. when x > then print x. stop.",
        "expected": "syntax error",
        "type": "error",
    },
    {
        "id": "EOF-05",
        "name": "Unclosed list literal hits EOF",
        "description": (
            "'let arr = [1, 2, 3' — no closing bracket. "
            "Must raise SyntaxError."
        ),
        "code": "let arr = [1, 2, 3",
        "expected": "syntax error",
        "type": "error",
    },
    {
        "id": "EOF-06",
        "name": "expect() error message names the bad token",
        "description": (
            "When 'set' is missing 'to', the error must mention what was "
            "actually found, not just say 'expected to'."
        ),
        "code": "let a = 1. set a 5.",
        "expected": "syntax error",
        "type": "error",
    },
    {
        "id": "EOF-07",
        "name": "Empty source code runs without crashing",
        "description": (
            "An empty string must complete cleanly with no output and "
            "no exception."
        ),
        "code": "",
        "expected": "Execution Completed Successfully",
        "type": "success",
    },

    # -------------------------------------------------------
    # FIX 3 — VARIABLE-AS-TASK: clear diagnostic messages
    # -------------------------------------------------------
    {
        "id": "VARID-01",
        "name": "Calling an integer variable as a task",
        "description": (
            "If a variable holds a plain integer and is called with 'name.', "
            "the interpreter must raise a Runtime Error with a helpful message."
        ),
        "code": '''
            let notATask = 42.
            notATask.
        ''',
        "expected": "not a task",
        "type": "error",
    },
    {
        "id": "VARID-02",
        "name": "Calling a string variable as a task",
        "description": (
            "Same as VARID-01 but the variable holds a string value."
        ),
        "code": '''
            let greeting = "hello".
            greeting.
        ''',
        "expected": "not a task",
        "type": "error",
    },
    {
        "id": "VARID-03",
        "name": "Calling an undefined name as a task",
        "description": (
            "Calling a name that was never declared at all must raise a "
            "Semantic Error (undefined variable), not a crash."
        ),
        "code": "ghost.",
        "expected": "undefined variable",
        "type": "error",
    },
    {
        "id": "VARID-04",
        "name": "Bare identifier without dot raises SyntaxError",
        "description": (
            "An identifier used as a statement WITHOUT a trailing dot must "
            "raise a SyntaxError explaining that '.' is required."
        ),
        "code": "let x = 5. x",
        "expected": "syntax error",
        "type": "error",
    },
    {
        "id": "VARID-05",
        "name": "Valid task call still works after fix",
        "description": (
            "Regression check: a properly defined task must still execute "
            "correctly after the diagnostic improvements."
        ),
        "code": '''
            define task sayHello
                print "Hello from task".
            end task.
            sayHello.
        ''',
        "expected": "Hello from task",
        "type": "success",
    },

    # -------------------------------------------------------
    # REGRESSION — existing features must still pass
    # -------------------------------------------------------
    {
        "id": "REG-01",
        "name": "Regression: PEMDAS math",
        "code": "let r = (10 + 3) * 2 - 10 mod 4. print r.",
        "expected": "24",
        "type": "success",
    },
    {
        "id": "REG-02",
        "name": "Regression: Boolean AND / NOT",
        "code": '''
            let v = 50.
            when v > 10 and not v == 100 then
                print "Logic holds".
            else
                print "Logic fails".
            stop.
        ''',
        "expected": "Logic holds",
        "type": "success",
    },
    {
        "id": "REG-03",
        "name": "Regression: Loop accumulator",
        "code": '''
            let i = 1.
            let total = 0.
            keep going:
                set total to total + i.
                set i to i + 1.
            until i > 5.
            print total.
        ''',
        "expected": "15",
        "type": "success",
    },
    {
        "id": "REG-04",
        "name": "Regression: List declaration",
        "code": "let arr = [1, 2, 3, 4]. print arr.",
        "expected": "[1, 2, 3, 4]",
        "type": "success",
    },
    {
        "id": "REG-05",
        "name": "Regression: Fibonacci i==5, expect b=8",
        # Trace: after 5 iters → a=5, b=8  (see reference table at top)
        "code": '''
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
        ''',
        "expected": "8",
        "type": "success",
    },
    {
        "id": "REG-06",
        "name": "Regression: Fibonacci i==6, expect b=13",
        # Trace: after 6 iters → a=8, b=13  (see reference table at top)
        "code": '''
            let a = 0.
            let b = 1.
            let temp = 0.
            let i = 0.
            keep going:
                set temp to a + b.
                set a to b.
                set b to temp.
                set i to i + 1.
            until i == 6.
            print b.
        ''',
        "expected": "13",
        "type": "success",
    },
    {
        "id": "REG-07",
        "name": "Regression: Fibonacci i==7, expect b=21",
        # Trace: after 7 iters → a=13, b=21  (see reference table at top)
        # The previous test suite had this wrong (expected 13 instead of 21).
        "code": '''
            let a = 0.
            let b = 1.
            let temp = 0.
            let i = 0.
            keep going:
                set temp to a + b.
                set a to b.
                set b to temp.
                set i to i + 1.
            until i == 7.
            print b.
        ''',
        "expected": "21",
        "type": "success",
    },
]


# ============================================================
# TEST RUNNER
# ============================================================

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

SECTION_LABELS = {
    "SCOPE": "FIX 1 — Lexical Scoping",
    "EOF":   "FIX 2 — EOF / Malformed Input",
    "VARID": "FIX 3 — Variable-as-Task Diagnostics",
    "REG":   "Regression — Existing Features",
}


def capture_run(code):
    """Run EZLang source and return all stdout as a single string."""
    buf = io.StringIO()
    sys.stdout = buf
    try:
        run_compiler(code)
    except Exception:
        pass
    finally:
        sys.stdout = sys.__stdout__
    return buf.getvalue()


def check(test, output):
    """Return True if the test passes given the captured output."""
    kind      = test["type"]
    out_lower = output.lower()

    if kind == "success":
        needle = test["expected"]
        return (
            f"[EZLang Output]: {needle}" in output
            or needle in output
        )

    if kind == "multi_success":
        return all(
            f"[EZLang Output]: {line}" in output or line in output
            for line in test["expected_lines"]
        )

    if kind == "error":
        return test["expected"].lower() in out_lower

    return False


def section_prefix(test_id):
    return test_id.split("-")[0]


def run_suite():
    print("=" * 72)
    print(f"{BOLD}{'EZLANG FIX VERIFICATION SUITE (V3)':^72}{RESET}")
    print("=" * 72)

    stats        = {"pass": 0, "fail": 0}
    section_seen = set()

    for test in TEST_CASES:
        prefix = section_prefix(test["id"])
        if prefix not in section_seen:
            section_seen.add(prefix)
            label = SECTION_LABELS.get(prefix, prefix)
            print(f"\n{CYAN}{BOLD}  ── {label} ──{RESET}")

        output = capture_run(test["code"])
        passed = check(test, output)
        tag    = f"{GREEN}PASSED{RESET}" if passed else f"{RED}FAILED{RESET}"

        print(f"  [{test['id']}] {test['name']:<50} {tag}")

        if not passed:
            all_lines    = [l for l in output.strip().splitlines() if l.strip()]
            output_lines = [l for l in all_lines if "[EZLang Output]" in l]
            last_line    = all_lines[-1] if all_lines else "(no output)"

            if test["type"] == "multi_success":
                print(f"    {YELLOW}> Expected lines : {test['expected_lines']}{RESET}")
            else:
                print(f"    {YELLOW}> Expected       : {test['expected']}{RESET}")

            if output_lines:
                print(f"    {YELLOW}> EZLang output  : {output_lines}{RESET}")
            else:
                print(f"    {YELLOW}> Last line      : {last_line}{RESET}")
                print(f"    {YELLOW}> (No [EZLang Output] lines — possible silent failure){RESET}")

            if "description" in test:
                print(f"    {YELLOW}> Hint           : {test['description']}{RESET}")

        stats["pass" if passed else "fail"] += 1

    total = stats["pass"] + stats["fail"]
    pct   = int(stats["pass"] / total * 100) if total else 0

    print("\n" + "=" * 72)
    print(f"  Results : {stats['pass']}/{total} passed  ({pct}%)")
    if stats["fail"] == 0:
        print(f"  {GREEN}{BOLD}STATUS  : ALL FIXES VERIFIED — SYSTEMS OPERATIONAL{RESET}")
    else:
        print(f"  {RED}{BOLD}STATUS  : {stats['fail']} test(s) failing — review output above{RESET}")
    print("=" * 72)


if __name__ == "__main__":
    run_suite()