import argparse
import subprocess
from .lamb_parser import LambParser
from .lamb_transformer import LambTransformer
from .lamb_codegen import LambCodeGenerator

def run_model(model_name):
    if model_name == 'phi':
        subprocess.run(['ollama', 'run', 'phi'])
    else:
        print(f"Model '{model_name}' is not supported.")

def main():
    parser = argparse.ArgumentParser(description="LaMb Transpiler and Runner CLI")
    subparsers = parser.add_subparsers(dest='command')
    
    # Sub-parser for file transpilation
    transpile_parser = subparsers.add_parser('transpile')
    transpile_parser.add_argument("file", help="Path to the LaMb file")
    transpile_parser.add_argument("-o", "--output", help="Output file path")
    
    # Sub-parser for model running
    run_parser = subparsers.add_parser('run')
    run_parser.add_argument("model", help="Model name to run")

    args = parser.parse_args()

    if args.command == 'transpile':
        with open(args.file, "r") as file:
            lamb_code = file.read()

        lamb_parser = LambParser()
        transformer = LambTransformer()
        codegen = LambCodeGenerator()

        lamb_ast = lamb_parser.parse(lamb_code)
        transformed_ast = transformer.transform(lamb_ast)
        python_code = codegen.generate(transformed_ast)

        if args.output:
            with open(args.output, "w") as file:
                file.write(python_code)
        else:
            print(python_code)
    elif args.command == 'run':
        run_model(args.model)

if __name__ == "__main__":
    main()
