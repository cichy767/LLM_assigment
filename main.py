from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')


def remove_immediate_duplicate_lines(code):
    lines = code.strip().split('\n')
    cleaned_lines = [lines[0]] if lines else []
    for line in lines[1:]:
        if line != cleaned_lines[-1]:
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)


def remove_repeated_blocks(text, block_separator='\n\n'):
    """
    Removes repeated blocks of text separated by a specific separator.
    """
    blocks = text.split(block_separator)
    unique_blocks = []
    seen_blocks = set()

    for block in blocks:
        trimmed_block = block.strip()
        if trimmed_block and trimmed_block not in seen_blocks:
            unique_blocks.append(block)
            seen_blocks.add(trimmed_block)

    return block_separator.join(unique_blocks)


@app.route('/generate-code', methods=['POST'])
def generate_code():
    user_input = request.json.get('prompt')
    try:
        response = generator(user_input, max_length=500, temperature=0.2, early_stopping=True)
        generated_code = response[0]['generated_text']
        cleaned_code = remove_repeated_blocks(generated_code, block_separator='\n\n')
        print(f"cleaned_code: {cleaned_code}")
        return jsonify({"generated_text": cleaned_code}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"}, 200)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
