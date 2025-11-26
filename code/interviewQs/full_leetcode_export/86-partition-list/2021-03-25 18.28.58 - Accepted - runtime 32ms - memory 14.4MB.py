class Solution:
    def partition(self, head, x):
        """
        use 2 aux lists. smaller and bigger. one pass build them. then connect smaller tail to node with x and node with x.next to bigger
        mem: o(n)
        runtime: o(n)
        """
        s, st, g, gt, prev= None, None, None, None, None #smaller head, smaller tail, greater head, greater tail, previous
        runner = head
        while runner:
            #print('at {}'.format(runner.val))
            if runner.val < x:
                if st:
                    st.next = runner
                    st = st.next
                else:
                    s = runner
                    st = s
                if prev and prev.val>=x: #if prev belongs to greater list, break the link, its ok b/c it would be greater tail
                    prev.next = None
            else:
                if gt:
                    gt.next = runner
                    gt = gt.next
                else:
                    g = runner
                    gt = g
                if prev and prev.val<x: #if prev belongs to smaller list, break the link, its ok b/c it would be smaller tail
                    prev.next = None
            prev = runner
            runner = runner.next
            #printList(s)
            #printList(g)

        if st:
            st.next = g
            return s
        else:
            return g