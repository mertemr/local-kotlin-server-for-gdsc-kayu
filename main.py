import httpx
import json

import lxml.html

import os, sys

pid = os.getpid()

from rich.console import Console
from rich.traceback import install
install(show_locals=True)

console = Console(
    color_system="standard"
)

x = 1
passes = 0

client = httpx.Client(
    base_url="http://localhost:8080/",
    headers={
        "Content-Type": "application/json"
    },
    timeout=30,
    verify=False
)

def get(url: str, params: dict = None) -> dict:
    response = client.get(url, params=params)
    return response.json()

def post(url: str, data: dict = None, type_: str = None) -> dict:
    global x, passes
    response = client.post(url, data=json.dumps(data))
    if type_ == "compiler_run":
        success, output = check_output(response.json())
    
        if not success:
            console.print(f"[bold red]Test Code_{pid}_{x}.kt failed![/bold red]")
            console.print(f"[bold red]{output}[/bold red]")
        else:
            console.print(f"[bold green]Test Code_{pid}_{x}.kt got output:[/bold green]")
            console.print(f"[bold yellow]> {output}[/bold yellow]".lstrip())
            passes += 1
    else:
        passes += 1
    
    x += 1
    return response.json()

def compiler_run(args: str = "", codeblock: str = "") -> dict:
    if not codeblock:
        raise ValueError("codeblock cannot be empty")
    
    files = [
        {
            "name": f"Code_{pid}_{x}.kt",
            "text": codeblock
        }
    ]
    
    print(files[0])
    
    return post("api/compiler/run", data={
        "args": args,
        "files": files
    }, type_="compiler_run")

def compiler_complete(line: int = 0, ch: int = 0, codeblock: str = "") -> dict:
    if not codeblock:
        raise ValueError("codeblock cannot be empty")
    
    files = [
        {
            "name": f"Code_{pid}_{x}.kt",
            "text": codeblock
        }
    ]
    
    return post(f"api/compiler/complete?line={line}&ch={ch}", data={
        "files": files
    }, type_="compiler_complete")

kotlin_codes = [
("""
fun test_message(str: String): String {
    return str.replace("Hello", "Hi")
}

fun main(args: Array<String>) {
    println(test_message(args[0]))
}
""", ["Hello"]),
("""
fun main() {
    var x = 10
    var y = 12
    println(x + y)
}
""", []),
("""
fun main() {
    println("Hello, World!")
}""", [])
]

def check_output(output: dict) -> bool:
    if output["errors"].get(f"Code_{pid}_{x}.kt") != []:
        return False, output["errors"][f"Code_{pid}_{x}.kt"]
    if output["exception"] != None:
        return False, output["exception"]

    stream_output = lxml.html.fromstring(output["text"]).text
    return True, stream_output
    

def main():
    console.print("Checking Version...")
    console.print_json(
        data=get("versions")
    )
    
    for i, kt_code in enumerate(kotlin_codes[2:]):
        code, args = kt_code
                
        if args:
            console.print(f"Running Test {i+1} with {args} on\n{'-'*20}{code}{'-'*20}")
        else:
            console.print(f"Running Test {i+1} on\n{'-'*20}{code}{'-'*20}")
        compiler_run(args=",".join(args), codeblock=code)
    
        
    # print("Enter your code here: ")
    # manual_code = ""
    # while True:
    #     try:
    #         line = input()
    #         manual_code += line + "\n"
    #     except KeyboardInterrupt:
    #         break
        
    # console.print(f"Running Code Test on\n{'-'*20}{manual_code}{'-'*20}\n")
    # compiler_run(codeblock=manual_code)
    
    console.print(f"[bold green]Passed {passes}/{x - 1} tests![/bold green]")
    
if __name__ == "__main__":
    main()