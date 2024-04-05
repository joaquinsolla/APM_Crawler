def format_json():
    input_file_path = 'dumps/parking.json'
    output_file_path = 'dumps/parking_formatted.json'

    try:
        with open(input_file_path, 'r', encoding='utf-8') as file_in:
            data = file_in.read()

        data = data.replace('[\n', '{\n"plazas": [\n')
        data = data.replace('\n]', '\n]\n}')

        with open(output_file_path, 'w', encoding='utf-8') as file_out:
            file_out.write(data)

        print(f"[OK] Archivo formateado creado: {output_file_path}")
    except Exception as e:
        print(f"[ERR] No se pudo formatear el archivo JSON: {e}.")

if __name__ == "__main__":
    format_json()
