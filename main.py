from flask import Flask, request, jsonify
import sympy as sp

app = Flask(__name__)

# Define symbols
x = sp.symbols("x")

@app.route("/integrate", methods=["POST"])
def integrate():
    try:
        data = request.get_json()

        expr_str = data.get("expr")
        lower = data.get("lower")
        upper = data.get("upper")

        if not expr_str:
            return jsonify({"error": "No expression provided"}), 400

        # Convert string to SymPy expression
        expr = sp.sympify(expr_str)

        # Indefinite integral
        indefinite = sp.integrate(expr, x)

        response = {
            "expression": str(expr),
            "indefinite_integral": str(indefinite)
        }

        # Definite integral if bounds are provided
        if lower is not None and upper is not None:
            definite = sp.integrate(expr, (x, lower, upper))

            response["definite_integral"] = str(definite)
            response["definite_integral_decimal"] = str(definite.evalf())

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
