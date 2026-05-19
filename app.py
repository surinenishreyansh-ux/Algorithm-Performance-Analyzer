from flask import Flask, render_template, request, jsonify
import time
import copy

app = Flask(__name__)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort_arrays():
    data = request.get_json()
    numbers_str = data.get('numbers', '')
    
    try:
        # Parse numbers, ignore whitespace
        arr = [int(x.strip()) for x in numbers_str.split(',') if x.strip()]
    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter a comma-separated sequence of numbers.'}), 400
        
    if not arr:
        return jsonify({'error': 'Please provide a valid array of numbers.'}), 400

    arr_for_bubble = copy.deepcopy(arr)
    arr_for_merge = copy.deepcopy(arr)

    # Bubble Sort timing
    start_time = time.perf_counter()
    bubble_sort(arr_for_bubble)
    bubble_time = time.perf_counter() - start_time

    # Merge Sort timing
    start_time = time.perf_counter()
    merge_sort(arr_for_merge)
    merge_time = time.perf_counter() - start_time

    return jsonify({
        'bubble_time': f"{bubble_time:.6f}",
        'bubble_complexity': 'O(n²)',
        'merge_time': f"{merge_time:.6f}",
        'merge_complexity': 'O(n log n)',
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
