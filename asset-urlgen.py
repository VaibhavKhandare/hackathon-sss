base_url = "https://cdn.phaserfiles.com/v385/assets/games/coin-clicker/"


asset_files = ["background.png", "cc-logo.png", 'coin.png', 'coin.json']


for asset in asset_files:
    print(f'wget {base_url}{asset} -O public/images/{asset}')

print()