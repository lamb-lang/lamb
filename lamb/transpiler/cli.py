import argparse
from .lamb_parser import LambParser
from .lamb_transformer import LambTransformer
from .lamb_codegen import LambCodeGenerator

def main():
    parser = argparse.ArgumentParser(description="LaMb Transpiler CLI")
    parser.add_argument("file", help="Path to the LaMb file")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        lamb_code = file.read()

    parser = LambParser()
    transformer = LambTransformer()
    codegen = LambCodeGenerator()

    lamb_ast = parser.parse(lamb_code)
    transformed_ast = transformer.transform(lamb_ast)
    python_code = codegen.generate(transformed_ast)

    if args.output:
        with open(args.output, "w") as file:
            file.write(python_code)
    else:
        print(python_code)

if __name__ == "__main__":
    main()