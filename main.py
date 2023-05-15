import quart
import quart_cors
from quart import Quart, jsonify, request
import httpx

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
url = 'https://polkadot.api.subscan.io/api'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': 'abb5735610c64c40a761f2bcb185230c' # free api key so idc really 
}

@app.get("/now")
async def get_timestamp():
    print ("GET TIMESTAMP")
    payload = {}

    async with httpx.AsyncClient() as client:
        response = await client.post(url+'/now', json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to make the POST request"}), 500

@app.get("/metadata")
async def get_metadata():
    payload = {}

    async with httpx.AsyncClient() as client:
        response = await client.post(url+'/scan/metadata', json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to make the POST request"}), 500
    
# @app.get('/accounts')
# async def get_accounts(row, page, order='desc', order_field='', min_balance=100, max_balance=100000000, filter, address):
#     payload = {}

#     async with httpx.AsyncClient() as client:
#         response = await client.post(url+'/scan/accounts', json=payload, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 200:
#         return jsonify(response.json())
#     else:
#         return jsonify({"error": "Failed to make the POST request"}), 500
    
@app.get('/proposals')
async def get_proposals():
    payload = {
        'row': 6,
        'page': 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url+'/scan/treasury/proposals', json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to make the POST request"}), 500
    
@app.get('/daily-stats')
async def get_daily_stats():
    payload = {
        "start": "2023-05-13",
        "end": "2023-05-14",
        "format": "day",
        "category": "TreasurySpend"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url+'/v2/scan/daily', json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to make the POST request"}), 500

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
