from flask import Flask, render_template, request, jsonify
import time
import copy

app = Flask(__name__)


# -----------------------------
# Sorting Algorithms
# -----------------------------

def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # Optimization
        if not swapped:
            break

    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# -----------------------------
# Routes
# -----------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sort', methods=['POST'])
def sort_arrays():
    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'No data received'
        }), 400

    numbers_str = data.get('numbers', '')

    try:
        arr = [
            int(x.strip())
            for x in numbers_str.split(',')
            if x.strip()
        ]

    except ValueError:
        return jsonify({
            'error': 'Invalid input. Enter comma-separated numbers only.'
        }), 400

    if not arr:
        return jsonify({
            'error': 'Please enter at least one number.'
        }), 400

    arr_for_bubble = copy.deepcopy(arr)
    arr_for_merge = copy.deepcopy(arr)

    # Bubble Sort Timing
    start_time = time.perf_counter()
    bubble_sorted = bubble_sort(arr_for_bubble)
    bubble_time = time.perf_counter() - start_time

    # Merge Sort Timing
    start_time = time.perf_counter()
    merge_sorted = merge_sort(arr_for_merge)
    merge_time = time.perf_counter() - start_time

    return jsonify({
        'bubble_time': f"{bubble_time:.6f}",
        'bubble_complexity': 'O(n²)',
        'bubble_sorted': bubble_sorted,

        'merge_time': f"{merge_time:.6f}",
        'merge_complexity': 'O(n log n)',
        'merge_sorted': merge_sorted
    })


if __name__ == '__main__':
    app.run(debug=True)
