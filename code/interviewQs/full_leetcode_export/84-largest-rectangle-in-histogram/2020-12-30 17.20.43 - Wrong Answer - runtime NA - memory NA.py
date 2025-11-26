
class Solution:
    def largestRectangleArea(self, heights):
        """
        so for rectangle area we do width*height. 
        width is endpos-startpos+1
        height we keep track of start positions (in a stack) and height.
        we also keep a stack with current largest height, whenever we enounter
        a smaller height we pop all the larger heights and their start position
        - because this means that they have reached their end. we calc area and
          update max area var
        if encounter same height just continue 
        if we encounter larger height this means we start a new possible
        rectangle, so we add a new start pos to positions stack
        At the end just process what's left in the stack pairs of height, start
        pos
        """
        max_area = 0
        startpos_stack = []
        heights_stack = []

        for i,h in enumerate(heights):
            #new rectangle detected
            if (len(startpos_stack) == 0) or (len(heights_stack) > 0 and h > heights_stack[-1]):
                startpos_stack.append(i)
                heights_stack.append(h)
            else:
                if (len(heights_stack) > 0 and h == heights_stack[-1]):
                    continue
                else: # h<heights_stack[-1]
            #we need to terminate all rectangles higher than h
                    while len(heights_stack) > 0 and h < heights_stack[-1]:
                        start = startpos_stack.pop()
                        height = heights_stack.pop()
                        area = (i-start)*height
                        max_area = max(max_area, area)

        last_pos = len(heights)
        while (len(startpos_stack) > 0) and (len(heights_stack) > 0):
                start = startpos_stack.pop()
                height = heights_stack.pop()
                area = (last_pos-start)*height
                max_area = max(max_area, area)

        return max_area