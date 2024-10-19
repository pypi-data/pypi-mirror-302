from collections import defaultdict
from bisect import bisect_right

class IntervalHistogram:
    """
    Class that keeps track of a histogram of intervals.
    For any point x, the frequency at x is the number of intervals that contain x.
    Internally, the histogram is stored as a list of key points, which is represented by a tuple (p, p_freq).
    For 2 consecutive key points (p, p_freq) and (q, q_freq), the frequency of all points in the interval [p, q) is p_freq.
    By convention, the end key-point of the entire histogram is (max_x, 0). 
    """
    def __init__(self, min_x=None, max_x=None):
        # Store points and their cumulative frequencies
        self.sorted_points = [] 
        """List of (point, frequency) tuples"""

        self.height = 0
        """The maximum frequency in the histogram"""
        
        # Initialize with boundary points if provided
        if min_x is not None:
            self.sorted_points.append((min_x, 0))
        if max_x is not None:
            self.sorted_points.append((max_x, 0))

    def get_index_before_or_equal(self, point):
        """
        Return the index of the last change point that is <= the query point.
        If no such point exists, return -1.
        """
        idx = bisect_right(self.sorted_points, point, key=lambda x: x[0]) - 1
        return idx

    def get_index_after(self, point):
        """
        Return the index of the first change point that is strictly > the query point.
        If no such point exists, return len(self.sorted_points).
        """
        return bisect_right(self.sorted_points, point, key=lambda x: x[0])

    def frequency(self, point):
        """
        Return the frequency of the point in the histogram.
        We compute this by finding the last change point before or at the query point
        and returning its associated frequency.
        """
        idx = self.get_index_before_or_equal(point)
        if idx == -1:
            return 0
        return self.sorted_points[idx][1]

    def append(self, interval):
        """
        Add an interval to the histogram.
        We modify the frequency change points at the start and end of the interval.
        """
        start, end = interval
        if end < start:
            raise ValueError('invalid interval')

        end_freq = self.frequency(end) # before all else, measure end freq
        
        # Handle start point
        start_idx = self.get_index_before_or_equal(start)
        if 0 <= start_idx < len(self.sorted_points):
            start_freq = self.sorted_points[start_idx][1]
        else:
            start_freq = 0
        if start_idx >= 0 and self.sorted_points[start_idx][0] == start:
            # Point exists, just update frequency
            self.sorted_points[start_idx] = (start, start_freq + 1)
        else:
            # Insert new point with frequency increment
            start_idx += 1
            self.sorted_points.insert(start_idx, (start, start_freq + 1))
        
        if start_freq + 1 > self.height:
            self.height = start_freq + 1
        
        # Handle end point
        end_idx = self.get_index_before_or_equal(end)
        if end_idx >= 0 and self.sorted_points[end_idx][0] == end:
            pass
        else:
            # Insert new point with same frequency as before
            end_idx += 1
            self.sorted_points.insert(end_idx, (end, end_freq))
        
        # increase all frequencies in between
        for i in range(start_idx+1, end_idx):
            # self.sorted_points[i][1] += 1
            self.sorted_points[i] = (self.sorted_points[i][0], self.sorted_points[i][1] + 1)

    def __str__(self):
        """Return a string representation of the histogram."""
        return f"IntervalHistogram(points={self.sorted_points})"
    
    def iter_intervals_below(self, threshold):
        """
        Yields all the intervals [p, q) such that for all x in [p, q), frequency(x) <= threshold.
        Note that this will merge consecutive intervals, even if they have different frequencies, as long as they are all <= threshold.

        Yields intervals of [p, q).
        """
        if not self.sorted_points:
            return
            
        current_start = None  # Start of the current interval
        for i in range(len(self.sorted_points)):
            point, freq = self.sorted_points[i]
            
            # If frequency is <= threshold and we haven't started an interval
            if freq <= threshold:
                if current_start is None and i < len(self.sorted_points) - 1: # don't start an interval at the global end point
                    current_start = point
            # If frequency > threshold and we have an open interval
            else:
                if current_start is not None:
                    yield (current_start, point)
                    current_start = None
                
        # Handle the last point specially if we have an open interval
        if current_start is not None:
            yield (current_start, point)
    



def run_tests():
    """Run a comprehensive set of tests for the IntervalHistogram class."""
    
    # Test 1: Basic initialization
    hist = IntervalHistogram()
    assert len(hist.sorted_points) == 0, "Empty histogram should have no points"
    # assert len(hist.change_points) == 0, "Empty histogram should have no change points"

    # Test 2: Initialize with boundaries
    hist = IntervalHistogram(min_x=0, max_x=10)
    assert len(hist.sorted_points) == 2, "Should have two boundary points"
    assert hist.sorted_points[0] == (0, 0), "First point should be (0, 0)"
    assert hist.sorted_points[1] == (10, 0), "Second point should be (10, 0)"

    # Test 3: Basic interval addition
    hist = IntervalHistogram()
    hist.append((1, 5))
    assert len(hist.sorted_points) == 2, "Should have two points after adding interval"
    assert hist.sorted_points[0] == (1, 1), "Start point should have frequency 1"
    assert hist.sorted_points[1] == (5, 0), "End point should have frequency 0"

    # Test 4: Overlapping intervals
    hist = IntervalHistogram()
    hist.append((1, 5))
    hist.append((3, 7))
    expected_points = [(1, 1), (3, 2), (5, 1), (7, 0)]
    assert hist.sorted_points == expected_points, f"Expected {expected_points}, got {hist.sorted_points}"

    # Test 5: Frequency queries
    hist = IntervalHistogram()
    hist.append((1, 5))
    hist.append((3, 7))
    test_points = [
        (0, 0),  # Before all intervals
        (2, 1),  # Inside first interval only
        (4, 2),  # Inside both intervals
        (6, 1),  # Inside second interval only
        (8, 0),  # After all intervals
    ]
    for point, expected_freq in test_points:
        assert hist.frequency(point) == expected_freq, f"Expected frequency {expected_freq} at point {point}, got {hist.frequency(point)}"

    # Test 6: Edge cases
    hist = IntervalHistogram()
    hist.append((1, 2))
    hist.append((2, 3))  # Adjacent intervals
    assert hist.frequency(2) == 1, "Point at interval boundary should belong to second interval only"

    # Test 7: Error cases
    hist = IntervalHistogram()
    try:
        hist.append((5, 3))  # Start > end
        assert False, "Should raise ValueError for invalid interval"
    except ValueError:
        pass

    try:
        hist.append(("a", "b"))  # Non-numeric endpoints
        assert False, "Should raise ValueError for non-numeric endpoints"
    except ValueError:
        pass

    # Test 8: Multiple overlapping intervals
    hist = IntervalHistogram()
    intervals = [(1, 5), (2, 6), (3, 7), (4, 8)]
    max_freq = 0
    for interval in intervals:
        hist.append(interval)
        max_freq += 1
        assert max(point[1] for point in hist.sorted_points) == max_freq, f"Maximum frequency should be {max_freq}"

    # Test 9: Binary search edge cases
    hist = IntervalHistogram()
    hist.append((1, 5))
    assert hist.get_index_before_or_equal(0) == -1, "Should return -1 for point before all intervals"
    assert hist.get_index_before_or_equal(6) == 1, "Should return last index for point after all intervals"
    assert hist.get_index_after(6) == 2, "Should return length for point after all intervals"

    # Test 10: Non-overlapping intervals
    hist = IntervalHistogram()
    intervals = [(1, 2), (3, 4), (5, 6), (7, 8)]
    max_freq = 0
    for interval in intervals:
        hist.append(interval)
    expected_points = [(1, 1), (2, 0), (3, 1), (4, 0), (5, 1), (6, 0), (7, 1), (8, 0)]
    assert hist.sorted_points == expected_points, f"Expected {expected_points}, got {hist.sorted_points}"




    print("All tests passed!")

# Run the tests
if __name__ == "__main__":
    run_tests()