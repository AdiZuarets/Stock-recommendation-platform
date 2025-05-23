from flask import Flask, request, jsonify
import config
import database
import cup_and_handle

app = Flask(__name__)


@app.route("/is-handle-and-cup/<company_symbol>")
def is_cup_and_handle(company_symbol):
    """
    API endpoint to check if a company's stock shows a cup and handle pattern.
    
    Args:
        company_symbol (str): The stock symbol of the company to check
    
    Returns:
        JSON: Result indicating whether the pattern was found or error information
    """

    if company_symbol not in config.COMPANIES:
       return jsonify({
            "Company": company_symbol,
            "Error": "This company not part from the magnificent 7"
       })

    prices_data = database.get_price_data(company_symbol)
    if len(prices_data) < config.MINIMUM_DATA_POINTS:
        return jsonify({
            "Company": company_symbol,
            "Error": "There is not enough data to determine"
        })

    is_cup = cup_and_handle.check_cup_and_handle_pattern(prices_data)
    return jsonify({
        "Company": company_symbol,
        "Is cup and handle": is_cup
    })


if __name__ == "__main__":
    app.run(debug=True)
