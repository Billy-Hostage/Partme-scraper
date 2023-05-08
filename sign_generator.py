
from subprocess import check_output

def getURLSign(url: str) -> str:
    out = check_output(
        ['node', './sign_gen.js', url], timeout=60)
    return out.decode()
