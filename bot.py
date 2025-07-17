import pandas as pd
import os
import random
from datetime import datetime, timedelta
import re

def list_csv_files():
    files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not files:
        print("❌ Tidak ada file CSV di direktori ini.")
        exit()
    print("\n📂 Pilih file CSV:")
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")
    choice = int(input("\n📥 Masukkan nomor file CSV: ")) - 1
    return files[choice]

def extract_number(text):
    """Ambil angka dari string seperti '5.02VANA'"""
    return float(re.findall(r"[\d.]+", str(text))[0])

def extract_symbol(text):
    """Ambil simbol token dari string seperti '5.02VANA'"""
    match = re.findall(r"[A-Z]+", str(text))
    return match[0] if match else ""

def generate_random_datetime(start_year=2023, end_year=2025):
    start = datetime(start_year, 1, 1, 0, 0, 0)
    end = datetime(end_year, 12, 31, 23, 59, 59)
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return (start + timedelta(seconds=random_seconds)).strftime('%Y-%m-%d %H:%M:%S')

def main():
    input_file = list_csv_files()
    df = pd.read_csv(input_file)

    required_cols = ['Date(UTC)', 'Pair', 'Side', 'Price', 'Executed', 'Amount', 'Fee']
    for col in required_cols:
        if col not in df.columns:
            print(f"❌ Kolom '{col}' tidak ditemukan.")
            return

    try:
        num_clones = int(input("🔁 Masukkan jumlah clone per baris: "))
    except ValueError:
        print("❌ Input harus berupa angka.")
        return

    all_rows = []

    for _, row in df.iterrows():
        price = float(row['Price'])
        token_symbol = extract_symbol(row['Executed'])

        for _ in range(num_clones):
            # Random amount in USD
            target_value = random.uniform(2000, 10000)
            executed_amount = round(target_value / price, 8)
            fee = round(executed_amount * 0.001, 8)  # 0.1% fee

            new_row = {
                'Date(UTC)': generate_random_datetime(2023, 2025),
                'Pair': row['Pair'],
                'Side': row['Side'],
                'Price': f"{price:.6f}",
                'Executed': f"{executed_amount:.8f}{token_symbol}",
                'Amount': f"{target_value:.8f}USDT",
                'Fee': f"{fee:.8f}{token_symbol}"
            }

            all_rows.append(new_row)

    df_final = pd.DataFrame(all_rows, columns=required_cols)

    # Simpan file
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_cloned.csv"
    df_final.to_csv(output_file, index=False, quoting=1)  # QUOTE_ALL untuk format seperti contoh

    print(f"\n✅ File hasil disimpan sebagai: {output_file}")

if __name__ == "__main__":
    main()
