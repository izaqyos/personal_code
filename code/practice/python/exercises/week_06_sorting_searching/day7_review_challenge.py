"""
Week 6, Day 7: Review & Challenge - Search and Sort Problems

Learning Objectives:
- Review all Week 6 concepts
- Apply sorting and searching together
- Solve complex algorithmic problems
- Practice optimization techniques
- Build complete solutions

Challenge: Solve real-world sorting and searching problems

Time: 15-20 minutes
"""

import bisect
import heapq
from collections import Counter

# ============================================================
# REVIEW: Week 6 Concepts
# ============================================================

def week6_review():
    """
    Quick review of all Week 6 concepts.
    """
    print("=" * 60)
    print("WEEK 6 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: Built-in Sorting")
    print("  • sorted() vs list.sort()")
    print("  • key functions")
    print("  • Stable Timsort O(n log n)")
    
    print("\nDay 2: Binary Search")
    print("  • O(log n) on sorted arrays")
    print("  • bisect module")
    print("  • bisect_left vs bisect_right")
    
    print("\nDay 3: heapq and Priority Queues")
    print("  • Min-heap operations")
    print("  • Top-k problems")
    print("  • Priority queues")
    
    print("\nDay 4: Custom Sorting")
    print("  • Bubble, Selection, Insertion")
    print("  • Merge, Quick Sort")
    print("  • Counting, Radix Sort")
    
    print("\nDay 5: Search Algorithms")
    print("  • Linear, Jump, Interpolation")
    print("  • Exponential, Ternary")
    print("  • 2D matrix search")
    
    print("\nDay 6: Two Pointers")
    print("  • Two pointers technique")
    print("  • Fast/slow pointers")
    print("  • Sliding window")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Top K Frequent Elements
# ============================================================

def top_k_frequent():
    """
    Find k most frequent elements.
    
    TODO: Use Counter and heap
    """
    print("--- Challenge 1: Top K Frequent Elements ---")
    
    def top_k_frequent_elements(nums, k):
        """Find k most frequent elements"""
        # Count frequencies
        count = Counter(nums)
        
        # Use heap to find top k
        return heapq.nlargest(k, count.keys(), key=count.get)
    
    numbers = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]
    k = 2
    
    print(f"Numbers: {numbers}")
    result = top_k_frequent_elements(numbers, k)
    print(f"Top {k} frequent: {result}")
    
    print()

# ============================================================
# CHALLENGE 2: Merge Intervals
# ============================================================

def merge_intervals():
    """
    Merge overlapping intervals.
    
    TODO: Sort and merge
    """
    print("--- Challenge 2: Merge Intervals ---")
    
    def merge(intervals):
        """Merge overlapping intervals"""
        if not intervals:
            return []
        
        # Sort by start time
        intervals.sort(key=lambda x: x[0])
        
        merged = [intervals[0]]
        
        for current in intervals[1:]:
            last = merged[-1]
            
            if current[0] <= last[1]:
                # Overlapping, merge
                merged[-1] = [last[0], max(last[1], current[1])]
            else:
                # Non-overlapping
                merged.append(current)
        
        return merged
    
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    
    print(f"Intervals: {intervals}")
    result = merge(intervals)
    print(f"Merged: {result}")
    
    print()

# ============================================================
# CHALLENGE 3: Meeting Rooms II
# ============================================================

def meeting_rooms():
    """
    Find minimum meeting rooms needed.
    
    TODO: Use heap for room management
    """
    print("--- Challenge 3: Meeting Rooms II ---")
    
    def min_meeting_rooms(intervals):
        """Find minimum number of meeting rooms needed"""
        if not intervals:
            return 0
        
        # Sort by start time
        intervals.sort(key=lambda x: x[0])
        
        # Heap of end times
        rooms = []
        heapq.heappush(rooms, intervals[0][1])
        
        for i in range(1, len(intervals)):
            # If earliest ending meeting is done, reuse room
            if intervals[i][0] >= rooms[0]:
                heapq.heappop(rooms)
            
            # Add current meeting's end time
            heapq.heappush(rooms, intervals[i][1])
        
        return len(rooms)
    
    meetings = [[0, 30], [5, 10], [15, 20]]
    
    print(f"Meetings: {meetings}")
    rooms_needed = min_meeting_rooms(meetings)
    print(f"Minimum rooms needed: {rooms_needed}")
    
    print()

# ============================================================
# CHALLENGE 4: Search in Rotated Sorted Array
# ============================================================

def search_rotated_complete():
    """
    Complete solution for rotated array search.
    
    TODO: Handle duplicates
    """
    print("--- Challenge 4: Search in Rotated Array ---")
    
    def search(nums, target):
        """Search in rotated sorted array"""
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if nums[mid] == target:
                return mid
            
            # Determine which half is sorted
            if nums[left] <= nums[mid]:
                # Left half is sorted
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                # Right half is sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        
        return -1
    
    arr = [4, 5, 6, 7, 0, 1, 2]
    targets = [0, 3, 5]
    
    print(f"Array: {arr}")
    for target in targets:
        index = search(arr, target)
        result = f"found at {index}" if index != -1 else "not found"
        print(f"  Search {target}: {result}")
    
    print()

# ============================================================
# CHALLENGE 5: Kth Largest Element
# ============================================================

def kth_largest():
    """
    Find kth largest element efficiently.
    
    TODO: Multiple approaches
    """
    print("--- Challenge 5: Kth Largest Element ---")
    
    def find_kth_largest_heap(nums, k):
        """Using heap - O(n log k)"""
        return heapq.nlargest(k, nums)[-1]
    
    def find_kth_largest_sort(nums, k):
        """Using sort - O(n log n)"""
        return sorted(nums, reverse=True)[k - 1]
    
    def find_kth_largest_quickselect(nums, k):
        """Using quickselect - O(n) average"""
        k = len(nums) - k  # Convert to kth smallest
        
        def quickselect(left, right):
            pivot = nums[right]
            i = left
            
            for j in range(left, right):
                if nums[j] <= pivot:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
            
            nums[i], nums[right] = nums[right], nums[i]
            
            if i == k:
                return nums[i]
            elif i < k:
                return quickselect(i + 1, right)
            else:
                return quickselect(left, i - 1)
        
        return quickselect(0, len(nums) - 1)
    
    numbers = [3, 2, 1, 5, 6, 4]
    k = 2
    
    print(f"Numbers: {numbers}")
    print(f"Find {k}th largest:")
    print(f"  Using heap: {find_kth_largest_heap(numbers.copy(), k)}")
    print(f"  Using sort: {find_kth_largest_sort(numbers.copy(), k)}")
    print(f"  Using quickselect: {find_kth_largest_quickselect(numbers.copy(), k)}")
    
    print()

# ============================================================
# CHALLENGE 6: Sort Colors (Dutch Flag)
# ============================================================

def sort_colors():
    """
    Sort array with 3 values (Dutch National Flag).
    
    TODO: One-pass, O(1) space
    """
    print("--- Challenge 6: Sort Colors ---")
    
    def sort_colors_array(nums):
        """Sort array with values 0, 1, 2"""
        low = mid = 0
        high = len(nums) - 1
        
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:  # nums[mid] == 2
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
        
        return nums
    
    colors = [2, 0, 2, 1, 1, 0]
    print(f"Original: {colors}")
    
    sorted_colors = sort_colors_array(colors.copy())
    print(f"Sorted: {sorted_colors}")
    
    print("\n💡 Dutch National Flag: O(n) time, O(1) space")
    
    print()

# ============================================================
# CHALLENGE 7: Find Median from Data Stream
# ============================================================

class MedianFinder:
    """
    Find median from data stream.
    
    TODO: Use two heaps
    """
    
    def __init__(self):
        self.small = []  # Max-heap (negated)
        self.large = []  # Min-heap
    
    def add_num(self, num):
        """Add number to data structure"""
        heapq.heappush(self.small, -num)
        
        # Balance heaps
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self):
        """Get current median"""
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2

def test_median_finder():
    """Test median finder"""
    print("--- Challenge 7: Find Median from Stream ---")
    
    mf = MedianFinder()
    numbers = [1, 2, 3, 4, 5]
    
    print("Adding numbers and tracking median:")
    for num in numbers:
        mf.add_num(num)
        print(f"  Added {num}, median: {mf.find_median()}")
    
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """
    Self-assessment checklist for Week 6.
    """
    print("=" * 60)
    print("WEEK 6 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("Sorting", "Can you use sorted() and key functions effectively?"),
        ("Binary Search", "Can you implement and apply binary search?"),
        ("Heaps", "Do you understand heap operations and top-k problems?"),
        ("Algorithms", "Can you implement classic sorting algorithms?"),
        ("Search Variants", "Do you know different search algorithms?"),
        ("Two Pointers", "Can you apply two pointers technique?"),
        ("Problem Solving", "Can you choose the right algorithm?"),
    ]
    
    print("\nRate yourself (1-5) on these concepts:\n")
    for i, (topic, question) in enumerate(checklist, 1):
        print(f"{i}. {topic}")
        print(f"   {question}")
        print()
    
    print("=" * 60)
    print()

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 6, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week6_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    top_k_frequent()
    merge_intervals()
    meeting_rooms()
    search_rotated_complete()
    kth_largest()
    sort_colors()
    test_median_finder()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 6 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered sorting and searching!")
    print("\n📚 Next: Week 7 - Graph & Tree Algorithms")
    print("\n💡 Keep practicing these fundamental algorithms!")

