import aiohttp

async def get_ip_details(ip):
  final_ip = ip

  if ip in ["::ffff:127.0.0.1", "::1"]:
    final_ip = "185.65.135.253"

  err_response = {
    "status": "error",
    "timezone": "Europe/Istanbul",
    "location": {
      "countryCode": "TR",
      "country": "Turkey",
      "city": "Istanbul",
      "region": "Beşiktaş",
      "zip": 34110,
      "full": "Beşiktaş, Istanbul, Turkey",
    },
    "isp": "",
    "address": final_ip,
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"http://ip-api.com/json/{final_ip}") as response:
        data = await response.json()

    if data["status"] == "success":
      return {
        "status": "success",
        "timezone": data["timezone"],
        "location": {
          "countryCode": data["countryCode"],
          "country": data["country"],
          "city": data["city"],
          "region": data["regionName"],
          "zip": data["zip"],
          "full": (
            f"{data['regionName'] + ', ' if data['city'] != data['regionName'] else ''}"
            f"{data['city']}, {data['country']}"
          ),
        },
        "isp": data["isp"],
        "address": data["query"],
      }
    else:
      return err_response
  except Exception as e:
    return err_response
