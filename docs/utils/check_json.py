"""Local semantic checker. Usage: python check_json.py expected.json actual.json"""
import json,math,sys
def equal(expected,actual):
    if isinstance(expected,bool):return isinstance(actual,bool) and expected==actual
    if isinstance(expected,(int,float)):
        return isinstance(actual,(int,float)) and not isinstance(actual,bool) and math.isfinite(actual) and abs(expected-actual)<=1e-6+1e-6*abs(expected)
    if isinstance(expected,str) or expected is None:return type(actual) is type(expected) and expected==actual
    if isinstance(expected,list):return isinstance(actual,list) and len(expected)==len(actual) and all(equal(a,b) for a,b in zip(expected,actual))
    if isinstance(expected,dict):return isinstance(actual,dict) and set(expected)==set(actual) and all(equal(v,actual[k]) for k,v in expected.items())
    return False
if __name__=='__main__':
    with open(sys.argv[1],encoding='utf-8') as f:expected=json.load(f)
    try:
        with open(sys.argv[2],encoding='utf-8') as f:actual=json.load(f)
        ok=equal(expected,actual)
    except (ValueError,OSError):ok=False
    print('AC' if ok else 'WA');sys.exit(0 if ok else 1)
